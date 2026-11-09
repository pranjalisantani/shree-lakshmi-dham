/**
 * PHASE 1: WELCOME SCREEN CONTROLLER
 * Manages full-viewport video autoplay, responsive handling,
 * and user scroll detection for transitioning to Phase 2.
 */

class WelcomeScreen {
    constructor(options = {}) {
        this.container = document.getElementById('welcomeScreen');
        this.video = document.getElementById('welcomeVideo');
        this.scrollPrompt = document.getElementById('scrollPrompt');
        this.onScrollCallback = options.onScrollTrigger || null;
        this.isTriggered = false;

        this.init();
    }

    init() {
        if (!this.video) {
            console.error('WelcomeScreen: #welcomeVideo element not found.');
            return;
        }

        // Configure video for bulletproof cross-browser autoplay
        this.video.muted = true;
        this.video.defaultMuted = true;
        this.video.autoplay = true;
        this.video.loop = true;
        this.video.playsInline = true;
        this.video.setAttribute('playsinline', '');
        this.video.setAttribute('webkit-playsinline', '');

        // Safe autoplay attempt
        const playPromise = this.video.play();
        if (playPromise !== undefined) {
            playPromise.catch((err) => {
                console.warn('Autoplay was prevented by browser policy, user interaction will start playback:', err);
                const playOnInteract = () => {
                    this.video.play();
                    window.removeEventListener('click', playOnInteract);
                    window.removeEventListener('touchstart', playOnInteract);
                };
                window.addEventListener('click', playOnInteract, { once: true });
                window.addEventListener('touchstart', playOnInteract, { once: true });
            });
        }

        // Attach scroll and gesture listeners for Phase 2 transition trigger
        this.attachListeners();
    }

    attachListeners() {
        // 1. Mouse wheel / trackpad scroll
        window.addEventListener('wheel', (e) => {
            if (!this.isTriggered && e.deltaY > 10) {
                this.triggerDarshanTransition();
            }
        }, { passive: true });

        // 2. Touch swipe gesture on mobile
        let touchStartY = 0;
        window.addEventListener('touchstart', (e) => {
            touchStartY = e.touches[0].clientY;
        }, { passive: true });

        window.addEventListener('touchend', (e) => {
            const touchEndY = e.changedTouches[0].clientY;
            if (!this.isTriggered && (touchStartY - touchEndY > 30)) {
                this.triggerDarshanTransition();
            }
        }, { passive: true });

        // 3. Direct click/tap on corner prompt
        if (this.scrollPrompt) {
            this.scrollPrompt.addEventListener('click', (e) => {
                e.preventDefault();
                if (!this.isTriggered) {
                    this.triggerDarshanTransition();
                }
            });
        }

        // 4. Keyboard Navigation (ArrowDown, PageDown, Space, Enter)
        window.addEventListener('keydown', (e) => {
            if (!this.isTriggered && ['ArrowDown', 'PageDown', 'Space', 'Enter'].includes(e.code)) {
                this.triggerDarshanTransition();
            }
        });
    }

    triggerDarshanTransition() {
        this.isTriggered = true;
        if (typeof this.onScrollCallback === 'function') {
            this.onScrollCallback();
        }
    }

    hide() {
        if (this.container) {
            this.container.style.transform = 'translateY(-100%)';
            this.container.style.opacity = '0';
            this.container.style.pointerEvents = 'none';
        }
    }

    show() {
        this.isTriggered = false;
        if (this.container) {
            this.container.style.transform = 'translateY(0)';
            this.container.style.opacity = '1';
            this.container.style.pointerEvents = 'auto';
        }
    }
}

// Export for module or global use
window.WelcomeScreen = WelcomeScreen;

