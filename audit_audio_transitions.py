import subprocess
import imageio_ffmpeg
import numpy as np

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
mp3_path = r'c:\Users\pranjali\OneDrive\Desktop\Divinity_Maa_Laxmi\media\audio\maa-lakshmi-aarti.mp3'

# Extract 16kHz mono audio
cmd = [ffmpeg_exe, '-i', mp3_path, '-f', 's16le', '-ac', '1', '-ar', '16000', '-']
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
raw_audio, _ = proc.communicate()
audio = np.frombuffer(raw_audio, dtype=np.int16).astype(np.float32) / 32768.0
sr = 16000

def get_vocal_onset(t_search_start, t_search_end, step=0.05, win=0.15):
    best_t = t_search_start
    max_jump = 0
    prev_ve = None
    results = []
    
    t = t_search_start
    while t + win <= t_search_end:
        s = int(t * sr)
        c = audio[s : s + int(win * sr)]
        fft = np.abs(np.fft.rfft(c))
        f = np.fft.rfftfreq(len(c), 1/sr)
        # Vocal formant harmonic energy (focus on 400 - 2200 Hz)
        ve = np.sum(fft[(f >= 400) & (f <= 2200)])
        rms = np.sqrt(np.mean(c**2))
        results.append((t, ve, rms))
        if prev_ve is not None:
            jump = ve - prev_ve
            if jump > max_jump:
                max_jump = jump
                best_t = t
        prev_ve = ve
        t += step
    return best_t, results

# Transition checkpoints to verify
checkpoints = [
    ('Prelude -> V1 L1 (Om Jai Lakshmi Mata)', 12.0, 15.0),
    ('V1 L1 -> V1 L2 (Tumko Nishidin Sevat)', 31.0, 35.0),
    ('V1 L2 -> Interlude 1', 55.5, 59.0),
    ('Interlude 1 -> V2 L1 (Uma Rama Brahmani)', 59.0, 63.0),
    ('V2 L1 -> V2 L2 (Surya Chandrama Dhyavat)', 80.5, 84.0),
    ('V2 L2 -> Interlude 2', 101.0, 104.5),
    ('Interlude 2 -> V3 L1 (Durga Roop Niranjani)', 104.5, 108.5),
    ('V3 L1 -> V3 L2 (Jo Koi Tumko Dhyavat)', 123.5, 127.0),
    ('V3 L2 -> Interlude 3', 148.0, 151.5),
    ('Interlude 3 -> V4 L1 (Tum Patal Nivasini)', 151.5, 155.0),
    ('V4 L1 -> V4 L2 (Karm Prabhav Prakashini)', 170.5, 174.5),
    ('V4 L2 -> Interlude 4', 191.0, 194.5),
    ('Interlude 4 -> V5 L1 (Jis Ghar Mein Tum)', 193.5, 197.0),
    ('V5 L1 -> V5 L2 (Sab Sambhav Ho Jata)', 203.0, 206.5),
    ('V5 L2 -> Interlude 5', 224.0, 227.0),
    ('Interlude 5 -> V6 L1 (Tum Bin Yagya Na Hote)', 226.0, 229.5),
    ('V6 L1 -> V6 L2 (Khan Pan Ka Vaibhav)', 238.0, 241.5),
    ('V6 L2 -> Interlude 6', 253.0, 256.5),
    ('Interlude 6 -> V7 L1 (Shubh Gun Mandir)', 255.5, 259.0),
    ('V7 L1 -> V7 L2 (Ratna Chaturdash Tumhin)', 272.0, 275.5),
    ('V7 L2 -> Interlude 7', 287.0, 290.5),
    ('Interlude 7 -> V8 L1 (Maha Lakshmiji Ki Aarti)', 291.5, 295.0),
    ('V8 L1 -> V8 L2 (Ur Anand Samata)', 303.0, 306.5),
    ('V8 L2 -> Outro (Crescendo/Bells)', 325.0, 328.5)
]

print('=== DETAILED ONSET / OFFSET AUDIT ===')
for name, ts_start, ts_end in checkpoints:
    onset, res = get_vocal_onset(ts_start, ts_end)
    print(f'{name:48s}: Peak transition detected at {onset:5.2f}s')

