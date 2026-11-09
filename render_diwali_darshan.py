"""
Cinematic Devotional Diwali Animation: Maa's Holy Feet Darshan
Preserves original fiery golden-orange chakra, stationary decorated lotus feet,
slow clockwise chakra rotation, living glowing golden diya, floating red rose petals,
subtle golden prana particles, volumetric divine light rays, and increasing golden radiance.
"""

import os
import math
import random
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import imageio

def generate_animation():
    print("=" * 60)
    print("Beginning Devotional Diwali Animation Generation...")
    print("=" * 60)

    # 1. Paths and Reference Image
    orig_path = r'C:/Users/pranjali/.gemini/antigravity/brain/8868637f-3187-40ed-a6d7-cdcf53be6fbc/.user_uploaded/media_1794116102600_4ce53208.jpg'
    output_dir = r'c:\Users\pranjali\OneDrive\Desktop\Divinity_Maa_Laxmi'
    os.makedirs(output_dir, exist_ok=True)
    
    orig_img = Image.open(orig_path).convert('RGBA')
    orig_w, orig_h = orig_img.size
    print(f"Loaded original reference image: {orig_w}x{orig_h}")

    # Circular geometry normalization:
    # In original perspective: rx=301, ry=281
    scale_y = 301.0 / 281.0
    h_circ = int(round(orig_h * scale_y))
    img_circ = orig_img.resize((orig_w, h_circ), resample=Image.BICUBIC)

    cx = 481.5
    cy = 378.5 * scale_y
    flame_x = 498.0
    flame_y = 481.0 * scale_y
    diya_bowl_y = 516.0 * scale_y

    print(f"Chakra center: ({cx:.1f}, {cy:.1f}), Flame: ({flame_x:.1f}, {flame_y:.1f})")

    # 2. Extract Annular Chakra Layer
    Y, X = np.ogrid[:h_circ, :orig_w]
    dist_from_center = np.sqrt((X - cx)**2 + (Y - cy)**2)

    # Inner boundary: 276 to 286 (just inside the beaded ring)
    inner_f = np.clip((dist_from_center - 276.0) / 10.0, 0.0, 1.0)
    inner_f = 3 * inner_f**2 - 2 * inner_f**3

    # Outer boundary: 380 to 405 (petal tips and golden aura)
    outer_f = np.clip((405.0 - dist_from_center) / 25.0, 0.0, 1.0)
    outer_f = 3 * outer_f**2 - 2 * outer_f**3

    chakra_alpha = inner_f * outer_f
    chakra_mask = Image.fromarray((chakra_alpha * 255).astype(np.uint8), mode='L')

    box_r = 430
    box_x0 = int(cx - box_r)
    box_y0 = int(cy - box_r)
    box_x1 = int(cx + box_r)
    box_y1 = int(cy + box_r)

    chakra_rgba = img_circ.copy()
    chakra_rgba.putalpha(chakra_mask)
    chakra_sprite = chakra_rgba.crop((box_x0, box_y0, box_x1, box_y1))

    # 3. Clean Background Plate behind chakra
    arr_circ = np.array(img_circ, dtype=float)
    bg_arr = arr_circ.copy()
    mask_annulus = (dist_from_center >= 270) & (dist_from_center <= 405)
    t_ann = np.clip((dist_from_center - 270.0) / (405.0 - 270.0), 0.0, 1.0)

    col_inner = np.array([255.0, 228.0, 95.0, 255.0])
    col_outer = np.array([254.0, 162.0, 10.0, 255.0])
    for c in range(4):
        bg_arr[..., c] = np.where(mask_annulus, (1.0 - t_ann) * col_inner[c] + t_ann * col_outer[c], bg_arr[..., c])

    bg_plate = Image.fromarray(np.uint8(bg_arr)).filter(ImageFilter.GaussianBlur(radius=6))

    # 4. Stationary Inner Sanctuary Mask (r < 283)
    inner_alpha_sanctuary = np.clip((283.0 - dist_from_center) / 7.0, 0.0, 1.0)
    inner_alpha_sanctuary = 3 * inner_alpha_sanctuary**2 - 2 * inner_alpha_sanctuary**3
    inner_sanctuary_mask = Image.fromarray((inner_alpha_sanctuary * 255).astype(np.uint8), mode='L')

    # 5. Pre-calculate Divine Light Rays grid
    dx = X - cx
    dy = Y - cy
    dist_rays = np.sqrt(dx**2 + dy**2) + 1e-5
    angle_rays = np.arctan2(dy, dx)
    # Radial falloff for rays: rising outside r=260, peaks at r=360, gentle falloff outward
    ray_falloff = np.clip((dist_rays - 260.0) / 100.0, 0.0, 1.0) * np.exp(-dist_rays / 500.0)
    ray_falloff = np.clip(ray_falloff * 2.8, 0.0, 1.0)

    # 6. Generate Realistic Rose Petal Sprites
    print("Generating realistic 3D rose petal sprites...")
    def create_petal_sprite(w=70, h=80, col_base=(215, 22, 38)):
        p_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(p_img)
        pcx, pcy = w / 2.0, h / 2.0
        pts = []
        num_pts = 64
        for i in range(num_pts):
            th = 2 * math.pi * i / num_pts
            r = (w * 0.42) * (1.0 + 0.28 * math.cos(th) - 0.22 * math.cos(2*th) + 0.1 * math.sin(th))
            px = pcx + r * math.sin(th) * 0.88
            py = pcy - r * math.cos(th)
            pts.append((px, py))
        draw.polygon(pts, fill=col_base + (255,))
        
        arr = np.array(p_img, dtype=float)
        py_grid, px_grid = np.ogrid[:h, :w]
        rim = np.exp(-((px_grid - pcx*0.75)**2 + (py_grid - pcy*0.65)**2) / (w*0.35)**2)
        shadow = np.exp(-((px_grid - pcx*1.25)**2 + (py_grid - pcy*1.25)**2) / (w*0.45)**2)
        
        mask = arr[..., 3] > 0
        arr[mask, 0] = np.clip(arr[mask, 0] * (1.0 - 0.28*shadow[mask] + 0.25*rim[mask]), 0, 255)
        arr[mask, 1] = np.clip(arr[mask, 1] * (1.0 - 0.35*shadow[mask] + 0.38*rim[mask]), 0, 255)
        arr[mask, 2] = np.clip(arr[mask, 2] * (1.0 - 0.25*shadow[mask]), 0, 255)
        
        return Image.fromarray(np.uint8(arr)).filter(ImageFilter.SMOOTH_MORE)

    base_petal_sprite = create_petal_sprite()

    # Pre-generate 36 floating rose petals with randomized motion properties
    random.seed(108) # Sacred seed
    petals = []
    num_petals = 36
    for i in range(num_petals):
        petals.append({
            'x0': random.uniform(30, orig_w - 30),
            'y0': random.uniform(-60, h_circ + 60),
            'depth': random.uniform(0.65, 1.25),
            'speed_y': random.uniform(36.0, 58.0),
            'sway_amp': random.uniform(25.0, 50.0),
            'sway_freq': random.uniform(1.2, 2.2),
            'sway_phase': random.uniform(0, 2 * math.pi),
            'pitch_freq': random.uniform(1.5, 3.0),
            'pitch_phase': random.uniform(0, 2 * math.pi),
            'roll_freq': random.uniform(1.8, 3.5),
            'roll_phase': random.uniform(0, 2 * math.pi),
            'rot_speed': random.uniform(-40.0, 40.0), # deg/sec
            'rot_init': random.uniform(0, 360),
            'opacity': random.uniform(0.85, 0.98),
        })

    # Pre-generate 120 subtle golden prana particles
    particles = []
    num_particles = 120
    for i in range(num_particles):
        particles.append({
            'x0': random.uniform(cx - 380, cx + 380),
            'y0': random.uniform(cy - 380, cy + 380),
            'vy': random.uniform(-25.0, -55.0), # float upward
            'vx_amp': random.uniform(8.0, 20.0),
            'vx_freq': random.uniform(1.0, 2.5),
            'vx_phase': random.uniform(0, 2 * math.pi),
            'twinkle_freq': random.uniform(3.0, 7.0),
            'twinkle_phase': random.uniform(0, 2 * math.pi),
            'radius': random.choice([1.0, 1.5, 2.0, 2.5, 3.5, 4.5]),
            'is_orb': random.random() < 0.35, # soft bokeh orb
        })

    # 7. Animation Settings
    fps = 30
    duration_sec = 12.0
    total_frames = int(fps * duration_sec)
    print(f"Total frames to render: {total_frames} ({duration_sec}s @ {fps}fps)")

    # Output video file paths
    video_path_centered = os.path.join(output_dir, "cinematic_diwali_darshan_centered.mp4")
    video_path_1080p = os.path.join(output_dir, "cinematic_diwali_darshan_1080p.mp4")
    poster_path = os.path.join(output_dir, "darshan_poster.png")

    writer_centered = imageio.get_writer(
        video_path_centered,
        fps=fps,
        codec='libx264',
        quality=9,
        pixelformat='yuv420p',
        macro_block_size=None
    )

    writer_1080p = imageio.get_writer(
        video_path_1080p,
        fps=fps,
        codec='libx264',
        quality=9,
        pixelformat='yuv420p',
        macro_block_size=None
    )

    t_start = time.time()

    # Pre-calculate Diya glow distance array
    diya_dist = np.sqrt((X - flame_x)**2 + (Y - flame_y)**2)
    diya_base_glow = np.exp(-diya_dist / 68.0)

    # 8. Frame Rendering Loop
    for frame_idx in range(total_frames):
        t = frame_idx / fps
        t_norm = frame_idx / total_frames

        # --- A. Chakra Rotation (Slow Clockwise) ---
        # 360 degrees / 24 seconds = 15 deg/sec -> in 12s, rotates 180 degrees
        chakra_angle_deg = 15.0 * t

        # --- B. Divine Radiance Progression ---
        # Starts at 1.0, increases smoothly to 1.45 at t=10s, holds peaceful darshan to 12s
        if t <= 9.5:
            radiance = 1.0 + 0.45 * ((t / 9.5) ** 1.3)
        else:
            # Steady blissful peak darshan
            radiance = 1.45

        # Diya introduction: kindles gracefully in first 1.5 seconds
        diya_intro = min(1.0, t / 1.5)
        diya_intro = 3 * diya_intro**2 - 2 * diya_intro**3 # smoothstep

        # --- C. Divine Light Rays Layer ---
        # 16 divine rays with subtle slow sweep and breathing
        ray_rot = 0.04 * t
        ray_pattern = (np.cos(16 * (angle_rays - ray_rot)) * 0.5 + 0.5) ** 3.5
        ray_breathe = 1.0 + 0.18 * math.sin(2.2 * t)
        ray_strength = ray_pattern * ray_falloff * ray_breathe * (radiance * 0.95)

        # Build Background with Rays
        # Ambient golden rays color: luminous sacred amber-gold
        frame_bg = bg_arr.copy()
        frame_bg[..., 0] = np.clip(frame_bg[..., 0] + ray_strength * 180.0, 0, 255)
        frame_bg[..., 1] = np.clip(frame_bg[..., 1] + ray_strength * 135.0, 0, 255)
        frame_bg[..., 2] = np.clip(frame_bg[..., 2] + ray_strength * 45.0, 0, 255)

        bg_current = Image.fromarray(np.uint8(frame_bg))

        # --- D. Paste Rotated Chakra ---
        # Negative angle for clockwise rotation in PIL
        rot_chakra = chakra_sprite.rotate(-chakra_angle_deg, resample=Image.BICUBIC)
        bg_current.paste(rot_chakra, (box_x0, box_y0), rot_chakra)

        # --- E. Composite Stationary Inner Sanctuary (Maa's Sacred Feet) ---
        # Maa's feet stay 100% anatomically stationary and pristine
        frame_img = Image.composite(img_circ, bg_current, inner_sanctuary_mask)

        # --- F. Living Golden Diya Flame & Warm Halo ---
        # Organic harmonic living flame breathing
        flicker_h = 1.0 + 0.08 * math.sin(7.3 * t) + 0.04 * math.sin(13.1 * t) + 0.02 * math.sin(23.7 * t)
        flicker_x = 1.2 * math.sin(5.7 * t) + 0.7 * math.sin(11.2 * t)
        flame_current_x = flame_x + flicker_x
        flame_current_y = flame_y

        # Dynamic warm illumination on surrounding lotus petals and diya
        diya_pulse = (0.88 + 0.14 * math.sin(6.1 * t)) * diya_intro
        diya_glow_intensity = diya_base_glow * diya_pulse

        arr_frame = np.array(frame_img, dtype=float)
        arr_frame[..., 0] = np.clip(arr_frame[..., 0] + diya_glow_intensity * 230.0, 0, 255)
        arr_frame[..., 1] = np.clip(arr_frame[..., 1] + diya_glow_intensity * 170.0, 0, 255)
        arr_frame[..., 2] = np.clip(arr_frame[..., 2] + diya_glow_intensity * 40.0, 0, 255)

        frame_img = Image.fromarray(np.uint8(arr_frame))
        draw = ImageDraw.Draw(frame_img, 'RGBA')

        # Draw Living Diya Flame (Inner core + outer golden mantle)
        if diya_intro > 0.05:
            fl_w = 9.0 * flicker_h * diya_intro
            fl_h = 24.0 * flicker_h * diya_intro
            
            # Outer golden-saffron flame
            outer_flame_poly = [
                (flame_current_x, flame_current_y - fl_h),
                (flame_current_x + fl_w * 0.5, flame_current_y - fl_h * 0.55),
                (flame_current_x + fl_w * 0.7, flame_current_y - fl_h * 0.15),
                (flame_current_x + fl_w * 0.35, flame_current_y + 3),
                (flame_current_x - fl_w * 0.35, flame_current_y + 3),
                (flame_current_x - fl_w * 0.7, flame_current_y - fl_h * 0.15),
                (flame_current_x - fl_w * 0.5, flame_current_y - fl_h * 0.55),
            ]
            draw.polygon(outer_flame_poly, fill=(255, 175, 25, int(230 * diya_intro)))

            # Inner intense golden-white flame core
            core_w = fl_w * 0.45
            core_h = fl_h * 0.65
            inner_flame_poly = [
                (flame_current_x, flame_current_y - core_h),
                (flame_current_x + core_w * 0.5, flame_current_y - core_h * 0.5),
                (flame_current_x + core_w * 0.6, flame_current_y - core_h * 0.15),
                (flame_current_x + core_w * 0.3, flame_current_y + 1),
                (flame_current_x - core_w * 0.3, flame_current_y + 1),
                (flame_current_x - core_w * 0.6, flame_current_y - core_h * 0.15),
                (flame_current_x - core_w * 0.5, flame_current_y - core_h * 0.5),
            ]
            draw.polygon(inner_flame_poly, fill=(255, 255, 230, int(250 * diya_intro)))

            # Delicate white-hot central wick spark
            draw.ellipse([flame_current_x - 2, flame_current_y - core_h * 0.4, flame_current_x + 2, flame_current_y], fill=(255, 255, 255, int(255 * diya_intro)))

        # --- G. Render Subtle Golden Prana Particles ---
        for p in particles:
            py = (p['y0'] + p['vy'] * t) % (h_circ + 60) - 30
            px = p['x0'] + p['vx_amp'] * math.sin(p['vx_freq'] * t + p['vx_phase'])
            
            twinkle = (math.sin(p['twinkle_freq'] * t + p['twinkle_phase']) * 0.5 + 0.5) ** 2
            alpha = int(twinkle * 220 * min(1.0, radiance * 0.9))
            
            if alpha > 15:
                r = p['radius']
                if p['is_orb']:
                    # Soft golden orb
                    draw.ellipse([px - r, py - r, px + r, py + r], fill=(255, 225, 120, int(alpha * 0.6)))
                    draw.ellipse([px - r*0.5, py - r*0.5, px + r*0.5, py + r*0.5], fill=(255, 255, 210, alpha))
                else:
                    # Sharp golden sparkle
                    draw.ellipse([px - r, py - r, px + r, py + r], fill=(255, 255, 220, alpha))
                    # Subtle micro cross-sparkle
                    draw.line([px - r*2, py, px + r*2, py], fill=(255, 235, 150, int(alpha * 0.7)), width=1)
                    draw.line([px, py - r*2, px, py + r*2], fill=(255, 235, 150, int(alpha * 0.7)), width=1)

        # --- H. Render 3D Floating Red Rose Petals ---
        for p in petals:
            # Vertical travel with seamless continuous wrap
            py = (p['y0'] + p['speed_y'] * t) % (h_circ + 100) - 50
            px = p['x0'] + p['sway_amp'] * math.sin(p['sway_freq'] * t + p['sway_phase'])
            
            # 3D tumbling scales
            pitch_scale = math.cos(p['pitch_freq'] * t + p['pitch_phase'])
            roll_scale = math.cos(p['roll_freq'] * t + p['roll_phase'])
            curr_rot = p['rot_init'] + p['rot_speed'] * t
            
            # Effective size
            scale_x = abs(roll_scale) * p['depth']
            scale_y_petal = abs(pitch_scale) * p['depth']
            
            # Minimum size threshold for visibility
            pw = max(10, int(60 * scale_x))
            ph = max(10, int(70 * scale_y_petal))
            
            # Resize and rotate petal
            petal_thumb = base_petal_sprite.resize((pw, ph), resample=Image.BICUBIC)
            petal_rot = petal_thumb.rotate(curr_rot, resample=Image.BICUBIC, expand=True)
            
            # Modulate alpha based on depth and facing
            alpha_val = p['opacity'] * (0.85 + 0.15 * math.sin(curr_rot * 0.05))
            
            # Drop shadow onto scene for 3D depth
            shadow_offset = int(6 * p['depth'])
            shadow_mask = petal_rot.split()[3]
            shadow_alpha = shadow_mask.point(lambda a: int(a * 0.28))
            shadow_img = Image.new('RGBA', petal_rot.size, (20, 8, 0, 0))
            shadow_img.putalpha(shadow_alpha)
            
            frame_img.paste(shadow_img, (int(px - petal_rot.width/2 + shadow_offset), int(py - petal_rot.height/2 + shadow_offset)), shadow_img)
            
            # Paste petal
            frame_img.paste(petal_rot, (int(px - petal_rot.width/2), int(py - petal_rot.height/2)), petal_rot)

        # --- I. Gradually Increasing Golden Radiance (Global Aura & Bloom) ---
        # Restore original aspect ratio (1024x800)
        final_frame_img = frame_img.resize((orig_w, orig_h), resample=Image.BICUBIC)
        
        arr_final = np.array(final_frame_img, dtype=float)
        
        # Golden radiance bloom factor
        extra_radiance = max(0.0, radiance - 1.0)
        if extra_radiance > 0.01:
            # Soft golden light wash: boost warm tones gracefully
            arr_final[..., 0] = np.clip(arr_final[..., 0] * (1.0 + 0.12 * extra_radiance) + 18.0 * extra_radiance, 0, 255)
            arr_final[..., 1] = np.clip(arr_final[..., 1] * (1.0 + 0.09 * extra_radiance) + 12.0 * extra_radiance, 0, 255)
            arr_final[..., 2] = np.clip(arr_final[..., 2] * (1.0 + 0.03 * extra_radiance) + 2.0 * extra_radiance, 0, 255)

        frame_rgb = np.uint8(arr_final[..., :3])

        # Write to Centered 1024x800 MP4
        writer_centered.append_data(frame_rgb)

        # --- J. Generate 1920x1080 Full HD Cinematic Master ---
        # Seamlessly centered in 1920x1080 canvas with warm golden aura background
        hd_canvas = Image.new('RGB', (1920, 1080), (242, 138, 5))
        
        # Create subtle widescreen golden background gradient
        # Center of 1920x1080 is (960, 540)
        # Scale the 1024x800 image smoothly to 1382x1080 (fitting height) or composite centered
        scaled_w = int(orig_w * (1080.0 / orig_h))
        scaled_h = 1080
        scaled_frame = Image.fromarray(frame_rgb).resize((scaled_w, scaled_h), resample=Image.BICUBIC)
        
        # Center horizontally: offset = (1920 - 1382) // 2 = 269
        offset_x = (1920 - scaled_w) // 2
        hd_canvas.paste(scaled_frame, (offset_x, 0))
        
        # Smoothly feather edges into the background if needed
        hd_frame_rgb = np.array(hd_canvas)
        writer_1080p.append_data(hd_frame_rgb)

        # Save poster at peak darshan frame
        if frame_idx == total_frames - 30:
            Image.fromarray(frame_rgb).save(poster_path)
            print(f"Saved high-res darshan poster to: {poster_path}")

        # Progress reporting
        if (frame_idx + 1) % 45 == 0 or frame_idx == total_frames - 1:
            elapsed = time.time() - t_start
            fps_render = (frame_idx + 1) / elapsed
            eta = (total_frames - (frame_idx + 1)) / max(0.1, fps_render)
            print(f"Rendered [{frame_idx + 1:3d}/{total_frames}] frames ({(frame_idx + 1)/total_frames*100:5.1f}%) | "
                  f"Speed: {fps_render:4.1f} fps | Elapsed: {elapsed:4.1f}s | ETA: {eta:4.1f}s")

    writer_centered.close()
    writer_1080p.close()
    total_time = time.time() - t_start
    print("=" * 60)
    print(f"Animation rendering complete in {total_time:.1f}s!")
    print(f"Output 1: {video_path_centered} ({os.path.getsize(video_path_centered) / 1024:.1f} KB)")
    print(f"Output 2: {video_path_1080p} ({os.path.getsize(video_path_1080p) / 1024:.1f} KB)")
    print(f"Poster:   {poster_path} ({os.path.getsize(poster_path) / 1024:.1f} KB)")
    print("=" * 60)

if __name__ == "__main__":
    generate_animation()

