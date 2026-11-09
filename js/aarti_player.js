/**
 * ============================================================================
 * PHASE 3B: MAA LAKSHMI AARTI AUDIO CONTROLLER & SYNCHRONIZED LYRICS ENGINE
 * 
 * - Drives HTMLAudioElement with full play, pause, seek, replay, and volume
 * - Synchronizes authoritative Hindi Devanagari lyrics from aarti_lyrics.json
 * - Displays previous, current, and upcoming lines with golden typography
 * - Distinguishes vocal verses from instrumental interludes
 * - Audio currentTime is the single source of truth
 * ============================================================================
 */

class MaaLakshmiAartiPlayer {
    constructor(options = {}) {
        this.audioElement = document.getElementById(options.audioId || 'aartiAudio');
        this.container = document.getElementById(options.containerId || 'aartiPlayerPedestal');
        
        // Lyrics Display DOM Elements
        this.prevLineEl = document.getElementById('lyricPrev');
        this.currentLineEl = document.getElementById('lyricCurrent');
        this.nextLineEl = document.getElementById('lyricNext');

        // Audio Controls DOM Elements
        this.playBtn = document.getElementById('btnPlayPause');
        this.replayBtn = document.getElementById('btnReplay');
        this.seekSlider = document.getElementById('aartiSeekSlider');
        this.currentTimeEl = document.getElementById('currentTimeDisplay');
        this.totalTimeEl = document.getElementById('totalTimeDisplay');
        this.volumeSlider = document.getElementById('aartiVolSlider');
        this.volumeBtn = document.getElementById('btnVolumeIcon');

        // State variables
        this.lyrics = [];
        this.currentIndex = -1;
        this.isSeeking = false;
        this.isPlaying = false;
        this.lastVolume = 0.85;

        // Fallback embedded authoritative lyrics to ensure instant 100% reliability
        // even when running offline or via file:// protocol
        this.embeddedLyrics = [
            { id: 'intro', verse: 0, type: 'instrumental', label: '🪔 ॥ शंखनाद एवं मंदिर घंटानाद (Instrumental Prelude) ॥ 🪔', text: '', startTime: 0.00, endTime: 13.40, verified: true },
            { id: 'v1_l1', verse: 1, type: 'vocal', text: 'ॐ जय लक्ष्मी माता, मैया जय लक्ष्मी माता।', startTime: 13.40, endTime: 33.80, verified: true },
            { id: 'v1_l2', verse: 1, type: 'vocal', text: 'तुमको निशिदिन सेवत, हरि विष्णु विधाता॥ ॐ जय लक्ष्मी माता॥', startTime: 33.80, endTime: 56.80, verified: true },
            { id: 'interlude_1', verse: 1, type: 'instrumental', label: '🪔 ॥ संगीत अन्तराल (Flute & Sitar Interlude) ॥ 🪔', text: '', startTime: 56.80, endTime: 60.40, verified: true },
            { id: 'v2_l1', verse: 2, type: 'vocal', text: 'उमा, रमा, ब्रह्माणी, तुम ही जग-माता।', startTime: 60.40, endTime: 82.20, verified: true },
            { id: 'v2_l2', verse: 2, type: 'vocal', text: 'सूर्य-चन्द्रमा ध्यावत, नारद ऋषि गाता॥ ॐ जय लक्ष्मी माता॥', startTime: 82.20, endTime: 102.50, verified: true },
            { id: 'interlude_2', verse: 2, type: 'instrumental', label: '🪔 ॥ संगीत अन्तराल (Dholak & Shenhai Interlude) ॥ 🪔', text: '', startTime: 102.50, endTime: 104.80, verified: true },
            { id: 'v3_l1', verse: 3, type: 'vocal', text: 'दुर्गा रुप निरंजनी, सुख सम्पत्ति दाता।', startTime: 104.80, endTime: 125.30, verified: true },
            { id: 'v3_l2', verse: 3, type: 'vocal', text: 'जो कोई तुमको ध्यावत, ऋद्धि-सिद्धि धन पाता॥ ॐ जय लक्ष्मी माता॥', startTime: 125.30, endTime: 149.00, verified: true },
            { id: 'interlude_3', verse: 3, type: 'instrumental', label: '🪔 ॥ संगीत अन्तराल (Interlude) ॥ 🪔', text: '', startTime: 149.00, endTime: 152.50, verified: true },
            { id: 'v4_l1', verse: 4, type: 'vocal', text: 'तुम पाताल-निवासिनि, तुम ही शुभदाता।', startTime: 152.50, endTime: 172.60, verified: true },
            { id: 'v4_l2', verse: 4, type: 'vocal', text: 'कर्म-प्रभाव-प्रकाशिनी, भवनिधि की त्राता॥ ॐ जय लक्ष्मी माता॥', startTime: 172.60, endTime: 192.50, verified: true },
            { id: 'interlude_4', verse: 4, type: 'instrumental', label: '🪔 ॥ संगीत अन्तराल (Interlude) ॥ 🪔', text: '', startTime: 192.50, endTime: 195.00, verified: true },
            { id: 'v5_l1', verse: 5, type: 'vocal', text: 'जिस घर में तुम रहतीं, सब सद्गुण आता।', startTime: 195.00, endTime: 203.80, verified: true },
            { id: 'v5_l2', verse: 5, type: 'vocal', text: 'सब सम्भव हो जाता, मन नहीं घबराता॥ ॐ जय लक्ष्मी माता॥', startTime: 203.80, endTime: 225.50, verified: true },
            { id: 'interlude_5', verse: 5, type: 'instrumental', label: '🪔 ॥ संगीत अन्तराल (Interlude) ॥ 🪔', text: '', startTime: 225.50, endTime: 227.20, verified: true },
            { id: 'v6_l1', verse: 6, type: 'vocal', text: 'तुम बिन यज्ञ न होते, वस्त्र न कोई पाता।', startTime: 227.20, endTime: 239.70, verified: true },
            { id: 'v6_l2', verse: 6, type: 'vocal', text: 'खान-पान का वैभव, सब तुमसे आता॥', startTime: 239.70, endTime: 254.50, verified: true },
            { id: 'interlude_6', verse: 6, type: 'instrumental', label: '🪔 ॥ संगीत अन्तराल (Interlude) ॥ 🪔', text: '', startTime: 254.50, endTime: 257.50, verified: true },
            { id: 'v7_l1', verse: 7, type: 'vocal', text: 'शुभ-गुण मन्दिर सुन्दर, क्षीरोदधि-जाता।', startTime: 257.50, endTime: 274.20, verified: true },
            { id: 'v7_l2', verse: 7, type: 'vocal', text: 'रत्न चतुर्दश तुमहीं, कोई नहीं पाता॥', startTime: 274.20, endTime: 288.80, verified: true },
            { id: 'interlude_7', verse: 7, type: 'instrumental', label: '🪔 ॥ संगीत अन्तराल (Interlude) ॥ 🪔', text: '', startTime: 288.80, endTime: 293.50, verified: true },
            { id: 'v8_l1', verse: 8, type: 'vocal', text: 'महा लक्ष्मीजी की आरती, जो कोई जन गाता।', startTime: 293.50, endTime: 305.50, verified: true },
            { id: 'v8_l2', verse: 8, type: 'vocal', text: 'उर आनन्द समाता, पाप उतर जाता॥ ॐ जय लक्ष्मी माता॥', startTime: 305.50, endTime: 327.20, verified: true },
            { id: 'outro', verse: 9, type: 'instrumental', label: '🪔 ॥ महाआरती पूर्णम् एवं घंटानाद (Crescendo & Temple Bells) ॥ 🪔', text: '', startTime: 327.20, endTime: 331.02, verified: true }
        ];

        // Immediately seed lyrics so synchronization is active synchronously from t=0
        this.lyrics = this.embeddedLyrics.slice();

        this.init();
    }

    async init() {
        await this.loadLyrics();
        this.setupAudioEvents();
        this.setupUIEvents();
        this.updateLyricsDisplay(0);
    }

    async loadLyrics() {
        // When running on local file:// protocol, use embedded authoritative lyrics directly
        // to avoid browser CORS fetch warnings on local file systems
        if (typeof window !== 'undefined' && window.location && window.location.protocol === 'file:') {
            this.lyrics = this.embeddedLyrics;
            return;
        }

        try {
            const resp = await fetch('data/aarti_lyrics.json');
            if (resp.ok) {
                this.lyrics = await resp.json();
                console.log('MaaLakshmiAartiPlayer: Loaded lyrics JSON successfully.');
            } else {
                this.lyrics = this.embeddedLyrics;
            }
        } catch (e) {
            this.lyrics = this.embeddedLyrics;
        }
    }

    setupAudioEvents() {
        if (!this.audioElement) return;

        // Metadata loaded: set total duration
        this.audioElement.addEventListener('loadedmetadata', () => {
            const dur = this.audioElement.duration;
            if (this.totalTimeEl && !isNaN(dur)) {
                this.totalTimeEl.textContent = this.formatTime(dur);
            }
            if (this.seekSlider && !isNaN(dur)) {
                this.seekSlider.max = Math.floor(dur);
            }
        });

        // Timeupdate: Single source of truth for synchronization
        this.audioElement.addEventListener('timeupdate', () => {
            if (!this.isSeeking) {
                const ct = this.audioElement.currentTime;
                const dur = this.audioElement.duration || 331.02;

                if (this.currentTimeEl) {
                    this.currentTimeEl.textContent = this.formatTime(ct);
                }
                if (this.seekSlider) {
                    this.seekSlider.value = Math.floor(ct);
                    this.updateSliderFill(this.seekSlider, (ct / dur) * 100);
                }

                this.syncLyrics(ct);
            }
        });

        // Play / Pause event listeners for UI state
        this.audioElement.addEventListener('play', () => {
            this.isPlaying = true;
            if (this.playBtn) {
                this.playBtn.innerHTML = '⏸';
                this.playBtn.setAttribute('aria-label', 'Pause Aarti');
            }
        });

        this.audioElement.addEventListener('pause', () => {
            this.isPlaying = false;
            if (this.playBtn) {
                this.playBtn.innerHTML = '▶';
                this.playBtn.setAttribute('aria-label', 'Play Aarti');
            }
        });

        this.audioElement.addEventListener('ended', () => {
            this.isPlaying = false;
            if (this.playBtn) {
                this.playBtn.innerHTML = '↺';
                this.playBtn.setAttribute('aria-label', 'Replay Aarti');
            }
            console.log('MaaLakshmiAartiPlayer: Aarti hymn completed.');
        });

        // Error handling
        this.audioElement.addEventListener('error', (e) => {
            console.error('MaaLakshmiAartiPlayer: Audio error:', e);
            if (this.currentLineEl) {
                this.currentLineEl.innerHTML = '<span style="color:#FF8A80; font-size:1.0rem;">॥ ऑडियो लोड करने में असमर्थ । कृपया पुनः प्रयास करें ॥</span>';
            }
        });
    }

    setupUIEvents() {
        // Play / Pause toggle
        if (this.playBtn) {
            this.playBtn.addEventListener('click', () => this.togglePlay());
        }

        // Replay button
        if (this.replayBtn) {
            this.replayBtn.addEventListener('click', () => this.replay());
        }

        // Seeking via progress bar
        if (this.seekSlider) {
            this.seekSlider.addEventListener('input', () => {
                this.isSeeking = true;
                const targetTime = parseFloat(this.seekSlider.value);
                if (this.currentTimeEl) {
                    this.currentTimeEl.textContent = this.formatTime(targetTime);
                }
                const dur = this.audioElement.duration || 331.02;
                this.updateSliderFill(this.seekSlider, (targetTime / dur) * 100);
            });

            this.seekSlider.addEventListener('change', () => {
                const targetTime = parseFloat(this.seekSlider.value);
                this.seek(targetTime);
                this.isSeeking = false;
            });
        }

        // Volume slider
        if (this.volumeSlider) {
            this.volumeSlider.addEventListener('input', () => {
                const vol = parseFloat(this.volumeSlider.value);
                this.setVolume(vol);
            });
        }

        // Volume icon mute/unmute toggle
        if (this.volumeBtn) {
            this.volumeBtn.addEventListener('click', () => this.toggleMute());
        }
    }

    togglePlay() {
        if (!this.audioElement) return;
        if (this.audioElement.paused) {
            this.audioElement.play().catch(e => console.warn('Play was prevented:', e));
        } else {
            this.audioElement.pause();
        }
    }

    play() {
        if (this.audioElement && this.audioElement.paused) {
            this.audioElement.play().catch(e => console.warn('Play error:', e));
        }
    }

    pause() {
        if (this.audioElement && !this.audioElement.paused) {
            this.audioElement.pause();
        }
    }

    replay() {
        if (!this.audioElement) return;
        this.seek(0);
        this.audioElement.play().catch(e => console.warn('Replay error:', e));
    }

    seek(timeInSeconds) {
        if (!this.audioElement) return;
        this.audioElement.currentTime = Math.max(0, Math.min(timeInSeconds, this.audioElement.duration || 331.02));
        this.syncLyrics(this.audioElement.currentTime);
    }

    setVolume(vol) {
        if (!this.audioElement) return;
        vol = Math.max(0, Math.min(1, vol));
        this.audioElement.volume = vol;
        if (this.volumeSlider) {
            this.volumeSlider.value = vol;
            this.updateSliderFill(this.volumeSlider, vol * 100);
        }
        if (this.volumeBtn) {
            this.volumeBtn.textContent = vol === 0 ? '🔇' : (vol < 0.5 ? '🔉' : '🔊');
        }
    }

    toggleMute() {
        if (!this.audioElement) return;
        if (this.audioElement.volume > 0) {
            this.lastVolume = this.audioElement.volume;
            this.setVolume(0);
        } else {
            this.setVolume(this.lastVolume || 0.85);
        }
    }

    /**
     * Synchronizes lyrics strictly based on audio currentTime
     */
    syncLyrics(currentTime) {
        if (!this.lyrics || this.lyrics.length === 0) return;

        let activeIdx = -1;
        for (let i = 0; i < this.lyrics.length; i++) {
            const item = this.lyrics[i];
            if (currentTime >= item.startTime && currentTime < item.endTime) {
                activeIdx = i;
                break;
            }
        }

        // If beyond the last segment
        if (activeIdx === -1 && currentTime >= this.lyrics[this.lyrics.length - 1].endTime) {
            activeIdx = this.lyrics.length - 1;
        }

        if (activeIdx !== -1 && activeIdx !== this.currentIndex) {
            this.currentIndex = activeIdx;
            this.updateLyricsDisplay(activeIdx);
        }
    }

    updateLyricsDisplay(index) {
        if (index < 0 || index >= this.lyrics.length) return;

        const current = this.lyrics[index];
        const prev = index > 0 ? this.lyrics[index - 1] : null;
        const next = index < this.lyrics.length - 1 ? this.lyrics[index + 1] : null;

        // Previous Line
        if (this.prevLineEl) {
            this.prevLineEl.textContent = prev ? (prev.type === 'vocal' ? prev.text : '') : '';
        }

        // Current Active Line
        if (this.currentLineEl) {
            if (current.type === 'instrumental') {
                this.currentLineEl.innerHTML = `<span class="lyric-instrumental-badge">${current.label}</span>`;
            } else {
                this.currentLineEl.textContent = current.text;
            }
        }

        // Next Line
        if (this.nextLineEl) {
            this.nextLineEl.textContent = next ? (next.type === 'vocal' ? next.text : (next.label || '')) : '';
        }
    }

    updateSliderFill(slider, percent) {
        slider.style.background = `linear-gradient(to right, #FFD700 0%, #FFA000 ${percent}%, rgba(255, 215, 0, 0.22) ${percent}%, rgba(255, 215, 0, 0.22) 100%)`;
    }

    formatTime(seconds) {
        if (isNaN(seconds)) return '00:00';
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        return `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;
    }
}

window.MaaLakshmiAartiPlayer = MaaLakshmiAartiPlayer;

