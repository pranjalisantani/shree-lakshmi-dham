/**
 * ============================================================================
 * PHASE 2: TEMPLE CURTAINS & CINEMATIC DARSHAN REVEAL CONTROLLER
 * Uses GSAP timeline-based animation to orchestrate the smooth parting of
 * luxurious red silk curtains, synchronized with natural devotional Hindi
 * voiceover, sacred Shankh Naad, golden light leaks, and particle bursts.
 * ============================================================================
 */

class TempleCurtainsComponent {
    constructor(options = {}) {
        this.curtainsContainer = document.getElementById('templeCurtainsStage');
        this.leftCurtain = document.getElementById('curtainLeft');
        this.rightCurtain = document.getElementById('curtainRight');
        this.lightLeak = document.getElementById('curtainLightLeak');
        this.curtainCanvas = document.getElementById('curtainFxCanvas');
        this.sanctumSanctorum = document.getElementById('sanctumSanctorum');
        this.shankhAudio = document.getElementById('shankhAudio');

        this.onRevealComplete = options.onRevealComplete || null;

        // State guards: Exactly once execution, prevent accidental re-triggers
        this.isTransitioning = false;
        this.isRevealed = false;

        this.particles = [];
        this.animFrameId = null;
        this.audioContext = null;

        this.init();
    }

    init() {
        if (this.curtainCanvas) {
            this.resizeCanvas();
            window.addEventListener('resize', () => this.resizeCanvas());
        }
    }

    resizeCanvas() {
        if (this.curtainCanvas) {
            this.curtainCanvas.width = window.innerWidth;
            this.curtainCanvas.height = window.innerHeight;
        }
    }

    /**
     * Initializes or resumes Web Audio Context upon user interaction
     */
    getAudioContext() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }
        return this.audioContext;
    }

    /**
     * Plays authentic resonant temple bell partials
     */
    playTempleBell(freq = 864, duration = 3.6) {
        try {
            const ctx = this.getAudioContext();
            const now = ctx.currentTime;
            const partials = [
                { f: freq * 1.0,  g: 0.35, d: duration },
                { f: freq * 1.5,  g: 0.18, d: duration * 0.8 },
                { f: freq * 2.76, g: 0.15, d: duration * 0.6 },
                { f: freq * 4.07, g: 0.08, d: duration * 0.4 },
            ];

            partials.forEach(p => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(p.f, now);

                gain.gain.setValueAtTime(0, now);
                gain.gain.linearRampToValueAtTime(p.g, now + 0.015);
                gain.gain.exponentialRampToValueAtTime(0.0001, now + p.d);

                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + p.d);
            });
        } catch (e) {
            console.warn('Temple bell audio warning:', e);
        }
    }

    /**
     * Speaks the sacred Hindi voiceover with peaceful, natural devotional female tone
     */
    playDevotionalVoiceover() {
        if (!('speechSynthesis' in window)) return;

        window.speechSynthesis.cancel();
        const text = "आइए, माँ की आरती आरंभ करें।";
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'hi-IN';
        utterance.rate = 0.84; // Peaceful, deliberate devotional tempo
        utterance.pitch = 1.05; // Gentle, reverent female register

        // Select the most natural Hindi female voice available
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => 
            v.lang.startsWith('hi') && (
                v.name.includes('Natural') || 
                v.name.includes('Swara') || 
                v.name.includes('Kalpana') || 
                v.name.includes('Google') || 
                v.name.includes('Heera') ||
                v.name.includes('Female')
            )
        ) || voices.find(v => v.lang.startsWith('hi'));

        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }

        // Slight breathing gap before sacred voice speaks
        setTimeout(() => {
            window.speechSynthesis.speak(utterance);
        }, 450);
    }

    /**
     * Emits a burst of sparkling golden prana particles along the parting seam
     */
    spawnGoldenCurtainBurst() {
        const cx = window.innerWidth / 2;
        const count = 75;
        for (let i = 0; i < count; i++) {
            this.particles.push({
                x: cx + (Math.random() * 30 - 15),
                y: Math.random() * window.innerHeight,
                vx: (Math.random() - 0.5) * 5.0,
                vy: (Math.random() - 0.5) * 3.5 - 1.2,
                size: 2 + Math.random() * 4.5,
                alpha: 1.0,
                decay: 0.012 + Math.random() * 0.018,
                color: Math.random() > 0.3 ? '#FFD700' : '#FFF59D'
            });
        }

        if (!this.animFrameId) {
            this.renderParticleBurst();
        }
    }

    renderParticleBurst() {
        if (!this.curtainCanvas) return;
        const ctx = this.curtainCanvas.getContext('2d');
        ctx.clearRect(0, 0, this.curtainCanvas.width, this.curtainCanvas.height);

        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.alpha -= p.decay;

            if (p.alpha <= 0) {
                this.particles.splice(i, 1);
                continue;
            }

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = p.alpha;
            ctx.shadowColor = '#FFA000';
            ctx.shadowBlur = 8;
            ctx.fill();
        }
        ctx.globalAlpha = 1.0;

        if (this.particles.length > 0) {
            this.animFrameId = requestAnimationFrame(() => this.renderParticleBurst());
        } else {
            this.animFrameId = null;
            ctx.clearRect(0, 0, this.curtainCanvas.width, this.curtainCanvas.height);
        }
    }

    /**
     * Executes the GSAP Timeline-based Curtain Opening
     */
    openCurtains(onCompleteCallback) {
        if (this.isTransitioning || this.isRevealed) return;
        this.isTransitioning = true;

        console.log('Phase 2: Executing GSAP Timeline Curtain Opening...');

        // 1. Play Shankh Naad & Temple Bell
        if (this.shankhAudio) {
            this.shankhAudio.currentTime = 0;
            this.shankhAudio.play().catch(e => console.warn('Shankh audio notice:', e));
        }
        this.playTempleBell(540, 5.0);

        // 2. Play Devotional Voiceover
        this.playDevotionalVoiceover();

        // Check if user prefers reduced motion
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        const duration = prefersReducedMotion ? 0.8 : 2.5;

        // Check for GSAP availability
        if (typeof gsap !== 'undefined') {
            const tl = gsap.timeline({
                onComplete: () => {
                    this.isTransitioning = false;
                    this.isRevealed = true;
                    if (this.sanctumSanctorum) {
                        this.sanctumSanctorum.classList.add('active');
                    }
                    if (typeof onCompleteCallback === 'function') {
                        onCompleteCallback();
                    }
                    if (typeof this.onRevealComplete === 'function') {
                        this.onRevealComplete();
                    }
                }
            });

            // Step A: Golden light leak intensifies between closed curtains
            tl.to(this.lightLeak, {
                opacity: 1,
                scaleX: 2.2,
                duration: 0.6,
                ease: 'power2.in'
            });

            // Step B: Curtains begin slow, luxurious parting with subtle cloth wave
            tl.add(() => {
                this.spawnGoldenCurtainBurst();
            }, "-=0.2");

            tl.to(this.leftCurtain, {
                xPercent: -100,
                duration: duration,
                ease: 'power3.inOut'
            }, "curtainOpen");

            tl.to(this.rightCurtain, {
                xPercent: 100,
                duration: duration,
                ease: 'power3.inOut'
            }, "curtainOpen");

            // Step C: Light leak spreads and fades as sanctum emerges
            tl.to(this.lightLeak, {
                opacity: 0,
                scaleX: 8.0,
                duration: 1.2,
                ease: 'power1.out'
            }, "-=1.4");

            // Step D: Sanctum Sanctorum cross-fades into full glorious darshan
            tl.to(this.sanctumSanctorum, {
                opacity: 1,
                duration: 1.5,
                ease: 'power2.out'
            }, "-=1.6");

        } else {
            // High-fidelity fallback if GSAP CDN is loading/unavailable
            this.lightLeak.style.opacity = '1';
            this.spawnGoldenCurtainBurst();
            this.leftCurtain.style.transition = `transform ${duration}s cubic-bezier(0.77, 0, 0.175, 1)`;
            this.rightCurtain.style.transition = `transform ${duration}s cubic-bezier(0.77, 0, 0.175, 1)`;
            this.leftCurtain.style.transform = 'translateX(-100%)';
            this.rightCurtain.style.transform = 'translateX(100%)';

            setTimeout(() => {
                this.lightLeak.style.opacity = '0';
                if (this.sanctumSanctorum) {
                    this.sanctumSanctorum.classList.add('active');
                    this.sanctumSanctorum.style.opacity = '1';
                }
                this.isTransitioning = false;
                this.isRevealed = true;
                if (typeof onCompleteCallback === 'function') {
                    onCompleteCallback();
                }
                if (typeof this.onRevealComplete === 'function') {
                    this.onRevealComplete();
                }
            }, duration * 1000);
        }
    }
}

window.TempleCurtainsComponent = TempleCurtainsComponent;
