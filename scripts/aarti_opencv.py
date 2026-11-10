"""
Shree Maha Lakshmi Virtual Aarti Room - Standalone OpenCV Hand Gesture Tracking
Run this desktop app with: python aarti_opencv.py
Requirements: pip install opencv-python numpy
"""

import sys
import math
import time
import random
import numpy as np

def run_aarti_desktop():
    try:
        import cv2
    except ImportError:
        print("\n[!] OpenCV is not installed yet.")
        print("    Install it on your computer with:")
        print("    pip install opencv-python\n")
        print("    Alternatively, you can run the interactive web version immediately")
        print("    by double-clicking 'index.html' in your browser!\n")
        return

    print("=" * 60)
    print("Shree Maha Lakshmi Virtual Aarti Room - OpenCV Hand Tracking")
    print("Move your hand in gentle clockwise circles to perform Maa's Aarti!")
    print("Press 'q' or 'ESC' to exit.")
    print("=" * 60)

    # 1. Load Maa Lakshmi Image
    img_path = 'maa_laxmi_darshan.jpg'
    deity_img = cv2.imread(img_path)
    if deity_img is None:
        print(f"[!] Could not find '{img_path}'. Creating divine backdrop...")
        deity_img = np.zeros((720, 600, 3), dtype=np.uint8)
        deity_img[:] = (20, 10, 4)

    dh, dw = deity_img.shape[:2]
    # Resize deity to comfortable window size
    target_h = 700
    target_w = int(dw * (target_h / dh))
    deity_img = cv2.resize(deity_img, (target_w, target_h))

    # 2. Setup Webcam Capture
    cap = cv2.VideoCapture(0)
    has_cam = cap.isOpened()
    if not has_cam:
        print("[!] No webcam detected. Running in Demo / Mouse mode.")

    # 3. Canvas setup: Screen with Deity in Center and Webcam PiP
    canvas_w = target_w + 340
    canvas_h = target_h

    # Flower and Coin particle systems
    petals = []
    for _ in range(35):
        petals.append({
            'x': random.uniform(0, target_w),
            'y': random.uniform(0, target_h),
            'vy': random.uniform(1.8, 3.8),
            'vx': random.uniform(-0.5, 1.2),
            'r': random.uniform(5, 11),
            'color': random.choice([(40, 40, 220), (140, 80, 240), (20, 140, 255)]) # BGR
        })

    coins = []
    pot_x, pot_y = int(target_w * 0.38), int(target_h * 0.62)
    for _ in range(25):
        coins.append({
            'x': pot_x + random.uniform(-15, 15),
            'y': pot_y + random.uniform(0, target_h - pot_y),
            'vy': random.uniform(2.5, 5.0),
            'vx': random.uniform(-1.0, 2.0),
            'r': random.uniform(6, 11)
        })

    # Aarti Thali Position
    thali_x, thali_y = target_w // 2, int(target_h * 0.72)
    target_tx, target_ty = thali_x, thali_y

    sparkles = []
    completed_rounds = 0
    prev_angle = None
    cumulative_angle = 0

    cv2.namedWindow("Maa Lakshmi Virtual Aarti Room", cv2.WINDOW_AUTOSIZE)

    # Mouse Callback for fallback control
    def on_mouse(event, x, y, flags, param):
        nonlocal target_tx, target_ty
        if event == cv2.EVENT_MOUSEMOVE and not has_cam:
            target_tx = min(target_w - 50, max(50, x))
            target_ty = min(target_h - 50, max(50, y))

    cv2.setMouseCallback("Maa Lakshmi Virtual Aarti Room", on_mouse)

    t_start = time.time()

    while True:
        # Create blank display canvas
        canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)
        canvas[:, :] = (12, 5, 2) # Deep temple dark saffron

        # Blit Maa Lakshmi onto canvas
        canvas[:target_h, :target_w] = deity_img.copy()

        # Webcam frame processing
        cam_frame_display = None
        if has_cam:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1) # Mirror
                cam_h, cam_w = frame.shape[:2]

                # Hand Detection via HSV Skin Color Thresholding
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # Typical skin color range in HSV
                lower_skin = np.array([0, 30, 60], dtype=np.uint8)
                upper_skin = np.array([25, 255, 255], dtype=np.uint8)
                mask = cv2.inRange(hsv, lower_skin, upper_skin)
                
                # Morphological noise cleanup
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
                mask = cv2.erode(mask, kernel, iterations=1)
                mask = cv2.dilate(mask, kernel, iterations=2)

                # Find contours
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    max_c = max(contours, key=cv2.contourArea)
                    if cv2.contourArea(max_c) > 1200:
                        M = cv2.moments(max_c)
                        if M["m00"] > 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])

                            # Map webcam (cx, cy) to deity area
                            norm_x = cx / cam_w
                            norm_y = cy / cam_h
                            target_tx = int(norm_x * target_w)
                            target_ty = int(norm_y * target_h)

                            # Draw tracking indicator on cam preview
                            cv2.circle(frame, (cx, cy), 15, (0, 255, 100), 2)
                            cv2.circle(frame, (cx, cy), 4, (0, 215, 255), -1)

                cam_frame_display = cv2.resize(frame, (300, 225))

        # Smooth Aarti Thali lerp
        thali_x += int((target_tx - thali_x) * 0.25)
        thali_y += int((target_ty - thali_y) * 0.25)

        # Track Circular Motion around center
        center_x, center_y = target_w // 2, target_h // 2
        angle = math.atan2(thali_y - center_y, thali_x - center_x)
        if prev_angle is not None:
            delta = angle - prev_angle
            if delta > math.PI: delta -= 2 * math.PI
            if delta < -math.PI: delta += 2 * math.PI
            if delta > 0: # Clockwise
                cumulative_angle += delta
                if cumulative_angle >= 2 * math.PI:
                    cumulative_angle -= 2 * math.PI
                    completed_rounds += 1
        prev_angle = angle

        # 4. Render Falling Rose & Lotus Petals
        for p in petals:
            p['y'] += p['vy']
            p['x'] += p['vx'] + math.sin(p['y'] * 0.03) * 0.6
            if p['y'] > target_h + 15:
                p['y'] = -10
                p['x'] = random.uniform(0, target_w)
            
            ix, iy = int(p['x']), int(p['y'])
            if 0 <= ix < target_w and 0 <= iy < target_h:
                cv2.ellipse(canvas, (ix, iy), (int(p['r']), int(p['r']*0.6)), int(p['y']*2), 0, 360, p['color'], -1)

        # 5. Render Dhan Varsha Gold Coins from Pot
        for c in coins:
            c['y'] += c['vy']
            c['x'] += c['vx']
            if c['y'] > target_h + 15:
                c['y'] = pot_y + random.uniform(-10, 10)
                c['x'] = pot_x + random.uniform(-15, 15)
            
            ix, iy = int(c['x']), int(c['y'])
            if 0 <= ix < target_w and 0 <= iy < target_h:
                cv2.circle(canvas, (ix, iy), int(c['r']), (0, 215, 255), -1) # Gold
                cv2.circle(canvas, (ix, iy), int(c['r']), (20, 140, 180), 1)

        # 6. Aarti Sparkle Trail
        sparkles.append({'x': thali_x + random.randint(-15, 15), 'y': thali_y + random.randint(-15, 15), 'life': 20})
        for s in sparkles[:]:
            s['life'] -= 1
            if s['life'] <= 0:
                sparkles.remove(s)
            else:
                alpha = s['life'] / 20.0
                radius = int(3 * alpha) + 1
                if 0 <= s['x'] < target_w and 0 <= s['y'] < target_h:
                    cv2.circle(canvas, (s['x'], s['y']), radius, (50, 230, 255), -1)

        # 7. Render Aarti Thali
        cv2.circle(canvas, (thali_x, thali_y), 45, (30, 160, 215), -1) # Brass plate
        cv2.circle(canvas, (thali_x, thali_y), 45, (100, 220, 255), 3) # Golden rim
        cv2.circle(canvas, (thali_x, thali_y), 32, (10, 120, 180), 2)

        # 5 Sacred Ghee Flames
        flame_offsets = [(0, -28), (28, 0), (0, 28), (-28, 0), (0, 0)]
        for idx, (ox, oy) in enumerate(flame_offsets):
            fx = thali_x + ox
            fy = thali_y + oy
            # Inner flame
            cv2.ellipse(canvas, (fx, fy), (5, 9), 0, 0, 360, (0, 140, 255), -1)
            cv2.ellipse(canvas, (fx, fy-2), (2, 5), 0, 0, 360, (180, 255, 255), -1)

        # 8. Render Right Side Info Panel
        panel_x = target_w + 20
        cv2.putText(canvas, "Maha Lakshmi Aarti", (panel_x, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 215, 255), 2)
        cv2.putText(canvas, f"Aarti Rounds: {completed_rounds} / 7", (panel_x, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 240, 255), 2)
        cv2.putText(canvas, "Status: Active Darshan", (panel_x, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 120), 1)

        # Blit Webcam Preview in Panel
        if cam_frame_display is not None:
            canvas[150:150+225, panel_x:panel_x+300] = cam_frame_display
            cv2.rectangle(canvas, (panel_x, 150), (panel_x+300, 150+225), (0, 215, 255), 2)
            cv2.putText(canvas, "Camera Hand Tracking", (panel_x+10, 150+215), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        else:
            cv2.rectangle(canvas, (panel_x, 150), (panel_x+300, 150+225), (40, 30, 20), -1)
            cv2.putText(canvas, "Move Mouse in Circles", (panel_x+40, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (100, 200, 255), 1)

        # Instructions
        cv2.putText(canvas, "Instructions:", (panel_x, 410), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 215, 255), 1)
        cv2.putText(canvas, "- Move hand in clock-wise", (panel_x, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 200, 220), 1)
        cv2.putText(canvas, "  circles around Maa", (panel_x, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 200, 220), 1)
        cv2.putText(canvas, "- Complete 7 sacred rounds", (panel_x, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 200, 220), 1)
        cv2.putText(canvas, "- Press 'q' to Exit", (panel_x, 530), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120, 120, 255), 1)

        if completed_rounds >= 7:
            cv2.putText(canvas, "AARTI COMPLETED!", (target_w // 2 - 140, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 100), 2)

        cv2.imshow("Maa Lakshmi Virtual Aarti Room", canvas)
        key = cv2.waitKey(20) & 0xFF
        if key == ord('q') or key == 27:
            break

    if has_cam:
        cap.release()
    cv2.destroyAllWindows()
    print("Maa Lakshmi Aarti concluded peacefully. Har Har Mahadev • Shubham Bhavatu!")

if __name__ == '__main__':
    run_aarti_desktop()

