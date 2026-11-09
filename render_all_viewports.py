"""
Render All Responsive Viewports for Final Whole-Project Acceptance Audit
Generates:
1. Desktop 1920x1080 (16:9 Widescreen)
2. Laptop 1366x768 (16:9 Standard Laptop)
3. Mobile Portrait 412x915 (Android / Pixel Portrait)
4. Mobile Landscape 844x390 (iPhone Landscape)
5. Final Blessings Modal 1920x1080
"""

import os
import sys
from verify_phase4_phase5 import (
    WORKSPACE,
    render_phase4_interactive_scene,
    render_phase5_blessings_scene
)
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
import math
import random

def render_custom_viewport(width, height, is_mobile, output_name, desc):
    print(f"Rendering {desc}: {width}x{height} (Mobile={is_mobile})...")
    out_path = os.path.join(WORKSPACE, output_name)
    render_phase4_interactive_scene(out_path, is_mobile=is_mobile, custom_w=width, custom_h=height)
    # Also copy to artifact directory
    art_dir = r'C:\Users\pranjali\.gemini\antigravity\brain\8868637f-3187-40ed-a6d7-cdcf53be6fbc'
    dest_path = os.path.join(art_dir, output_name)
    import shutil
    shutil.copyfile(out_path, dest_path)
    print(f"Copied {output_name} to artifact directory.")

if __name__ == '__main__':
    render_custom_viewport(1920, 1080, False, 'desktop_1080p_aarti_preview.png', 'Desktop Widescreen')
    render_custom_viewport(1366, 768, False, 'laptop_768p_aarti_preview.png', 'Laptop Widescreen')
    render_custom_viewport(412, 915, True, 'mobile_portrait_aarti_preview.png', 'Mobile Portrait (412x915)')
    render_custom_viewport(844, 390, False, 'mobile_landscape_aarti_preview.png', 'Mobile Landscape (844x390)')
    
    # Also render final blessings modal
    bless_path = os.path.join(WORKSPACE, 'final_blessings_preview.png')
    render_phase5_blessings_scene(bless_path)
    art_dir = r'C:\Users\pranjali\.gemini\antigravity\brain\8868637f-3187-40ed-a6d7-cdcf53be6fbc'
    import shutil
    shutil.copyfile(bless_path, os.path.join(art_dir, 'final_blessings_preview.png'))
    print("All responsive viewports successfully rendered and synchronized!")
