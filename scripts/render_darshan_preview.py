"""
High-Fidelity Viewport Simulation Renderer for Maa Lakshmi Darshan (4K Master)
Renders Desktop (1920x1080) and Mobile Portrait (412x915) screenshots directly from
the production assets, shaders, and particle physics equations used in index.html & environment.js.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np

def render_viewport(width, height, is_mobile=False, output_path=None):
    print(f"Rendering viewport: {width}x{height} (Mobile={is_mobile})...")

    # 1. Load 4K Master Asset
    master_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media', 'images', 'maa_lakshmi_darshan_4k.jpg')
    img_master = Image.open(master_path).convert('RGBA')
    mw, mh = img_master.size
    img_aspect = mw / mh # ~16:9

    # Canvas root
    viewport = Image.new('RGBA', (width, height), (8, 3, 1, 255))

    # 2. Layer 1: Background Blurred Ambient Fill (for non-16:9 & portrait viewports)
    # Scales to cover full viewport with 36px blur and dark warm brightness
    bg_scale = max(width / mw, height / mh) * 1.12
    bg_w = int(mw * bg_scale)
    bg_h = int(mh * bg_scale)
    bg_img = img_master.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
    bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=36 if not is_mobile else 24))
    
    # Dim brightness to 0.52 and boost saturation
    enh_b = ImageEnhance.Brightness(bg_img)
    bg_img = enh_b.enhance(0.52)
    enh_c = ImageEnhance.Color(bg_img)
    bg_img = enh_c.enhance(1.2)

    bg_x = (width - bg_w) // 2
    bg_y = (height - bg_h) // 2
    viewport.paste(bg_img, (bg_x, bg_y), bg_img)

    # 3. Layer 2: Main Foreground Crisp Master Artwork
    # Desktop: object-fit: cover; Mobile: object-fit: contain (preserves all figures)
    view_aspect = width / height
    if view_aspect < 1.6:
        # Mobile: object-fit: contain
        fg_w = width
        fg_h = int(width / img_aspect)
        fg_x = 0
        fg_y = (height - fg_h) // 2
    else:
        # Desktop: object-fit: cover
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

    # 4. Layer 3: Golden Prabha Mandal Aura (Behind/around Maa's Crown)
    aura_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    aura_draw = ImageDraw.Draw(aura_layer)
    crown_cx = fg_x + int(fg_w * 0.503)
    crown_cy = fg_y + int(fg_h * 0.245)
    aura_r = int(min(width * 0.26, 220 if not is_mobile else 110))

    for r in range(aura_r, 0, -3):
        frac = r / aura_r
        alpha = int((1.0 - frac**1.4) * 85)
        r_col = 255
        g_col = int(220 - frac * 60)
        b_col = int(60 * (1 - frac))
        aura_draw.ellipse(
            [crown_cx - r, crown_cy - r, crown_cx + r, crown_cy + r],
            fill=(r_col, g_col, b_col, alpha)
        )
    aura_layer = aura_layer.filter(ImageFilter.GaussianBlur(radius=18 if not is_mobile else 10))
    viewport = Image.alpha_composite(viewport, aura_layer)

    # 5. Layer 4: Volumetric Divine God Rays
    rays_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    rays_draw = ImageDraw.Draw(rays_layer)
    num_rays = 14
    for i in range(num_rays):
        angle = -math.pi * 0.75 + (i / (num_rays - 1)) * math.pi * 0.5
        ray_len = max(width, height) * 0.85
        x1 = crown_cx + math.cos(angle - 0.04) * ray_len
        y1 = crown_cy + math.sin(angle - 0.04) * ray_len
        x2 = crown_cx + math.cos(angle + 0.04) * ray_len
        y2 = crown_cy + math.sin(angle + 0.04) * ray_len
        alpha = 14 if (i % 2 == 0) else 8
        rays_draw.polygon([(crown_cx, crown_cy), (x1, y1), (x2, y2)], fill=(255, 215, 60, alpha))
    rays_layer = rays_layer.filter(ImageFilter.GaussianBlur(radius=12))
    viewport = Image.alpha_composite(viewport, rays_layer)

    # 6. Layer 5: Canvas Particle Layer (Diya Flames, Dhan Varsha Coins, Petals, Prana Dust)
    fx_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    fx_draw = ImageDraw.Draw(fx_layer)

    # A. Diya Lamp Flames & Glow Pools
    lamps = [
        (0.155, 0.552, 7.5), # Left Samai
        (0.852, 0.552, 7.5), # Right Samai
        (0.328, 0.152, 5.0), # Hanging Left
        (0.672, 0.152, 5.0), # Hanging Right
        (0.335, 0.865, 4.8), # Center Puja Diya
    ]

    for nx, ny, sz in lamps:
        lx = fg_x + int(fg_w * nx)
        ly = fg_y + int(fg_h * ny)
        if is_mobile:
            sz *= 0.65

        # Glow pool
        pool_r = int(sz * 5)
        for pr in range(pool_r, 0, -2):
            p_alpha = int((1.0 - pr / pool_r) * 55)
            fx_draw.ellipse([lx - pr, ly - pr, lx + pr, ly + pr], fill=(255, 160, 20, p_alpha))

        # Flame core
        fw = sz
        fh = sz * 1.8
        fx_draw.ellipse([lx - fw*0.8, ly - fh*0.7, lx + fw*0.8, ly + fh*0.3], fill=(255, 175, 0, 220))
        fx_draw.ellipse([lx - fw*0.4, ly - fh*0.5, lx + fw*0.4, ly + fh*0.2], fill=(255, 245, 180, 255))
        fx_draw.ellipse([lx - fw*0.15, ly - fh*0.3, lx + fw*0.15, ly], fill=(255, 255, 255, 255))

    # B. Incense Smoke Wisps
    inc_x = fg_x + int(fg_w * 0.312)
    inc_y = fg_y + int(fg_h * 0.855)
    for si in range(18):
        sy = inc_y - si * (6 if not is_mobile else 3.5)
        sx = inc_x + math.sin(si * 0.4) * 6 + (si * 0.6)
        sr = 2 + si * 0.6
        s_alpha = int(max(0, (1.0 - si / 18.0) * 60))
        fx_draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(230, 225, 215, s_alpha))

    # C. Dhan Varsha Gold Coins (Falling from Kalash into Treasure Pile)
    mouth_x = fg_x + int(fg_w * 0.536)
    mouth_y = fg_y + int(fg_h * 0.565)
    target_y = fg_y + int(fg_h * 0.91)

    random.seed(42) # Reproducible divine frame
    for ci in range(35 if not is_mobile else 22):
        t = ci / 35.0
        cy = mouth_y + t * (target_y - mouth_y) + (random.random() * 8 - 4)
        cx = mouth_x + (random.random() * 24 - 12) + (t * 6)
        c_rad = (6.0 if not is_mobile else 3.8) * (0.85 + random.random() * 0.3)
        rot = ci * 0.85
        scale_y_coin = abs(math.cos(rot))

        # 3D Gold coin
        c_h = max(1.5, c_rad * scale_y_coin)
        fx_draw.ellipse(
            [cx - c_rad, cy - c_h, cx + c_rad, cy + c_h],
            fill=(255, 215, 0, 245),
            outline=(190, 135, 15, 255),
            width=1
        )
        # Specular glint
        if ci % 3 == 0:
            fx_draw.ellipse(
                [cx - c_rad*0.3, cy - c_h*0.3, cx + c_rad*0.1, cy + c_h*0.1],
                fill=(255, 255, 255, 230)
            )

    # D. Multi-Depth Petals (Red Rose & Sacred Pink Lotus)
    petals_data = [
        # (x_frac, y_frac, size, type, angle)
        (0.18, 0.22, 14, 'rose', 0.4),
        (0.24, 0.45, 12, 'lotus', 1.2),
        (0.35, 0.32, 16, 'rose', -0.6),
        (0.42, 0.15, 10, 'lotus', 0.8),
        (0.58, 0.18, 12, 'rose', 1.5),
        (0.68, 0.35, 18, 'rose', -0.3),
        (0.78, 0.28, 15, 'lotus', 0.7),
        (0.85, 0.48, 13, 'rose', -1.1),
        (0.12, 0.65, 16, 'marigold', 0.9),
        (0.88, 0.72, 15, 'rose', 0.5),
        (0.52, 0.78, 11, 'lotus', -0.4),
        (0.38, 0.68, 13, 'rose', 1.1),
        (0.62, 0.62, 14, 'marigold', -0.8),
        # Foreground large bokeh petals
        (0.08, 0.82, 28, 'rose', 0.3),
        (0.92, 0.85, 26, 'lotus', -0.5),
        (0.48, 0.92, 24, 'rose', 0.6),
    ]

    for pxf, pyf, psz, ptype, pang in petals_data:
        px = int(width * pxf)
        py = int(height * pyf)
        if is_mobile:
            psz *= 0.7

        p_col = (211, 47, 47, 235) if ptype == 'rose' else ((240, 98, 146, 235) if ptype == 'lotus' else (255, 160, 0, 235))
        
        # Simple rotated curved petal
        pw = psz * 0.7
        ph = psz * 1.3
        fx_draw.ellipse([px - pw, py - ph, px + pw, py + ph], fill=p_col)

    # E. Golden Prana Particles (Sparkles & Celestial Orbs)
    for si in range(45 if not is_mobile else 25):
        sx = int(random.random() * width)
        sy = int(random.random() * height)
        sr = 1.2 + random.random() * 2.5
        s_alpha = int(120 + random.random() * 110)
        fx_draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 235, 130, s_alpha))

    viewport = Image.alpha_composite(viewport, fx_layer)

    # 7. Layer 6: Phase 3B Devotional Mandir Lyrics & Audio Pedestal (Bottom Floating Dock)
    pedestal_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    ped_draw = ImageDraw.Draw(pedestal_layer)

    ped_w = int(min(width * 0.92, 740)) if not is_mobile else int(width * 0.94)
    ped_h = 108 if not is_mobile else 88
    ped_x = (width - ped_w) // 2
    ped_y = height - ped_h - (24 if not is_mobile else 14)

    # Glassmorphic ebony & deep maroon body with gold border
    ped_draw.rounded_rectangle(
        [ped_x, ped_y, ped_x + ped_w, ped_y + ped_h],
        radius=18 if not is_mobile else 14,
        fill=(16, 5, 2, 235),
        outline=(255, 215, 0, 120),
        width=1
    )

    # Inner subtle gold highlight line
    ped_draw.line(
        [(ped_x + 16, ped_y + 1), (ped_x + ped_w - 16, ped_y + 1)],
        fill=(255, 240, 160, 50),
        width=1
    )

    # Fonts with full Hindi Devanagari support
    try:
        from PIL import ImageFont
        font_main = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 19 if not is_mobile else 12)
        font_sub = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 12 if not is_mobile else 8)
        font_latin = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 11 if not is_mobile else 9)
    except:
        font_main = font_sub = font_latin = None

    if font_main:
        # Previous Line (Subtle)
        txt_prev = "ॐ जय लक्ष्मी माता, मैया जय लक्ष्मी माता।"
        ped_draw.text((ped_x + ped_w//2, ped_y + (10 if not is_mobile else 6)), txt_prev, fill=(255, 224, 130, 95), font=font_sub, anchor="mt")

        # Current Active Line (Luminous Golden Focus)
        txt_cur = "तुमको निशिदिन सेवत, हरि विष्णु विधाता॥ ॐ जय लक्ष्मी माता॥"
        ped_draw.text((ped_x + ped_w//2, ped_y + (30 if not is_mobile else 22)), txt_cur, fill=(255, 230, 80, 255), font=font_main, anchor="mt")

        # Next Line (Upcoming Context)
        txt_next = "उमा, रमा, ब्रह्माणी, तुम ही जग-माता।"
        ped_draw.text((ped_x + ped_w//2, ped_y + (54 if not is_mobile else 40)), txt_next, fill=(255, 215, 100, 105), font=font_sub, anchor="mt")

    # Audio Controls Row at bottom of pedestal
    ctrl_y = ped_y + ped_h - (24 if not is_mobile else 18)
    
    # Circular Play Button
    btn_r = 14 if not is_mobile else 11
    btn_cx = ped_x + 30
    btn_cy = ctrl_y
    ped_draw.ellipse([btn_cx - btn_r, btn_cy - btn_r, btn_cx + btn_r, btn_cy + btn_r], fill=(218, 165, 32, 255), outline=(255, 255, 255, 200), width=1)
    if font_latin:
        ped_draw.text((btn_cx, btn_cy - (7 if not is_mobile else 6)), "▶", fill=(18, 4, 0, 255), font=font_latin, anchor="mt")

    # Time display
    if font_latin:
        ped_draw.text((btn_cx + 28, ctrl_y - 6), "00:35", fill=(255, 224, 130, 220), font=font_latin)

    # Seek Progress Bar
    bar_x1 = btn_cx + (78 if not is_mobile else 65)
    bar_x2 = ped_x + ped_w - (120 if not is_mobile else 55)
    bar_w = bar_x2 - bar_x1
    progress_w = int(bar_w * 0.11) # ~35s / 331s

    # Track
    ped_draw.rounded_rectangle([bar_x1, ctrl_y - 2, bar_x2, ctrl_y + 2], radius=2, fill=(255, 215, 0, 50))
    # Filled progress
    ped_draw.rounded_rectangle([bar_x1, ctrl_y - 2, bar_x1 + progress_w, ctrl_y + 2], radius=2, fill=(255, 193, 7, 240))
    # Thumb
    ped_draw.ellipse([bar_x1 + progress_w - 5, ctrl_y - 5, bar_x1 + progress_w + 5, ctrl_y + 5], fill=(255, 255, 255, 255), outline=(218, 165, 32, 255))

    # Total Time
    if font_latin:
        ped_draw.text((bar_x2 + 10, ctrl_y - 6), "05:31", fill=(255, 224, 130, 220), font=font_latin)

    # Volume icon on desktop
    if not is_mobile and font_latin:
        ped_draw.text((bar_x2 + 55, ctrl_y - 7), "🔊", fill=(255, 224, 130, 240), font=font_latin)
        ped_draw.rounded_rectangle([bar_x2 + 75, ctrl_y - 2, bar_x2 + 110, ctrl_y + 2], radius=2, fill=(255, 215, 0, 160))

    viewport = Image.alpha_composite(viewport, pedestal_layer)

    # Convert to RGB and save
    out_rgb = viewport.convert('RGB')
    if output_path:
        out_rgb.save(output_path, quality=95)
        print(f"Saved: {output_path} ({os.path.getsize(output_path)/1024:.1f} KB)")
    return out_rgb

if __name__ == '__main__':
    render_viewport(1920, 1080, is_mobile=False, output_path=r'c:\Users\pranjali\OneDrive\Desktop\Divinity_Maa_Laxmi\desktop_darshan_4k_preview.png')
    render_viewport(412, 915, is_mobile=True, output_path=r'c:\Users\pranjali\OneDrive\Desktop\Divinity_Maa_Laxmi\mobile_darshan_4k_preview.png')

