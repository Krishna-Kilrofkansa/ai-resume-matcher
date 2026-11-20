import os
import sys
import time
import socket
import subprocess
import numpy as np
import cv2
import av
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_services(timeout=60):
    start = time.time()
    backend_ok = False
    frontend_ok = False
    while time.time() - start < timeout:
        if not backend_ok:
            try:
                with socket.create_connection(('127.0.0.1', 8000), timeout=1):
                    backend_ok = True
                    print("  ✓ Backend is up on port 8000")
            except Exception:
                pass
        if not frontend_ok:
            for host in ['127.0.0.1', 'localhost']:
                try:
                    with socket.create_connection((host, 5173), timeout=1):
                        frontend_ok = True
                        print(f"  ✓ Frontend is up on port 5173 ({host})")
                        break
                except Exception:
                    pass
        if backend_ok and frontend_ok:
            return True
        time.sleep(1)
    if not backend_ok:
        print("  ✗ Backend failed to bind port 8000 within timeout")
    if not frontend_ok:
        print("  ✗ Frontend failed to bind port 5173 within timeout")
    return False

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    demo_dir = os.path.join(root_dir, 'demo')
    os.makedirs(demo_dir, exist_ok=True)
    mp4_path = os.path.join(demo_dir, 'ai_resume_matcher_demo.mp4')

    print("[1/5] Starting Backend & Frontend servers...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--app-dir", "backend", "--host", "127.0.0.1", "--port", "8000"],
        cwd=root_dir
    )

    frontend_proc = subprocess.Popen(
        ["npm.cmd", "run", "dev"],
        cwd=os.path.join(root_dir, "frontend")
    )

    try:
        print("[2/5] Waiting for servers to be ready...")
        if not wait_for_services(timeout=60):
            raise RuntimeError("One or more services failed to start within 60s")
        print("  ✓ All services ready.")

        # Setup PyAV Container for MP4 H.264
        width = 1280
        height = 800
        fps = 15
        container = av.open(mp4_path, mode='w')
        stream = container.add_stream('h264', rate=fps)
        stream.width = width
        stream.height = height
        stream.pix_fmt = 'yuv420p'
        stream.options = {'crf': '23', 'preset': 'veryfast'}

        # Setup Chrome
        print("[3/5] Launching Headless Chrome Browser...")
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument(f'--window-size={width},{height}')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--hide-scrollbars')

        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(width, height)

        frames_recorded = 0
        gif_frames = []

        def capture_frames(count=1, delay=0.05):
            nonlocal frames_recorded
            for _ in range(count):
                png_bytes = driver.get_screenshot_as_png()
                img = cv2.imdecode(np.frombuffer(png_bytes, np.uint8), cv2.IMREAD_COLOR)
                if img.shape[0] != height or img.shape[1] != width:
                    img = cv2.resize(img, (width, height))
                frame = av.VideoFrame.from_ndarray(img, format='bgr24')
                for packet in stream.encode(frame):
                    container.mux(packet)
                
                # Sample every 3rd frame for GIF
                if frames_recorded % 3 == 0:
                    rgb = cv2.cvtColor(cv2.resize(img, (800, 500)), cv2.COLOR_BGR2RGB)
                    gif_frames.append(Image.fromarray(rgb).quantize(colors=128))
                
                frames_recorded += 1
                if delay > 0:
                    time.sleep(delay)

        def smooth_scroll(start_y, target_y, steps=15):
            for y in np.linspace(start_y, target_y, steps):
                driver.execute_script(f"window.scrollTo(0, {y});")
                capture_frames(1, delay=0.03)

        print("[4/5] Executing and recording automated demo scenario...")
        driver.get('http://localhost:5173')
        time.sleep(1.5)
        capture_frames(25, delay=0.04) # Initial view

        # Step 1: Click "Extract JD Criteria"
        print("  -> Step 1: Extract JD Criteria")
        extract_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Extract JD Criteria')]"))
        )
        extract_btn.click()
        capture_frames(20, delay=0.05)

        # Expand skills "+9 more"
        try:
            more_btn = driver.find_element(By.XPATH, "//button[contains(text(), '+') and contains(text(), 'more')]")
            more_btn.click()
            capture_frames(15, delay=0.05)
        except Exception:
            pass

        # Step 2: Click "Load 19 Real Multi-Page Resumes"
        print("  -> Step 2: Load 19 Real Multi-Page Resumes & Run AI Matching")
        load_samples_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Load 19 Real Multi-Page Resumes')]")
        load_samples_btn.click()
        
        # Capture loading animation while backend processes the 19 resumes
        start_wait = time.time()
        while time.time() - start_wait < 35:
            capture_frames(2, delay=0.1)
            # Check if rankings table appeared
            rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
            if len(rows) > 0:
                print(f"  ✓ {len(rows)} candidates ranked and rendered!")
                break
        
        capture_frames(25, delay=0.04)

        # Step 3: Smooth scroll to rankings table
        print("  -> Step 3: Inspect Candidate Rankings Dashboard")
        smooth_scroll(0, 320, steps=20)
        capture_frames(20, delay=0.04)

        # Step 4: Expand "+N more" skills in candidate row
        try:
            cand_more = driver.find_element(By.XPATH, "//tbody//button[contains(text(), '+') and contains(text(), 'more')]")
            cand_more.click()
            capture_frames(15, delay=0.05)
        except Exception as e:
            print("  Note: candidate more button not clicked:", e)

        # Step 5: Test Min Match slider filter
        print("  -> Step 5: Test Min Match Score slider filter")
        try:
            slider = driver.find_element(By.CSS_SELECTOR, "input[type='range']")
            for val in [30, 50, 70, 80]:
                driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", slider, val)
                capture_frames(10, delay=0.04)
            # Reset to 0
            driver.execute_script("arguments[0].value = 0; arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", slider)
            capture_frames(15, delay=0.04)
        except Exception as e:
            print("  Slider test note:", e)

        # Step 6: Test Search Filter
        print("  -> Step 6: Test Search Filter")
        try:
            search_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Filter name']")
            
            def set_search(text):
                driver.execute_script(
                    "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change', { bubbles: true })); arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                    search_input, text
                )

            set_search("Software")
            capture_frames(12, delay=0.04)
            set_search("Python")
            capture_frames(12, delay=0.04)
            set_search("")
            capture_frames(12, delay=0.04)
        except Exception as e:
            print("  Search test note:", e)

        # Step 7: Inspect Top Candidate (Module 5 Drawer)
        print("  -> Step 7: Open Candidate Deep Analysis Drawer (Module 5)")
        try:
            first_inspect = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//tbody//tr[1]//button[contains(text(), 'Inspect')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_inspect)
            capture_frames(5, delay=0.04)
            driver.execute_script("arguments[0].click();", first_inspect)
            
            # Wait for drawer
            drawer = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".drawer"))
            )
            capture_frames(25, delay=0.04)

            # Scroll inside drawer to see 4-pillar breakdown, skills gap & citations
            for y in [120, 260, 420, 600]:
                driver.execute_script("arguments[0].scrollTop = arguments[1];", drawer, y)
                capture_frames(12, delay=0.04)
            capture_frames(20, delay=0.04)
            
            # Scroll back up in drawer
            driver.execute_script("arguments[0].scrollTop = 0;", drawer)
            capture_frames(10, delay=0.04)

            # Close drawer
            close_btn = driver.find_element(By.CSS_SELECTOR, ".drawer button")
            driver.execute_script("arguments[0].click();", close_btn)
            capture_frames(15, delay=0.04)
        except Exception as e:
            print("  Drawer inspection note:", e)

        # Smooth scroll back to header
        smooth_scroll(320, 0, steps=15)
        capture_frames(25, delay=0.04)

        # Finalize Video
        print("[5/5] Flushing video packets...")
        for packet in stream.encode():
            container.mux(packet)
        container.close()
        driver.quit()

        print(f"✓ Video successfully generated: {mp4_path}")
        print(f"  Total frames: {frames_recorded} ({frames_recorded / fps:.1f} seconds)")
        print(f"  File size: {os.path.getsize(mp4_path) / (1024*1024):.2f} MB")

        # Save GIF Preview
        gif_path = os.path.join(demo_dir, 'demo_preview.gif')
        if gif_frames:
            print(f"Saving animated GIF preview ({len(gif_frames)} frames)...")
            gif_frames[0].save(
                gif_path,
                save_all=True,
                append_images=gif_frames[1:],
                duration=int(1000 / (fps / 3)),
                loop=0,
                optimize=True
            )
            print(f"✓ GIF preview generated: {gif_path} ({os.path.getsize(gif_path) / (1024*1024):.2f} MB)")

    finally:
        print("Terminating background servers...")
        try:
            backend_proc.terminate()
            backend_proc.wait(timeout=3)
        except Exception:
            backend_proc.kill()
        try:
            frontend_proc.terminate()
            frontend_proc.wait(timeout=3)
        except Exception:
            frontend_proc.kill()

if __name__ == '__main__':
    main()
