/**
 * ============================================================================
 * PHASE 4 & 5: INTERACTIVE AARTI & FINAL BLESSINGS ENGINE
 * 
 * - Traditional Ornate Aarti Thali with dynamic multi-wick illumination
 * - Real-time camera hand tracking via MediaPipe Hands & in-browser CV fallback
 * - Natural flame aerodynamics with velocity inertia and responsive tilt
 * - Clockwise circular parikrama round tracking (0 to 7) around Maa Lakshmi
 * - Resonant temple bell chimes at every quarter turn and full round
 * - Phase 5 Final Blessings transition with Shankh Naad, flower burst,
 *   spoken Hindi blessing voiceover, and radiant divine blessings card
 * ============================================================================
 */

class AartiInteractionComponent {
    constructor(options = {}) {
        this.thali = document.getElementById('aartiThali');
        this.kapoorFlame = this.thali ? this.thali.querySelector('.thali-flame-kapoor') : null;
        this.sanctum = document.getElementById('sanctumSanctorum');
        
        // Webcam elements
        this.camVideo = document.getElementById('camVideo');
        this.camViewBox = document.getElementById('camViewBox');
        this.camOverlay = document.getElementById('camOverlayCanvas');
        this.camOverlayCtx = this.camOverlay ? this.camOverlay.getContext('2d') : null;
        this.camToggleBtn = document.getElementById('camToggleBtn');
        this.autoAartiBtn = document.getElementById('autoAartiBtn');
        this.restartAartiBtn = document.getElementById('btnRestartAarti');

        // Audio & State references
        this.aartiRoundText = document.getElementById('aartiRoundText');
        this.blessingModal = document.getElementById('finalBlessingsModal');
        this.environmentComponent = options.environment || window.appEnvironment || null;
        this.player = options.player || window.appAartiPlayer || null;
        this.shankhAudio = document.getElementById('shankhAudio');

        // Offscreen CV canvas for zero-dependency local browser hand tracking
        this.cvCanvas = document.createElement('canvas');
        this.cvCanvas.width = 160;
        this.cvCanvas.height = 120;
        this.cvCtx = this.cvCanvas.getContext('2d', { willReadFrequently: true });

        // Motion physics & tracking states
        this.thaliX = window.innerWidth / 2;
        this.thaliY = window.innerHeight * 0.72;
        this.targetX = this.thaliX;
        this.targetY = this.thaliY;
        this.prevThaliX = this.thaliX;
        this.prevThaliY = this.thaliY;

        this.isCameraActive = false;
        this.mediaStream = null;
        this.mpHands = null;
        this.mpCamera = null;

        this.isAutoAarti = false;
        this.autoAngle = 0;

        // Aarti round tracking
        this.prevAngle = null;
        this.cumulativeAngle = 0;
        this.completedRounds = 0;
        this.maxRounds = 7;
        this.isBlessingActive = false;

        this.audioContext = null;

        this.init();
    }

    init() {
        this.centerThali();
        this.setupEventListeners();
        requestAnimationFrame(() => this.updateLoop());
    }

    getArtworkCenter() {
        const viewW = window.innerWidth;
        const viewH = window.innerHeight;
        const imgAspect = 16 / 9;
        const viewAspect = viewW / viewH;

        let centerX = viewW / 2;
        let centerY;

        if (viewAspect < 1.6) {
            // Mobile portrait: object-fit contain
            const renderH = viewW / imgAspect;
            const offsetY = (viewH - renderH) / 2;
            centerY = offsetY + renderH * 0.44;
        } else {
            // Desktop widescreen: object-fit cover
            centerY = viewH * 0.44;
        }

        return { centerX, centerY };
    }

    centerThali() {
        const { centerX, centerY } = this.getArtworkCenter();
        this.thaliX = centerX;
        this.thaliY = Math.min(window.innerHeight * 0.78, centerY + 180);
        this.targetX = this.thaliX;
        this.targetY = this.thaliY;
        if (this.thali) {
            this.thali.style.left = `${this.thaliX}px`;
            this.thali.style.top = `${this.thaliY}px`;
        }
    }

    setupEventListeners() {
        // 1. Fluid Full-Viewport Mouse Tracking
        window.addEventListener('mousemove', (e) => {
            if (this.sanctum && this.sanctum.classList.contains('active') && !this.isAutoAarti && !this.isCameraActive && !this.isBlessingActive) {
                this.targetX = e.clientX;
                this.targetY = e.clientY;
                this.trackCircularMotion(this.targetX, this.targetY);
            }
        });

        // 2. Fluid Full-Viewport Touch Tracking (Mobile & Tablet)
        window.addEventListener('touchmove', (e) => {
            if (this.sanctum && this.sanctum.classList.contains('active') && !this.isAutoAarti && !this.isCameraActive && !this.isBlessingActive && e.touches.length > 0) {
                this.targetX = e.touches[0].clientX;
                this.targetY = e.touches[0].clientY;
                this.trackCircularMotion(this.targetX, this.targetY);
            }
        }, { passive: true });

        // 3. UI Buttons
        if (this.camToggleBtn) {
            this.camToggleBtn.addEventListener('click', () => this.toggleCamera());
        }
        if (this.autoAartiBtn) {
            this.autoAartiBtn.addEventListener('click', () => this.toggleAutoAarti());
        }
        if (this.restartAartiBtn) {
            this.restartAartiBtn.addEventListener('click', () => this.closeBlessingModal());
        }
    }

    getAudioContext() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }
        return this.audioContext;
    }

    playBellChime(freq = 920, duration = 3.2) {
        try {
            const ctx = this.getAudioContext();
            const now = ctx.currentTime;
            const partials = [
                { f: freq * 1.0, g: 0.3, d: duration },
                { f: freq * 1.5, g: 0.16, d: duration * 0.75 },
                { f: freq * 2.76, g: 0.12, d: duration * 0.5 },
                { f: freq * 4.07, g: 0.06, d: duration * 0.3 }
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
            console.warn('Bell chime notice:', e);
        }
    }

    showThali() {
        if (this.thali) {
            this.thali.style.display = 'block';
            this.centerThali();
        }
    }

    hideThali() {
        if (this.thali) {
            this.thali.style.display = 'none';
        }
        this.stopCamera();
    }

    /**
     * Toggles Camera Hand Tracking
     * Requests permission only when clicked. Zero footage uploaded to any server.
     */
    async toggleCamera() {
        if (!this.isCameraActive) {
            try {
                this.mediaStream = await navigator.mediaDevices.getUserMedia({
                    video: { width: 320, height: 240, facingMode: 'user' }
                });
                
                if (this.camVideo) {
                    this.camVideo.srcObject = this.mediaStream;
                }
                if (this.camViewBox) {
                    this.camViewBox.style.display = 'block';
                }

                this.isCameraActive = true;
                if (this.camToggleBtn) {
                    this.camToggleBtn.textContent = '📷 Stop Camera';
                    this.camToggleBtn.classList.add('btn-cam-active');
                }

                if (this.camOverlay) {
                    this.camOverlay.width = 180;
                    this.camOverlay.height = 135;
                }

                console.log('Phase 4: Camera hand tracking activated locally in browser.');

                // Check MediaPipe Hands availability
                if (typeof window.Hands !== 'undefined' && !this.mpHands) {
                    this.initMediaPipeHands();
                } else {
                    requestAnimationFrame(() => this.processWebcamFrame());
                }
            } catch (err) {
                console.error('Camera access error:', err);
                alert("Camera permission was not granted. You can still perform Aarti smoothly with your Mouse or Touch!");
            }
        } else {
            this.stopCamera();
        }
    }

    stopCamera() {
        if (this.mediaStream) {
            this.mediaStream.getTracks().forEach(track => track.stop());
            this.mediaStream = null;
        }
        if (this.camViewBox) {
            this.camViewBox.style.display = 'none';
        }
        this.isCameraActive = false;
        if (this.camToggleBtn) {
            this.camToggleBtn.textContent = '📷 Hand Gesture Aarti';
            this.camToggleBtn.classList.remove('btn-cam-active');
        }
    }

    initMediaPipeHands() {
        try {
            this.mpHands = new window.Hands({
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
            });
            this.mpHands.setOptions({
                maxNumHands: 1,
                modelComplexity: 0,
                minDetectionConfidence: 0.5,
                minTrackingConfidence: 0.5
            });

            this.mpHands.onResults((results) => {
                if (!this.isCameraActive) return;

                if (this.camOverlayCtx) {
                    this.camOverlayCtx.clearRect(0, 0, this.camOverlay.width, this.camOverlay.height);
                }

                if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
                    const landmarks = results.multiHandLandmarks[0];
                    // Landmark 9: Middle finger MCP (palm center)
                    const palm = landmarks[9];

                    // Mirror X coordinate because camera is mirrored
                    const normX = 1.0 - palm.x;
                    const normY = palm.y;

                    this.targetX = normX * window.innerWidth;
                    this.targetY = normY * window.innerHeight;

                    this.trackCircularMotion(this.targetX, this.targetY);

                    // Draw hand indicator on PiP overlay
                    if (this.camOverlayCtx) {
                        const pipX = (1.0 - normX) * this.camOverlay.width;
                        const pipY = normY * this.camOverlay.height;

                        this.camOverlayCtx.strokeStyle = '#00FF66';
                        this.camOverlayCtx.lineWidth = 2.5;
                        this.camOverlayCtx.beginPath();
                        this.camOverlayCtx.arc(pipX, pipY, 16, 0, Math.PI * 2);
                        this.camOverlayCtx.stroke();

                        this.camOverlayCtx.fillStyle = '#FFD700';
                        this.camOverlayCtx.beginPath();
                        this.camOverlayCtx.arc(pipX, pipY, 5, 0, Math.PI * 2);
                        this.camOverlayCtx.fill();
                    }
                }
            });

            // Feed camera frames into MediaPipe
            const sendFrame = async () => {
                if (this.isCameraActive && this.camVideo && this.camVideo.readyState >= 2) {
                    await this.mpHands.send({ image: this.camVideo });
                }
                if (this.isCameraActive) {
                    requestAnimationFrame(sendFrame);
                }
            };
            sendFrame();
        } catch (e) {
            console.warn('MediaPipe init note, using local CV engine:', e);
            requestAnimationFrame(() => this.processWebcamFrame());
        }
    }

    /**
     * Local Zero-Dependency Computer Vision Fallback (Skin-Chroma Centroid Tracking)
     */
    processWebcamFrame() {
        if (!this.isCameraActive || !this.camVideo) return;

        if (this.camVideo.readyState === this.camVideo.HAVE_ENOUGH_DATA) {
            const cw = this.cvCanvas.width;
            const ch = this.cvCanvas.height;

            this.cvCtx.drawImage(this.camVideo, 0, 0, cw, ch);
            const frameData = this.cvCtx.getImageData(0, 0, cw, ch);
            const pixels = frameData.data;

            let sumX = 0, sumY = 0, count = 0;

            for (let i = 0; i < pixels.length; i += 4) {
                const r = pixels[i];
                const g = pixels[i + 1];
                const b = pixels[i + 2];

                if (r > 95 && g > 40 && b > 20 &&
                    (r - g) > 15 && r > g && r > b) {
                    const idx = i / 4;
                    sumX += idx % cw;
                    sumY += Math.floor(idx / cw);
                    count++;
                }
            }

            if (this.camOverlayCtx) {
                this.camOverlayCtx.clearRect(0, 0, this.camOverlay.width, this.camOverlay.height);
            }

            if (count > 70) {
                const cx = sumX / count;
                const cy = sumY / count;

                const normX = 1.0 - (cx / cw);
                const normY = cy / ch;

                this.targetX = normX * window.innerWidth;
                this.targetY = normY * window.innerHeight;

                this.trackCircularMotion(this.targetX, this.targetY);

                if (this.camOverlayCtx) {
                    const pipX = (1.0 - normX) * this.camOverlay.width;
                    const pipY = normY * this.camOverlay.height;

                    this.camOverlayCtx.strokeStyle = '#00FF66';
                    this.camOverlayCtx.lineWidth = 2;
                    this.camOverlayCtx.beginPath();
                    this.camOverlayCtx.arc(pipX, pipY, 15, 0, Math.PI * 2);
                    this.camOverlayCtx.stroke();

                    this.camOverlayCtx.fillStyle = '#FFD700';
                    this.camOverlayCtx.beginPath();
                    this.camOverlayCtx.arc(pipX, pipY, 4, 0, Math.PI * 2);
                    this.camOverlayCtx.fill();
                }
            }
        }

        if (!this.mpHands && this.isCameraActive) {
            requestAnimationFrame(() => this.processWebcamFrame());
        }
    }

    toggleAutoAarti() {
        this.isAutoAarti = !this.isAutoAarti;
        if (this.autoAartiBtn) {
            this.autoAartiBtn.textContent = this.isAutoAarti ? '⏸ Pause Aarti' : '▶ Auto Aarti';
            if (this.isAutoAarti) {
                this.autoAartiBtn.style.background = 'linear-gradient(135deg, #FFF176 0%, #FFD700 50%, #FFA000 100%)';
            } else {
                this.autoAartiBtn.style.background = '';
            }
        }
    }

    /**
     * Detects sacred clockwise circular motion around Maa Lakshmi's center
     */
    trackCircularMotion(x, y) {
        if (this.isBlessingActive) return;

        const { centerX, centerY } = this.getArtworkCenter();
        const dist = Math.hypot(x - centerX, y - centerY);
        if (dist < 40) {
            // Must have reasonable radius to form a true parikrama
            return;
        }

        const angle = Math.atan2(y - centerY, x - centerX);

        if (this.prevAngle !== null) {
            let delta = angle - this.prevAngle;
            if (delta > Math.PI) delta -= 2 * Math.PI;
            if (delta < -Math.PI) delta += 2 * Math.PI;

            // Clockwise rotation (positive delta)
            if (delta > 0) {
                const prevCumulative = this.cumulativeAngle;
                this.cumulativeAngle += delta;

                // Resonant bell chime every quarter turn (90 degrees / PI/2)
                const quarterPrev = Math.floor(prevCumulative / (Math.PI / 2));
                const quarterCur = Math.floor(this.cumulativeAngle / (Math.PI / 2));
                if (quarterCur > quarterPrev) {
                    this.playBellChime(960 + (quarterCur % 4) * 80, 2.6);
                }

                // Full 360 degree circle completed (with floating-point roundoff tolerance)
                if (this.cumulativeAngle >= (2 * Math.PI - 0.04)) {
                    this.cumulativeAngle = Math.max(0, this.cumulativeAngle - 2 * Math.PI);
                    this.completedRounds++;

                    if (this.aartiRoundText) {
                        this.aartiRoundText.textContent = `Aarti Rounds: ${this.completedRounds} / ${this.maxRounds}`;
                    }

                    this.playBellChime(1180, 4.2);

                    // Celebrate full round with flower shower burst
                    if (this.environmentComponent && typeof this.environmentComponent.spawnFlowerBurst === 'function') {
                        this.environmentComponent.spawnFlowerBurst(centerX, centerY, 35);
                    }

                    // Complete Phase 4 -> Trigger Phase 5 Final Blessings
                    if (this.completedRounds >= this.maxRounds) {
                        this.triggerFinalBlessings();
                    }
                }
            } else if (delta < 0) {
                // If moving counter-clockwise, unwind cumulative angle gracefully
                this.cumulativeAngle = Math.max(0, this.cumulativeAngle + delta * 0.5);
            }
        }
        this.prevAngle = angle;
    }

    /**
     * PHASE 5: FINAL BLESSINGS TRANSITION
     */
    triggerFinalBlessings() {
        this.isBlessingActive = true;
        this.isAutoAarti = false;
        this.stopCamera();
        if (this.autoAartiBtn) {
            this.autoAartiBtn.textContent = '▶ Auto Aarti';
            this.autoAartiBtn.style.background = '';
        }
        console.log('Phase 5: Aarti completed (7 rounds). Triggering Final Divine Blessings.');

        // 1. Play Shankh Naad & Temple Bells (duck background bhajan gently)
        if (this.player && this.player.audioElement) {
            this.savedVolume = this.player.audioElement.volume;
            this.player.audioElement.volume = Math.min(this.savedVolume, 0.22);
        }
        if (this.shankhAudio) {
            this.shankhAudio.currentTime = 0;
            this.shankhAudio.play().catch(e => console.log('Shankh note:', e));
        }
        this.playBellChime(540, 6.0);

        // 2. Large Celebratory Flower Shower Burst
        const { centerX, centerY } = this.getArtworkCenter();
        if (this.environmentComponent && typeof this.environmentComponent.spawnFlowerBurst === 'function') {
            this.environmentComponent.spawnFlowerBurst(centerX, centerY, 85);
        }

        // 3. Spoken Divine Hindi Blessing Voiceover with Natural Female Register
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            const text = "सदा सुखी रहो, तुम्हारे घर में सुख, शांति और समृद्धि का वास हो। शुभ दीपावली।";
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'hi-IN';
            utterance.rate = 0.84;
            utterance.pitch = 1.05;

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
            window.speechSynthesis.speak(utterance);
        }

        // 4. Reveal Final Blessings Modal
        if (this.blessingModal) {
            this.blessingModal.classList.add('active');
        }
    }

    closeBlessingModal() {
        if (this.blessingModal) {
            this.blessingModal.classList.remove('active');
        }
        if (this.player && this.player.audioElement && this.savedVolume !== undefined) {
            this.player.audioElement.volume = this.savedVolume;
        }
        this.isBlessingActive = false;
        this.completedRounds = 0;
        this.cumulativeAngle = 0;
        this.prevAngle = null;
        if (this.aartiRoundText) {
            this.aartiRoundText.textContent = `Aarti Rounds: 0 / ${this.maxRounds}`;
        }
        this.centerThali();
    }

    /**
     * 60 FPS Animation Loop: Lerp, Flame Aerodynamics, Velocity Tilt
     */
    updateLoop() {
        if (this.isAutoAarti && !this.isBlessingActive) {
            const { centerX, centerY } = this.getArtworkCenter();
            const rx = Math.min(window.innerWidth * 0.28, 260);
            const ry = Math.min(window.innerHeight * 0.20, 180);

            this.autoAngle += 0.024;
            this.targetX = centerX + Math.cos(this.autoAngle) * rx;
            this.targetY = centerY + Math.sin(this.autoAngle) * ry;

            this.trackCircularMotion(this.targetX, this.targetY);
        }

        // Smooth Lerp Damping
        const vx = this.targetX - this.thaliX;
        const vy = this.targetY - this.thaliY;
        this.thaliX += vx * 0.22;
        this.thaliY += vy * 0.22;

        if (this.thali) {
            this.thali.style.left = `${this.thaliX}px`;
            this.thali.style.top = `${this.thaliY}px`;
        }

        // Natural flame aerodynamic tilt with velocity inertia
        if (this.kapoorFlame) {
            const tilt = Math.max(-18, Math.min(18, -vx * 0.55));
            this.kapoorFlame.style.transform = `scale(1.12) rotate(${tilt}deg)`;
        }

        requestAnimationFrame(() => this.updateLoop());
    }
}

window.AartiInteractionComponent = AartiInteractionComponent;
