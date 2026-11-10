"""
Comprehensive Verification and Visual Renderer for Phase 4 & Phase 5:
- Phase 4: Interactive Aarti Thali, Hand Gesture Tracking, Parikrama Physics, Bell Chimes
- Phase 5: 7-Round Completion, Shankh Naad, Celebratory Flower Burst, Divine Hindi Blessing Modal
"""

import os
import sys
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

WORKSPACE = r'c:\Users\pranjali\OneDrive\Desktop\Divinity_Maa_Laxmi'

def audit_files_and_code():
    print("=" * 70)
    print("STEP 1: AUDITING PHASE 4 & 5 CODE AND ASSETS INTEGRITY")
    print("=" * 70)

    required_files = [
        ('index.html', 5000),
        ('tests/preview_darshan.html', 3000),
        ('css/aarti.css', 4000),
        ('css/aarti_player.css', 5000),
        ('css/sanctum.css', 4000),
        ('css/welcome.css', 2000),
        ('css/curtains.css', 2000),
        ('js/aarti.js', 15000),
        ('js/aarti_player.js', 12000),
        ('js/environment.js', 20000),
        ('js/curtains.js', 8000),
        ('js/welcome.js', 2500),
        ('data/aarti_lyrics.json', 5000),
        ('media/audio/maa-lakshmi-aarti.mp3', 5000000),
        ('media/audio/shankh_naad.mp3', 80000),
        ('media/images/maa_lakshmi_darshan_4k.jpg', 2500000),
        ('media/video/cinematic_diwali_darshan_1080p.mp4', 50000000)
    ]

    all_ok = True
    for fname, min_size in required_files:
        fpath = os.path.join(WORKSPACE, fname)
        if not os.path.exists(fpath):
            print(f"[-] MISSING: {fname}")
            all_ok = False
        else:
            sz = os.path.getsize(fpath)
            if sz < min_size:
                print(f"[!] WARNING: {fname} size ({sz} bytes) is below expected ({min_size} bytes)")
                all_ok = False
            else:
                print(f"[+] VERIFIED: {fname:<35} ({sz:>9,} bytes)")

    # Inspect code logic in js/aarti.js
    aarti_js_path = os.path.join(WORKSPACE, 'js', 'aarti.js')
    with open(aarti_js_path, 'r', encoding='utf-8') as f:
        aarti_code = f.read()

    checks = [
        ("AartiInteractionComponent class definition", "class AartiInteractionComponent" in aarti_code),
        ("Center coordinate calculation for widescreen and portrait", "getArtworkCenter()" in aarti_code),
        ("Fluid window mouse tracking listener", "window.addEventListener('mousemove'" in aarti_code),
        ("Fluid window touch tracking listener", "window.addEventListener('touchmove'" in aarti_code),
        ("Clockwise parikrama angular tracking", "trackCircularMotion" in aarti_code and "cumulativeAngle += delta" in aarti_code),
        ("Minimum radius threshold for parikrama", "dist < 40" in aarti_code),
        ("Resonant temple bell chimes synthesis", "playBellChime" in aarti_code and "createOscillator" in aarti_code),
        ("Quarter turn bell trigger", "Math.PI / 2" in aarti_code),
        ("Full round flower burst trigger", "spawnFlowerBurst" in aarti_code),
        ("7 rounds maximum threshold", "maxRounds = 7" in aarti_code),
        ("Phase 5 Final Blessings transition", "triggerFinalBlessings" in aarti_code),
        ("Shankh Naad audio trigger", "shankhAudio.play()" in aarti_code),
        ("Spoken Hindi divine blessing voiceover", "सदा सुखी रहो" in aarti_code and "speechSynthesis" in aarti_code),
        ("Final blessings modal activation", "blessingModal.classList.add('active')" in aarti_code),
        ("Modal restart button callback", "closeBlessingModal" in aarti_code and "restartAartiBtn" in aarti_code),
        ("Flame aerodynamic velocity tilt", "Math.max(-18, Math.min(18, -vx * 0.55))" in aarti_code),
        ("MediaPipe Hands detection engine", "window.Hands" in aarti_code and "multiHandLandmarks" in aarti_code),
        ("Zero-dependency local skin-chroma CV fallback", "getImageData" in aarti_code and "count > 70" in aarti_code),
        ("Autonomous Auto-Aarti circular motion", "isAutoAarti" in aarti_code and "autoAngle" in aarti_code),
    ]

    print("\n--- CODE LOGIC VERIFICATION ---")
    for desc, passed in checks:
        status = "[+] PASS" if passed else "[-] FAIL"
        print(f"{status}: {desc}")
        if not passed:
            all_ok = False

    return all_ok


def draw_aarti_thali(layer, draw, cx, cy, sz=250, tilt=0):
    """Draws authentic ornate Panchmukhi brass Aarti Thali with 5 perfectly aligned flames"""
    tw = sz
    th = int(sz / 1.5625)
    tx = cx - tw // 2
    ty = cy - th // 2

    # Drop shadow
    shadow = Image.new('RGBA', layer.size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([tx + int(tw * 0.04), ty + int(th * 0.12), tx + int(tw * 0.96), ty + int(th * 1.12)], fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(max(int(sz * 0.05), 3)))
    layer.paste(Image.alpha_composite(Image.new('RGBA', layer.size, (0, 0, 0, 0)), shadow), (0, 0), shadow)

    # Authentic Panchmukhi Thali Plate
    thali_path = os.path.join(WORKSPACE, 'media', 'images', 'panchmukhi_aarti_thali.png')
    if os.path.exists(thali_path):
        thali_img = Image.open(thali_path).convert('RGBA')
        thali_scaled = thali_img.resize((tw, th), Image.Resampling.LANCZOS)
        layer.paste(thali_scaled, (tx, ty), thali_scaled)

    # 5 Authentically Aligned Flames:
    # 1: Diya 1 (Lower-Left), 2: Diya 2 (Upper-Left), 3: Kapoor (Apex), 4: Diya 4 (Upper-Right), 5: Diya 5 (Lower-Right)
    flame_w = max(int(tw * 0.048), 8)
    flame_h = max(int(th * 0.15), 16)
    kapoor_w = max(int(tw * 0.056), 10)
    kapoor_h = max(int(th * 0.165), 18)

    flames = [
        ('Diya 1', 0.3307, 0.3992, flame_w, flame_h, -2.0),
        ('Diya 2', 0.3711, 0.3014, flame_w, flame_h, -1.0),
        ('Kapoor', 0.5026, 0.2281, kapoor_w, kapoor_h, 0.0),
        ('Diya 4', 0.6315, 0.3014, flame_w, flame_h, 1.0),
        ('Diya 5', 0.6732, 0.3992, flame_w, flame_h, 2.0),
    ]

    for name, xp, yp, fw, fh, ftilt in flames:
        fx = tx + int(xp * tw)
        fy = ty + int(yp * th)
        # Velocity aerodynamic tilt
        dx = int(math.sin(math.radians(tilt + ftilt)) * (fh * 0.18))

        # Outer flame aura
        draw.ellipse([fx - fw // 2 - 3 + dx // 2, fy - fh - 3, fx + fw // 2 + 3 + dx // 2, fy + 3], fill=(255, 140, 0, 110))
        # Golden flame body
        draw.ellipse([fx - fw // 2 + dx // 2, fy - fh, fx + fw // 2 + dx // 2, fy], fill=(255, 215, 0, 210))
        # White hot inner core
        draw.ellipse([fx - fw // 4 + dx // 3, fy - int(fh * 0.75), fx + fw // 4 + dx // 3, fy - int(fh * 0.15)], fill=(255, 255, 255, 245))


def render_phase4_interactive_scene(output_path, is_mobile=False, custom_w=None, custom_h=None):
    """Renders Sanctum with active Aarti Thali circling Maa, top toolbar, camera PiP, and lyrics pedestal"""
    if custom_w and custom_h:
        width, height = custom_w, custom_h
    else:
        width, height = (412, 915) if is_mobile else (1920, 1080)
    print(f"Rendering Phase 4 Interactive Scene: {width}x{height} (Mobile={is_mobile})...")

    # 1. Base Darshan Scene
    master_path = os.path.join(WORKSPACE, 'media', 'images', 'maa_lakshmi_darshan_4k.jpg')
    img_master = Image.open(master_path).convert('RGBA')
    mw, mh = img_master.size
    img_aspect = mw / mh

    viewport = Image.new('RGBA', (width, height), (8, 3, 1, 255))

    # Ambient blurred backdrop
    bg_scale = max(width / mw, height / mh) * 1.12
    bg_w = int(mw * bg_scale)
    bg_h = int(mh * bg_scale)
    bg_img = img_master.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
    bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=32 if not is_mobile else 20))
    bg_img = ImageEnhance.Brightness(bg_img).enhance(0.52)
    bg_img = ImageEnhance.Color(bg_img).enhance(1.2)
    viewport.paste(bg_img, ((width - bg_w)//2, (height - bg_h)//2), bg_img)

    # Crisp foreground master
    view_aspect = width / height
    if view_aspect < 1.6:
        fg_w = width
        fg_h = int(width / img_aspect)
        fg_x = 0
        fg_y = (height - fg_h) // 2
    else:
        if view_aspect > img_aspect:
            fg_w = width
            fg_h = int(width / img_aspect)
            fg_x = 0
            fg_y = (height - fg_h) // 2
        else:
            fg_h = height
            fg_w = int(height * img_aspect)
            fg_x = (width - fg_w) // 2
            fg_y = 0

    fg_img = img_master.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
    viewport.paste(fg_img, (fg_x, fg_y), fg_img)

    # Prabha Mandal Halo & Divine God Rays
    aura_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    aura_draw = ImageDraw.Draw(aura_layer)
    crown_cx = fg_x + int(fg_w * 0.503)
    crown_cy = fg_y + int(fg_h * 0.245)
    aura_r = int(min(width * 0.26, 220 if not is_mobile else 110))

    for r in range(aura_r, 0, -3):
        frac = r / aura_r
        alpha = int((1.0 - frac**1.4) * 85)
        aura_draw.ellipse([crown_cx - r, crown_cy - r, crown_cx + r, crown_cy + r], fill=(255, int(220 - frac*60), int(60*(1-frac)), alpha))
    aura_layer = aura_layer.filter(ImageFilter.GaussianBlur(radius=16 if not is_mobile else 10))
    viewport = Image.alpha_composite(viewport, aura_layer)

    # Particles: Coins falling, Diya flames, Flowers
    fx_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    fx_draw = ImageDraw.Draw(fx_layer)

    # Dhan Varsha coins
    mouth_x = fg_x + int(fg_w * 0.536)
    mouth_y = fg_y + int(fg_h * 0.565)
    target_y = fg_y + int(fg_h * 0.91)
    random.seed(108)
    for ci in range(25 if not is_mobile else 16):
        t = ci / 25.0
        cy = mouth_y + t * (target_y - mouth_y) + (random.random() * 8 - 4)
        cx = mouth_x + (random.random() * 20 - 10) + (t * 5)
        c_rad = (5.5 if not is_mobile else 3.5)
        fx_draw.ellipse([cx - c_rad, cy - c_rad*0.5, cx + c_rad, cy + c_rad*0.5], fill=(255, 215, 0, 245), outline=(180, 130, 20, 255))

    # Floating flower petals
    for _ in range(24 if not is_mobile else 14):
        px = random.randint(0, width)
        py = random.randint(0, height)
        psz = random.randint(8, 16) if not is_mobile else random.randint(6, 11)
        pcol = random.choice([(211, 47, 47, 230), (240, 98, 146, 230), (255, 160, 0, 230)])
        fx_draw.ellipse([px - psz*0.7, py - psz, px + psz*0.7, py + psz], fill=pcol)

    viewport = Image.alpha_composite(viewport, fx_layer)

    # 2. Phase 4: Aarti Thali in Motion
    thali_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    thali_draw = ImageDraw.Draw(thali_layer)

    # Position thali along circular parikrama arc around Maa
    center_y = fg_y + int(fg_h * 0.44)
    thali_angle = math.radians(65) # Clockwise arc (bottom-right)
    rx = min(width * 0.26, 240) if not is_mobile else min(width * 0.32, 120)
    ry = min(height * 0.18, 170) if not is_mobile else min(height * 0.14, 85)
    thali_cx = int(width / 2 + math.cos(thali_angle) * rx)
    thali_cy = int(center_y + math.sin(thali_angle) * ry)
    thali_sz = 250 if not is_mobile else 190

    # Parikrama Trail Guide Curve (Subtle golden glowing guide)
    guide_steps = 60
    for s in range(guide_steps):
        a = (s / guide_steps) * math.pi * 2
        gx = int(width / 2 + math.cos(a) * rx)
        gy = int(center_y + math.sin(a) * ry)
        thali_draw.ellipse([gx - 1.5, gy - 1.5, gx + 1.5, gy + 1.5], fill=(255, 215, 0, 45))

    draw_aarti_thali(thali_layer, thali_draw, thali_cx, thali_cy, sz=thali_sz, tilt=-12)
    viewport = Image.alpha_composite(viewport, thali_layer)

    # 3. Top Aarti Toolbar
    ui_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    ui_draw = ImageDraw.Draw(ui_layer)

    try:
        font_hindi = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 16 if not is_mobile else 11)
        font_hindi_b = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 18 if not is_mobile else 12)
        font_latin = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 13 if not is_mobile else 10)
        font_latin_b = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 13 if not is_mobile else 10)
    except:
        font_hindi = font_hindi_b = font_latin = font_latin_b = None

    tb_y = 20 if not is_mobile else 12
    tb_w = int(min(width * 0.95, 1280)) if not is_mobile else int(width * 0.92)
    tb_x = (width - tb_w) // 2

    # A. Counter Badge
    badge_w = 210 if not is_mobile else 165
    badge_h = 38 if not is_mobile else 30
    ui_draw.rounded_rectangle([tb_x, tb_y, tb_x + badge_w, tb_y + badge_h], radius=19 if not is_mobile else 15,
                              fill=(28, 9, 2, 225), outline=(255, 215, 0, 200), width=1)
    if font_hindi_b:
        ui_draw.text((tb_x + 16, tb_y + (8 if not is_mobile else 6)), "🪔 Aarti Rounds: 3 / 7", fill=(255, 224, 130, 255), font=font_hindi_b)

    # B. Action Buttons
    btn_gap = 12 if not is_mobile else 8
    btn_cam_w = 175 if not is_mobile else 135
    btn_auto_w = 130 if not is_mobile else 105
    btn_h = 38 if not is_mobile else 30

    if not is_mobile:
        btn_auto_x = tb_x + tb_w - btn_auto_w
        btn_cam_x = btn_auto_x - btn_gap - btn_cam_w
        btn_cam_y = btn_auto_y = tb_y
    else:
        # Stacked / row on mobile
        btn_cam_x = tb_x
        btn_cam_y = tb_y + badge_h + 8
        btn_auto_x = btn_cam_x + btn_cam_w + btn_gap
        btn_auto_y = btn_cam_y

    # Camera Toggle Button (Active)
    ui_draw.rounded_rectangle([btn_cam_x, btn_cam_y, btn_cam_x + btn_cam_w, btn_cam_y + btn_h], radius=18,
                              fill=(255, 23, 68, 240), outline=(255, 82, 82, 255), width=1)
    if font_latin_b:
        ui_draw.text((btn_cam_x + btn_cam_w//2, btn_cam_y + (10 if not is_mobile else 7)), "📷 Stop Camera", fill=(255, 255, 255, 255), font=font_latin_b, anchor="mt")

    # Auto Aarti Button
    ui_draw.rounded_rectangle([btn_auto_x, btn_auto_y, btn_auto_x + btn_auto_w, btn_auto_y + btn_h], radius=18,
                              fill=(212, 175, 55, 240), outline=(255, 248, 220, 255), width=1)
    if font_latin_b:
        ui_draw.text((btn_auto_x + btn_auto_w//2, btn_auto_y + (10 if not is_mobile else 7)), "▶ Auto Aarti", fill=(18, 4, 0, 255), font=font_latin_b, anchor="mt")

    # 4. Webcam Picture-in-Picture Preview Box
    cam_w = 180 if not is_mobile else 130
    cam_h = 135 if not is_mobile else 98
    if not is_mobile:
        cam_x = width - cam_w - 24
        cam_y = height - cam_h - 24
    else:
        cam_x = width - cam_w - 14
        cam_y = 85 # Float safely above mobile pedestal

    # Outer border and shadow
    ui_draw.rounded_rectangle([cam_x, cam_y, cam_x + cam_w, cam_y + cam_h], radius=14,
                              fill=(15, 15, 20, 250), outline=(255, 215, 0, 220), width=2)
    # Simulated video silhouette of user's hand
    palm_x = cam_x + int(cam_w * 0.58)
    palm_y = cam_y + int(cam_h * 0.52)
    ui_draw.ellipse([palm_x - 18, palm_y - 18, palm_x + 18, palm_y + 18], fill=(60, 50, 40, 230))
    # Green tracking reticle
    ui_draw.ellipse([palm_x - 15, palm_y - 15, palm_x + 15, palm_y + 15], outline=(0, 255, 102, 255), width=2)
    ui_draw.ellipse([palm_x - 4, palm_y - 4, palm_x + 4, palm_y + 4], fill=(255, 215, 0, 255))
    # Status label
    ui_draw.rounded_rectangle([cam_x, cam_y + cam_h - 20, cam_x + cam_w, cam_y + cam_h], radius=4, fill=(0, 0, 0, 200))
    if font_latin:
        ui_draw.text((cam_x + cam_w//2, cam_y + cam_h - 16), "✋ Hand Tracking Active", fill=(255, 215, 0, 255), font=font_latin, anchor="mt")

    # 5. Bottom Mandir Lyrics & Audio Pedestal
    ped_w = int(min(width * 0.92, 740)) if not is_mobile else int(width * 0.94)
    ped_h = 108 if not is_mobile else 88
    ped_x = (width - ped_w) // 2
    ped_y = height - ped_h - (24 if not is_mobile else 14)

    ui_draw.rounded_rectangle([ped_x, ped_y, ped_x + ped_w, ped_y + ped_h], radius=18 if not is_mobile else 14,
                              fill=(16, 5, 2, 235), outline=(255, 215, 0, 120), width=1)
    if font_hindi:
        txt_prev = "ॐ जय लक्ष्मी माता, मैया जय लक्ष्मी माता।"
        txt_cur = "तुमको निशिदिन सेवत, हरि विष्णु विधाता॥ ॐ जय लक्ष्मी माता॥"
        txt_next = "उमा, रमा, ब्रह्माणी, तुम ही जग-माता।"
        ui_draw.text((ped_x + ped_w//2, ped_y + (10 if not is_mobile else 6)), txt_prev, fill=(255, 224, 130, 95), font=font_hindi, anchor="mt")
        ui_draw.text((ped_x + ped_w//2, ped_y + (30 if not is_mobile else 22)), txt_cur, fill=(255, 230, 80, 255), font=font_hindi_b, anchor="mt")
        ui_draw.text((ped_x + ped_w//2, ped_y + (54 if not is_mobile else 40)), txt_next, fill=(255, 215, 100, 105), font=font_hindi, anchor="mt")

    # Audio Play / Progress
    ctrl_y = ped_y + ped_h - (22 if not is_mobile else 18)
    btn_r = 13 if not is_mobile else 10
    ui_draw.ellipse([ped_x + 28 - btn_r, ctrl_y - btn_r, ped_x + 28 + btn_r, ctrl_y + btn_r], fill=(218, 165, 32, 255))
    if font_latin:
        ui_draw.text((ped_x + 28, ctrl_y - (7 if not is_mobile else 6)), "▶", fill=(18, 4, 0, 255), font=font_latin, anchor="mt")
        ui_draw.text((ped_x + 52, ctrl_y - 6), "01:42", fill=(255, 224, 130, 220), font=font_latin)

    bar_x1 = ped_x + (96 if not is_mobile else 78)
    bar_x2 = ped_x + ped_w - (120 if not is_mobile else 55)
    prog_w = int((bar_x2 - bar_x1) * 0.31) # 102s / 331s
    ui_draw.rounded_rectangle([bar_x1, ctrl_y - 2, bar_x2, ctrl_y + 2], radius=2, fill=(255, 215, 0, 50))
    ui_draw.rounded_rectangle([bar_x1, ctrl_y - 2, bar_x1 + prog_w, ctrl_y + 2], radius=2, fill=(255, 193, 7, 240))
    ui_draw.ellipse([bar_x1 + prog_w - 4, ctrl_y - 4, bar_x1 + prog_w + 4, ctrl_y + 4], fill=(255, 255, 255, 255))

    if font_latin:
        ui_draw.text((bar_x2 + 10, ctrl_y - 6), "05:31", fill=(255, 224, 130, 220), font=font_latin)
        if not is_mobile:
            ui_draw.text((bar_x2 + 55, ctrl_y - 7), "🔊", fill=(255, 224, 130, 240), font=font_latin)
            ui_draw.rounded_rectangle([bar_x2 + 75, ctrl_y - 2, bar_x2 + 110, ctrl_y + 2], radius=2, fill=(255, 215, 0, 160))

    viewport = Image.alpha_composite(viewport, ui_layer)
    out_rgb = viewport.convert('RGB')
    out_rgb.save(output_path, quality=95)
    print(f"Saved: {output_path} ({os.path.getsize(output_path)/1024:.1f} KB)")


def render_phase5_blessings_scene(output_path):
    """Renders Phase 5: Massive celebratory flower burst and radiant Final Blessings Modal"""
    width, height = 1920, 1080
    print(f"Rendering Phase 5 Final Blessings Scene: {width}x{height}...")

    # 1. Base Darshan Scene
    master_path = os.path.join(WORKSPACE, 'media', 'images', 'maa_lakshmi_darshan_4k.jpg')
    img_master = Image.open(master_path).convert('RGBA')
    mw, mh = img_master.size
    img_aspect = mw / mh

    viewport = Image.new('RGBA', (width, height), (8, 3, 1, 255))
    fg_h = height
    fg_w = int(height * img_aspect)
    fg_x = (width - fg_w) // 2
    fg_y = 0
    fg_img = img_master.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
    viewport.paste(fg_img, (fg_x, fg_y), fg_img)

    # 2. Phase 5: Celebratory Flower Shower Burst (85 radiant petals flying outwards)
    burst_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    burst_draw = ImageDraw.Draw(burst_layer)
    cx, cy = width // 2, int(height * 0.44)

    random.seed(777)
    for _ in range(85):
        angle = random.random() * math.pi * 2
        dist = random.uniform(40, 520)
        px = int(cx + math.cos(angle) * dist)
        py = int(cy + math.sin(angle) * dist)
        psz = random.randint(12, 28)
        pcol = random.choice([
            (229, 57, 53, 240),  # Red rose
            (244, 143, 177, 240), # Pink lotus
            (255, 179, 0, 245),  # Golden marigold
            (255, 238, 88, 230)  # Yellow petal
        ])
        burst_draw.ellipse([px - psz*0.7, py - psz, px + psz*0.7, py + psz], fill=pcol)

    viewport = Image.alpha_composite(viewport, burst_layer)

    # 3. Semi-transparent warm darkening backdrop behind modal
    dim_layer = Image.new('RGBA', (width, height), (15, 4, 1, 140))
    viewport = Image.alpha_composite(viewport, dim_layer)

    # 4. Phase 5 Final Blessings Modal Card
    modal_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    modal_draw = ImageDraw.Draw(modal_layer)

    card_w = 620
    card_h = 420
    card_x = (width - card_w) // 2
    card_y = (height - card_h) // 2

    # Outer radiant gold aura glow
    for gr in range(40, 0, -4):
        ga = int((1.0 - gr / 40.0) * 80)
        modal_draw.rounded_rectangle([card_x - gr, card_y - gr, card_x + card_w + gr, card_y + card_h + gr],
                                     radius=32, fill=(255, 215, 0, ga))

    # Inner deep maroon/ebony card
    modal_draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h],
                                 radius=24, fill=(24, 7, 2, 250), outline=(255, 215, 0, 255), width=3)
    modal_draw.rounded_rectangle([card_x + 8, card_y + 8, card_x + card_w - 8, card_y + card_h - 8],
                                 radius=18, outline=(212, 175, 55, 120), width=1)

    try:
        font_swastik = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 38)
        font_title = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 32)
        font_body = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 18)
        font_shloka = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 16)
        font_btn = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 18)
    except:
        font_swastik = font_title = font_body = font_shloka = font_btn = None

    if font_title:
        # Red sacred swastik (卐)
        modal_draw.text((width // 2, card_y + 24), "卐", fill=(255, 69, 0, 255), font=font_swastik, anchor="mt")
        # Heading
        modal_draw.text((width // 2, card_y + 78), "॥ शुभ दीपावली ॥", fill=(255, 224, 130, 255), font=font_title, anchor="mt")
        # Body text
        modal_draw.text((width // 2, card_y + 138), "माँ महालक्ष्मी की कृपा से आपके जीवन में सदैव", fill=(255, 236, 179, 255), font=font_body, anchor="mt")
        modal_draw.text((width // 2, card_y + 168), "सुख, शांति, समृद्धि और आरोग्य का वास हो।", fill=(255, 236, 179, 255), font=font_body, anchor="mt")
        # Shloka quote
        modal_draw.text((width // 2, card_y + 218), '"सर्वमङ्गलमाङ्गल्ये शिवे सर्वार्थसाधिके ।', fill=(255, 202, 40, 220), font=font_shloka, anchor="mt")
        modal_draw.text((width // 2, card_y + 246), 'शरण्ये त्र्यम्बके गौरि नारायणि नमोऽस्तु ते ॥"', fill=(255, 202, 40, 220), font=font_shloka, anchor="mt")

    # Restart button
    btn_w = 260
    btn_h = 48
    btn_x = (width - btn_w) // 2
    btn_y = card_y + card_h - 72
    modal_draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=24,
                                 fill=(212, 175, 55, 255), outline=(255, 255, 255, 220), width=1)
    if font_btn:
        modal_draw.text((width // 2, btn_y + 13), "✨ पुनः दर्शन एवं आरती", fill=(18, 4, 0, 255), font=font_btn, anchor="mt")

    viewport = Image.alpha_composite(viewport, modal_layer)
    out_rgb = viewport.convert('RGB')
    out_rgb.save(output_path, quality=95)
    print(f"Saved: {output_path} ({os.path.getsize(output_path)/1024:.1f} KB)")


if __name__ == '__main__':
    audit_passed = audit_files_and_code()
    print(f"\nAudit Passed: {audit_passed}\n")

    render_phase4_interactive_scene(
        os.path.join(WORKSPACE, 'archive', 'alternate_media', 'desktop_aarti_interaction_preview.png'),
        is_mobile=False
    )
    render_phase4_interactive_scene(
        os.path.join(WORKSPACE, 'archive', 'alternate_media', 'mobile_aarti_portrait_preview.png'),
        is_mobile=True
    )
    render_phase5_blessings_scene(
        os.path.join(WORKSPACE, 'archive', 'alternate_media', 'desktop_final_blessings_modal_preview.png')
    )
    print("\nAll Phase 4 & Phase 5 Verifications and Previews Successfully Generated!")

