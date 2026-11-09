/**
 * ============================================================================
 * PHASE 2: DIVINE SANCTUM ENVIRONMENT ENGINE (CINEMATIC 4K DARSHAN)
 * 
 * Implements 7 continuous natural devotional animations at 60 FPS:
 * 1. Multi-depth floating rose & lotus petals (foreground bokeh, midground, background)
 * 2. 3-tier golden prana dust & celestial particles floating at distinct depths
 * 3. Living, organic diya flame flickering on temple brass samai & hanging lamps
 * 4. Wisps of sacred agarbatti (incense) smoke rising from the puja thali
 * 5. Continuous golden coin cascade (Dhan Varsha) pouring from Maa's kalash
 * 6. Responsive coordinate projection mapping for 16:9 desktop & mobile viewports
 * 7. Burst particle effects for sacred transitions
 * ============================================================================
 */

class DivineEnvironmentComponent {
    constructor(canvasId = 'divineEnvCanvas') {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas ? this.canvas.getContext('2d', { alpha: true }) : null;

        this.isRunning = false;
        this.animFrameId = null;
        this.startTime = performance.now();

        // Particle Pools
        this.petals = [];
        this.coins = [];
        this.pranaSparks = [];
        this.smokeParticles = [];

        // Diya lamp locations (normalized to 16:9 rendered artwork)
        this.diyaLamps = [
            { id: 'leftSamai', nx: 0.155, ny: 0.552, size: 7.5, intensity: 1.0 },
            { id: 'rightSamai', nx: 0.852, ny: 0.552, size: 7.5, intensity: 1.0 },
            { id: 'leftHanging', nx: 0.328, ny: 0.152, size: 5.0, intensity: 0.75 },
            { id: 'rightHanging', nx: 0.672, ny: 0.152, size: 5.0, intensity: 0.75 },
            { id: 'centerDiya', nx: 0.335, ny: 0.865, size: 4.8, intensity: 0.85 }
        ];

        // Incense source location
        this.incenseSource = { nx: 0.312, ny: 0.855 };

        // Configuration
        this.counts = {
            petalsBg: 18,
            petalsMid: 36,
            petalsFg: 12,
            coins: 38,
            sparksBg: 35,
            sparksMid: 40,
            sparksFg: 15,
            smoke: 22
        };

        // Palette
        this.petalPalette = {
            rose: ['#B71C1C', '#C62828', '#D32F2F', '#E53935'],
            lotus: ['#E91E63', '#F06292', '#FF80AB', '#F8BBD0'],
            marigold: ['#FF8F00', '#FFA000', '#FFB300']
        };

        this.init();
    }

    init() {
        if (!this.canvas) {
            console.error('DivineEnvironmentComponent: Canvas not found.');
            return;
        }

        this.resize();
        window.addEventListener('resize', () => this.resize());

        // Respect reduced motion
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (prefersReducedMotion) {
            this.counts.petalsMid = 16;
            this.counts.petalsFg = 4;
            this.counts.coins = 16;
            this.counts.sparksMid = 18;
            this.counts.smoke = 10;
        }

        this.createPetalPool();
        this.createCoinPool();
        this.createSparksPool();
        this.createSmokePool();
    }

    resize() {
        if (!this.canvas) return;
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        this.canvas.width = window.innerWidth * dpr;
        this.canvas.height = window.innerHeight * dpr;
        this.canvas.style.width = `${window.innerWidth}px`;
        this.canvas.style.height = `${window.innerHeight}px`;
        if (this.ctx) {
            this.ctx.setTransform(1, 0, 0, 1, 0, 0);
            this.ctx.scale(dpr, dpr);
        }
    }

    /**
     * Accurately calculates the rendered bounding box of the 16:9 artwork on any viewport
     */
    getArtworkBounds() {
        const viewW = window.innerWidth;
        const viewH = window.innerHeight;
        const imgAspect = 16 / 9;
        const viewAspect = viewW / viewH;

        let renderW, renderH, offsetX, offsetY;

        if (viewAspect < 1.6) {
            // Mobile portrait or square screens: object-fit: contain ensures no cropping
            renderW = viewW;
            renderH = viewW / imgAspect;
            offsetX = 0;
            offsetY = (viewH - renderH) / 2;
        } else {
            // Desktop widescreen: object-fit: cover fills edge-to-edge
            if (viewAspect > imgAspect) {
                renderW = viewW;
                renderH = viewW / imgAspect;
                offsetX = 0;
                offsetY = (viewH - renderH) / 2;
            } else {
                renderH = viewH;
                renderW = viewH * imgAspect;
                offsetX = (viewW - renderW) / 2;
                offsetY = 0;
            }
        }

        return { renderW, renderH, offsetX, offsetY };
    }

    // =========================================================================
    // 1. PETAL POOL (3 Depth Layers)
    // =========================================================================
    createPetalPool() {
        this.petals = [];
        const allTypes = ['rose', 'rose', 'lotus', 'lotus', 'marigold'];

        // Layer 0: Background petals (distant, small, soft)
        for (let i = 0; i < this.counts.petalsBg; i++) {
            this.petals.push(this.spawnPetal('bg', allTypes[i % allTypes.length], true));
        }

        // Layer 1: Midground petals (temple floor / altar, crisp, natural tumble)
        for (let i = 0; i < this.counts.petalsMid; i++) {
            this.petals.push(this.spawnPetal('mid', allTypes[i % allTypes.length], true));
        }

        // Layer 2: Foreground petals (close to camera, large, soft bokeh)
        for (let i = 0; i < this.counts.petalsFg; i++) {
            this.petals.push(this.spawnPetal('fg', allTypes[i % allTypes.length], true));
        }
    }

    spawnPetal(depth = 'mid', type = 'rose', randomY = false) {
        const w = window.innerWidth;
        const h = window.innerHeight;
        const colors = this.petalPalette[type] || this.petalPalette.rose;
        const color = colors[Math.floor(Math.random() * colors.length)];

        let size, speedY, speedX, swayAmp, swayFreq, opacity, blur;

        if (depth === 'bg') {
            size = 6 + Math.random() * 5;
            speedY = 0.5 + Math.random() * 0.8;
            speedX = -0.2 + Math.random() * 0.6;
            swayAmp = 10 + Math.random() * 15;
            swayFreq = 0.015 + Math.random() * 0.015;
            opacity = 0.45 + Math.random() * 0.25;
            blur = 1.0;
        } else if (depth === 'fg') {
            size = 22 + Math.random() * 14;
            speedY = 1.6 + Math.random() * 1.8;
            speedX = -0.6 + Math.random() * 1.6;
            swayAmp = 28 + Math.random() * 40;
            swayFreq = 0.008 + Math.random() * 0.012;
            opacity = 0.85 + Math.random() * 0.15;
            blur = 2.0;
        } else {
            // Midground
            size = 11 + Math.random() * 9;
            speedY = 0.9 + Math.random() * 1.4;
            speedX = -0.4 + Math.random() * 1.0;
            swayAmp = 18 + Math.random() * 26;
            swayFreq = 0.012 + Math.random() * 0.018;
            opacity = 0.8 + Math.random() * 0.2;
            blur = 0;
        }

        return {
            depth,
            type,
            x: Math.random() * (w + 60) - 30,
            y: randomY ? Math.random() * h : -size - 10,
            size,
            color,
            speedY,
            speedX,
            swayAmp,
            swayFreq,
            opacity,
            blur,
            angle: Math.random() * Math.PI * 2,
            rotSpeed: -0.025 + Math.random() * 0.05,
            phase: Math.random() * Math.PI * 2
        };
    }

    // =========================================================================
    // 2. COIN CASCADE POOL (Dhan Varsha from Maa's Kalash)
    // =========================================================================
    createCoinPool() {
        this.coins = [];
        for (let i = 0; i < this.counts.coins; i++) {
            this.coins.push(this.spawnCoin(true));
        }
    }

    spawnCoin(randomInitialY = false) {
        const bounds = this.getArtworkBounds();
        // Exact location of the coin pot opening in the 16:9 masterwork
        const mouthX = bounds.offsetX + bounds.renderW * 0.536 + (Math.random() * 12 - 6);
        const mouthY = bounds.offsetY + bounds.renderH * 0.565 + (Math.random() * 10 - 5);
        const targetFloorY = bounds.offsetY + bounds.renderH * 0.91;

        const initialY = randomInitialY 
            ? mouthY + Math.random() * (targetFloorY - mouthY)
            : mouthY;

        return {
            x: mouthX,
            y: initialY,
            mouthX,
            mouthY,
            targetFloorY,
            radius: 5.5 + Math.random() * 4.5,
            vx: -0.6 + Math.random() * 1.5,
            vy: 1.8 + Math.random() * 3.2,
            gravity: 0.11,
            rot: Math.random() * Math.PI * 2,
            rotSpeed: 0.07 + Math.random() * 0.14,
            opacity: 0.9 + Math.random() * 0.1
        };
    }

    // =========================================================================
    // 3. CELESTIAL PRANA DUST (3-Tier Golden Light Particles)
    // =========================================================================
    createSparksPool() {
        this.pranaSparks = [];
        // Tier 1: Far background prana mist
        for (let i = 0; i < this.counts.sparksBg; i++) {
            this.pranaSparks.push(this.spawnSpark('bg'));
        }
        // Tier 2: Midground temple sparkles
        for (let i = 0; i < this.counts.sparksMid; i++) {
            this.pranaSparks.push(this.spawnSpark('mid'));
        }
        // Tier 3: Foreground luminous golden orbs
        for (let i = 0; i < this.counts.sparksFg; i++) {
            this.pranaSparks.push(this.spawnSpark('fg'));
        }
    }

    spawnSpark(depth = 'mid') {
        const w = window.innerWidth;
        const h = window.innerHeight;

        let size, vy, vx, baseAlpha, twinkleFreq;

        if (depth === 'bg') {
            size = 0.9 + Math.random() * 1.3;
            vy = -0.3 - Math.random() * 0.5;
            vx = -0.2 + Math.random() * 0.4;
            baseAlpha = 0.35;
            twinkleFreq = 0.02 + Math.random() * 0.03;
        } else if (depth === 'fg') {
            size = 3.5 + Math.random() * 3.5;
            vy = -0.6 - Math.random() * 0.9;
            vx = -0.4 + Math.random() * 0.8;
            baseAlpha = 0.7;
            twinkleFreq = 0.015 + Math.random() * 0.02;
        } else {
            // Midground
            size = 1.8 + Math.random() * 2.0;
            vy = -0.4 - Math.random() * 0.8;
            vx = -0.3 + Math.random() * 0.6;
            baseAlpha = 0.55;
            twinkleFreq = 0.025 + Math.random() * 0.04;
        }

        return {
            depth,
            x: Math.random() * w,
            y: Math.random() * h,
            vx,
            vy,
            size,
            baseAlpha,
            twinkleFreq,
            phase: Math.random() * Math.PI * 2
        };
    }

    // =========================================================================
    // 4. INCENSE SMOKE POOL
    // =========================================================================
    createSmokePool() {
        this.smokeParticles = [];
        for (let i = 0; i < this.counts.smoke; i++) {
            this.smokeParticles.push(this.spawnSmokeParticle(true));
        }
    }

    spawnSmokeParticle(randomY = false) {
        const bounds = this.getArtworkBounds();
        const originX = bounds.offsetX + bounds.renderW * this.incenseSource.nx;
        const originY = bounds.offsetY + bounds.renderH * this.incenseSource.ny;

        const maxRise = 180;
        const yOffset = randomY ? Math.random() * maxRise : 0;

        return {
            originX,
            originY,
            x: originX + (Math.random() * 4 - 2),
            y: originY - yOffset,
            radius: 3 + yOffset * 0.08,
            maxRadius: 18 + Math.random() * 8,
            growth: 0.07,
            vy: -0.6 - Math.random() * 0.5,
            vx: -0.15 + Math.random() * 0.35,
            swaySpeed: 0.02 + Math.random() * 0.02,
            swayAmp: 1.2,
            opacity: Math.max(0, 0.45 * (1 - yOffset / maxRise)),
            life: randomY ? 1 - yOffset / maxRise : 1,
            decay: 0.005 + Math.random() * 0.004
        };
    }

    // =========================================================================
    // ANIMATION CONTROL
    // =========================================================================
    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.startTime = performance.now();
        console.log('Divine Sanctum Environment Engine (4K Darshan) active.');
        this.renderLoop();
    }

    stop() {
        this.isRunning = false;
        if (this.animFrameId) {
            cancelAnimationFrame(this.animFrameId);
            this.animFrameId = null;
        }
    }

    renderLoop() {
        if (!this.isRunning || !this.ctx) return;

        const w = window.innerWidth;
        const h = window.innerHeight;
        const bounds = this.getArtworkBounds();
        const time = (performance.now() - this.startTime) * 0.001;

        this.ctx.clearRect(0, 0, w, h);

        // 1. Render Living Diya Lamp Flames & Warm Ambient Glow Pools
        this.renderDiyaFlames(bounds, time);

        // 2. Render Wisps of Sacred Agarbatti Incense Smoke
        this.renderIncenseSmoke(bounds);

        // 3. Render Dhan Varsha Gold Coin Shower (Pouring from Kalash)
        this.renderGoldCoins(bounds);

        // 4. Render Background & Midground Rose & Lotus Petals
        this.renderPetals(w, h, 'bg');
        this.renderPetals(w, h, 'mid');

        // 5. Render Celestial Prana Particles (Multi-depth)
        this.renderPranaSparks(w, h, time);

        // 6. Render Foreground Bokeh Petals (Closest to camera, ethereal drift)
        this.renderPetals(w, h, 'fg');

        this.animFrameId = requestAnimationFrame(() => this.renderLoop());
    }

    // =========================================================================
    // DIYA FLAME ENGINE (Natural Multi-Harmonic Organic Flame Physics)
    // =========================================================================
    renderDiyaFlames(bounds, time) {
        const ctx = this.ctx;

        for (const lamp of this.diyaLamps) {
            const lx = bounds.offsetX + bounds.renderW * lamp.nx;
            const ly = bounds.offsetY + bounds.renderH * lamp.ny;

            // Multi-harmonic natural flicker (avoids repetitive mechanical oscillation)
            const flicker = Math.sin(time * 16.3 + lamp.nx * 20) * 0.12
                          + Math.cos(time * 24.7 + lamp.ny * 15) * 0.07
                          + Math.sin(time * 38.1) * 0.04;

            const scale = (1.0 + flicker) * lamp.intensity;
            const flameW = lamp.size * scale;
            const flameH = lamp.size * 1.85 * scale;

            // 1. Ambient Warm Radial Illumination Pool (casts warm light on brass/marble)
            const poolRadius = lamp.size * 5.2 * scale;
            const poolGrad = ctx.createRadialGradient(lx, ly, 1, lx, ly, poolRadius);
            poolGrad.addColorStop(0, 'rgba(255, 190, 60, 0.32)');
            poolGrad.addColorStop(0.45, 'rgba(255, 120, 20, 0.12)');
            poolGrad.addColorStop(1, 'rgba(255, 90, 0, 0)');

            ctx.save();
            ctx.fillStyle = poolGrad;
            ctx.beginPath();
            ctx.arc(lx, ly, poolRadius, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            // 2. Outer Warm Saffron Flame Mantle
            ctx.save();
            ctx.translate(lx, ly);
            const sway = Math.sin(time * 12.0 + lamp.nx * 10) * 1.5;
            ctx.rotate((sway * Math.PI) / 180);

            // Flame teardrop bezier path
            ctx.beginPath();
            ctx.moveTo(0, -flameH);
            ctx.bezierCurveTo(flameW * 0.85, -flameH * 0.45, flameW * 0.9, flameH * 0.2, 0, flameH * 0.35);
            ctx.bezierCurveTo(-flameW * 0.9, flameH * 0.2, -flameW * 0.85, -flameH * 0.45, 0, -flameH);
            ctx.closePath();

            const flameGrad = ctx.createLinearGradient(0, -flameH, 0, flameH * 0.35);
            flameGrad.addColorStop(0, '#FFE082');
            flameGrad.addColorStop(0.4, '#FFB300');
            flameGrad.addColorStop(0.75, '#FF6F00');
            flameGrad.addColorStop(1, 'rgba(216, 67, 21, 0.6)');

            ctx.fillStyle = flameGrad;
            ctx.shadowColor = '#FFA000';
            ctx.shadowBlur = 10 * scale;
            ctx.fill();

            // 3. Inner White-Hot Radiant Core
            ctx.beginPath();
            const coreW = flameW * 0.45;
            const coreH = flameH * 0.55;
            ctx.moveTo(0, -coreH * 0.7);
            ctx.bezierCurveTo(coreW, -coreH * 0.2, coreW, coreH * 0.3, 0, coreH * 0.4);
            ctx.bezierCurveTo(-coreW, coreH * 0.3, -coreW, -coreH * 0.2, 0, -coreH * 0.7);
            ctx.closePath();

            const coreGrad = ctx.createLinearGradient(0, -coreH, 0, coreH * 0.4);
            coreGrad.addColorStop(0, '#FFFFFF');
            coreGrad.addColorStop(0.65, '#FFF9C4');
            coreGrad.addColorStop(1, '#FFD54F');
            ctx.fillStyle = coreGrad;
            ctx.shadowColor = '#FFFFFF';
            ctx.shadowBlur = 6;
            ctx.fill();

            ctx.restore();
        }
    }

    // =========================================================================
    // INCENSE SMOKE ENGINE (Soft Translucent Curves Drifting Upward)
    // =========================================================================
    renderIncenseSmoke(bounds) {
        const ctx = this.ctx;

        for (let i = 0; i < this.smokeParticles.length; i++) {
            const p = this.smokeParticles[i];
            p.y += p.vy;
            p.x += p.vx + Math.sin(p.y * p.swaySpeed) * p.swayAmp;
            p.radius += p.growth;
            p.life -= p.decay;

            if (p.life <= 0 || p.radius >= p.maxRadius) {
                this.smokeParticles[i] = this.spawnSmokeParticle(false);
                continue;
            }

            const alpha = p.life * p.opacity;
            ctx.save();
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            const grad = ctx.createRadialGradient(p.x, p.y, 1, p.x, p.y, p.radius);
            grad.addColorStop(0, `rgba(235, 230, 220, ${alpha * 0.6})`);
            grad.addColorStop(0.5, `rgba(210, 200, 190, ${alpha * 0.25})`);
            grad.addColorStop(1, 'rgba(200, 190, 180, 0)');
            ctx.fillStyle = grad;
            ctx.fill();
            ctx.restore();
        }
    }

    // =========================================================================
    // DHAN VARSHA GOLD COINS ENGINE (Realistic 3D Tumbling & Specular Glints)
    // =========================================================================
    renderGoldCoins(bounds) {
        const ctx = this.ctx;

        for (let i = 0; i < this.coins.length; i++) {
            const c = this.coins[i];
            c.vy += c.gravity;
            c.x += c.vx;
            c.y += c.vy;
            c.rot += c.rotSpeed;

            // When reaching the golden treasure pile
            if (c.y >= c.targetFloorY) {
                this.coins[i] = this.spawnCoin(false);
                continue;
            }

            ctx.save();
            ctx.translate(c.x, c.y);
            const flip = Math.cos(c.rot);
            ctx.scale(1, flip);

            // Shimmering 3D Gold Coin Disc
            ctx.beginPath();
            ctx.arc(0, 0, c.radius, 0, Math.PI * 2);

            const coinGrad = ctx.createRadialGradient(
                -c.radius * 0.35, -c.radius * 0.35, 1,
                0, 0, c.radius
            );
            coinGrad.addColorStop(0, '#FFFDE7');
            coinGrad.addColorStop(0.4, '#FFD700');
            coinGrad.addColorStop(0.8, '#C68E17');
            coinGrad.addColorStop(1, '#FFE082');

            ctx.fillStyle = coinGrad;
            ctx.shadowColor = 'rgba(255, 193, 7, 0.45)';
            ctx.shadowBlur = 5;
            ctx.fill();

            // Inner coin relief rim
            ctx.strokeStyle = 'rgba(160, 110, 20, 0.75)';
            ctx.lineWidth = 1;
            ctx.stroke();

            // Specular light reflection on rotation
            if (Math.sin(c.rot * 2.5) > 0.88) {
                ctx.fillStyle = '#FFFFFF';
                ctx.beginPath();
                ctx.arc(c.radius * 0.35, -c.radius * 0.35, 2.2, 0, Math.PI * 2);
                ctx.fill();
            }

            ctx.restore();
        }
    }

    // =========================================================================
    // PETALS ENGINE (Swaying in Temple Breeze with 3D Tumble)
    // =========================================================================
    renderPetals(w, h, targetDepth) {
        const ctx = this.ctx;

        for (let i = 0; i < this.petals.length; i++) {
            const p = this.petals[i];
            if (p.depth !== targetDepth) continue;

            p.y += p.speedY;
            p.x += p.speedX + Math.sin(p.y * p.swayFreq + p.phase) * (p.swayAmp * 0.05);
            p.angle += p.rotSpeed;
            const scaleX = Math.abs(Math.cos(p.angle * 1.3));

            if (p.y > h + 30) {
                const totalBase = this.counts.petalsBg + this.counts.petalsMid + this.counts.petalsFg;
                if (this.petals.length > totalBase) {
                    this.petals.splice(i, 1);
                    i--;
                } else {
                    this.petals[i] = this.spawnPetal(p.depth, p.type, false);
                }
                continue;
            }
            if (p.x > w + 40) p.x = -30;
            if (p.x < -40) p.x = w + 30;

            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.angle);
            ctx.scale(scaleX, 1);
            ctx.globalAlpha = p.opacity;

            // Organic curved petal silhouette
            ctx.beginPath();
            ctx.moveTo(0, -p.size);
            ctx.bezierCurveTo(p.size * 0.75, -p.size * 0.7, p.size * 0.75, p.size * 0.5, 0, p.size);
            ctx.bezierCurveTo(-p.size * 0.75, p.size * 0.5, -p.size * 0.75, -p.size * 0.7, 0, -p.size);
            ctx.closePath();

            ctx.fillStyle = p.color;
            if (p.depth === 'fg') {
                ctx.shadowColor = 'rgba(255, 100, 0, 0.4)';
                ctx.shadowBlur = 10;
            } else {
                ctx.shadowColor = 'rgba(180, 40, 20, 0.25)';
                ctx.shadowBlur = 4;
            }
            ctx.fill();

            // Subtle petal center vein
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
            ctx.lineWidth = 0.8;
            ctx.beginPath();
            ctx.moveTo(0, -p.size * 0.7);
            ctx.lineTo(0, p.size * 0.7);
            ctx.stroke();

            ctx.restore();
        }
    }

    // =========================================================================
    // PRANA SPARKS ENGINE (3-Tier Floating Golden Atmospheric Orbs)
    // =========================================================================
    renderPranaSparks(w, h, time) {
        const ctx = this.ctx;

        for (let i = 0; i < this.pranaSparks.length; i++) {
            const s = this.pranaSparks[i];
            s.y += s.vy;
            s.x += s.vx;
            s.phase += s.twinkleFreq;

            if (s.y < -20) {
                s.y = h + 10;
                s.x = Math.random() * w;
            }
            if (s.x < -20) s.x = w + 10;
            if (s.x > w + 20) s.x = -10;

            const twinkle = (Math.sin(s.phase) * 0.5 + 0.5);
            const alpha = s.baseAlpha * (0.6 + 0.4 * twinkle);

            ctx.save();
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);

            if (s.depth === 'fg') {
                // Luminous Golden Bokeh Orb with Gradient
                const orbGrad = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, s.size);
                orbGrad.addColorStop(0, `rgba(255, 255, 220, ${alpha})`);
                orbGrad.addColorStop(0.5, `rgba(255, 215, 0, ${alpha * 0.6})`);
                orbGrad.addColorStop(1, 'rgba(255, 170, 0, 0)');
                ctx.fillStyle = orbGrad;
            } else {
                ctx.fillStyle = `rgba(255, 225, 120, ${alpha})`;
                ctx.shadowColor = '#FFD700';
                ctx.shadowBlur = s.size * 2.5;
            }
            ctx.fill();
            ctx.restore();
        }
    }

    /**
     * Flower Shower Burst for celebration / Aarti milestones
     */
    spawnFlowerBurst(x, y, count = 35) {
        const allTypes = ['rose', 'lotus', 'marigold'];
        for (let i = 0; i < count; i++) {
            const angle = Math.random() * Math.PI * 2;
            const velocity = 2.5 + Math.random() * 5.0;
            const type = allTypes[Math.floor(Math.random() * allTypes.length)];
            const colors = this.petalPalette[type];

            this.petals.push({
                depth: 'mid',
                type,
                x,
                y,
                size: 14 + Math.random() * 10,
                color: colors[Math.floor(Math.random() * colors.length)],
                speedX: Math.cos(angle) * velocity,
                speedY: Math.sin(angle) * velocity - 1.5,
                swayAmp: 20,
                swayFreq: 0.015,
                opacity: 1.0,
                angle: Math.random() * Math.PI * 2,
                rotSpeed: -0.06 + Math.random() * 0.12,
                phase: Math.random() * Math.PI * 2
            });
        }
    }
}

window.DivineEnvironmentComponent = DivineEnvironmentComponent;
