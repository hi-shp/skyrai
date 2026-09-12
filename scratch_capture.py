"""
SKYRAI high-quality interactive walkthrough recorder.
Full 1920x1080 capture, 8 FPS, 256-color palette, realistic mouse interactions.
"""
import os, time, io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from PIL import Image

W, H = 1920, 1080
FPS = 8
FRAME_MS = 1000 // FPS  # 125ms per frame
OUT_W, OUT_H = 1440, 810  # high resolution output

os.makedirs('assets', exist_ok=True)

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument(f'--window-size={W},{H}')
opts.add_argument('--disable-gpu')
opts.add_argument('--no-sandbox')
opts.add_argument('--hide-scrollbars')
opts.add_argument('--force-device-scale-factor=1')

driver = webdriver.Chrome(options=opts)
frames = []


def snap():
    png = driver.get_screenshot_as_png()
    img = Image.open(io.BytesIO(png)).convert('RGB').resize((OUT_W, OUT_H), Image.Resampling.LANCZOS)
    frames.append(img)


def snap_n(n):
    for _ in range(n):
        snap()


def hover_and_snap(element, n=2):
    ActionChains(driver).move_to_element(element).perform()
    time.sleep(0.15)
    snap_n(n)


try:
    # ── 1. Load page (zoom 14) ──
    print('1. Loading page...')
    driver.get('http://localhost:8000/skyrai.html')
    time.sleep(4)
    snap_n(10)  # hold initial view ~1.25s

    # ── 2. Click Plot 2 ──
    print('2. Switching to Plot 2...')
    driver.execute_script("""
        var items = document.querySelectorAll('.field-item');
        if (items.length > 1) items[1].click();
    """)
    time.sleep(2)
    snap_n(10)

    # ── 3. Click Plot 3 ──
    print('3. Switching to Plot 3...')
    driver.execute_script("""
        var items = document.querySelectorAll('.field-item');
        if (items.length > 2) items[2].click();
    """)
    time.sleep(2)
    snap_n(8)

    # ── 4. Back to Plot 1 ──
    print('4. Back to Plot 1...')
    driver.execute_script("""
        var items = document.querySelectorAll('.field-item');
        if (items.length > 0) items[0].click();
    """)
    time.sleep(2)
    snap_n(8)

    # ── 5. Tilt 30 ──
    print('5. Tilting to 30...')
    btn30 = driver.find_element(By.ID, 'btn-tilt-30')
    hover_and_snap(btn30, 3)
    btn30.click()
    time.sleep(0.8)
    snap_n(8)

    # ── 6. Tilt 45 ──
    print('6. Tilting to 45...')
    btn45 = driver.find_element(By.ID, 'btn-tilt-45')
    hover_and_snap(btn45, 2)
    btn45.click()
    time.sleep(0.8)
    snap_n(10)

    # ── 7. Tilt 60 ──
    print('7. Tilting to 60...')
    btn60 = driver.find_element(By.ID, 'btn-tilt-60')
    hover_and_snap(btn60, 2)
    btn60.click()
    time.sleep(0.8)
    snap_n(8)

    # ── 8. Back to 45 then switch NDRE ──
    print('8. NDRE Nitrogen...')
    btn45.click()
    time.sleep(0.5)
    snap_n(4)

    ndre_el = driver.find_element(By.CSS_SELECTOR, '[data-layer="ndre"]')
    hover_and_snap(ndre_el, 3)
    ndre_el.click()
    time.sleep(1.5)
    snap_n(10)

    # ── 9. NDWI ──
    print('9. NDWI Moisture...')
    ndwi_el = driver.find_element(By.CSS_SELECTOR, '[data-layer="ndwi"]')
    hover_and_snap(ndwi_el, 3)
    ndwi_el.click()
    time.sleep(1.5)
    snap_n(10)

    # ── 10. Soil Moisture ──
    print('10. Soil Moisture...')
    moist_el = driver.find_element(By.CSS_SELECTOR, '[data-layer="moisture"]')
    hover_and_snap(moist_el, 3)
    moist_el.click()
    time.sleep(1.5)
    snap_n(8)

    # ── 11. Growth Stress ──
    print('11. Growth Stress...')
    stress_el = driver.find_element(By.CSS_SELECTOR, '[data-layer="stress"]')
    hover_and_snap(stress_el, 3)
    stress_el.click()
    time.sleep(1.5)
    snap_n(8)

    # ── 12. EVI ──
    print('12. EVI...')
    evi_el = driver.find_element(By.CSS_SELECTOR, '[data-layer="evi"]')
    hover_and_snap(evi_el, 2)
    evi_el.click()
    time.sleep(1.5)
    snap_n(8)

    # ── 13. Back to NDVI, reset tilt ──
    print('13. Back to NDVI flat...')
    ndvi_el = driver.find_element(By.CSS_SELECTOR, '[data-layer="ndvi"]')
    hover_and_snap(ndvi_el, 2)
    ndvi_el.click()
    time.sleep(1)
    snap_n(4)

    btn0 = driver.find_element(By.ID, 'btn-tilt-0')
    hover_and_snap(btn0, 2)
    btn0.click()
    time.sleep(0.8)
    snap_n(8)

    # ── 14. Scroll right panel to prescription ──
    print('14. Scrolling prescription...')
    driver.execute_script("document.querySelector('.dashboard').scrollTop = 450;")
    time.sleep(0.8)
    snap_n(8)

    driver.execute_script("document.querySelector('.dashboard').scrollTop = 950;")
    time.sleep(0.8)
    snap_n(8)

    driver.execute_script("document.querySelector('.dashboard').scrollTop = 0;")
    time.sleep(0.5)
    snap_n(4)

    # ── 15. Navigate to Dashboard ──
    print('15. Dashboard...')
    dash_link = driver.find_element(By.CSS_SELECTOR, '.nav-dashboard-link')
    hover_and_snap(dash_link, 3)
    dash_link.click()
    time.sleep(3)
    snap_n(12)

    # ── 16. Save individual screenshots ──
    print('16. Saving screenshots...')
    driver.save_screenshot('assets/skyrai_dashboard.png')

    driver.get('http://localhost:8000/skyrai.html')
    time.sleep(3.5)
    driver.save_screenshot('assets/skyrai_gis_overview.png')

    driver.execute_script('set3DTiltAngle(45);')
    time.sleep(1.5)
    driver.save_screenshot('assets/skyrai_3d_perspective.png')

    driver.execute_script('switchLayer("ndre");')
    time.sleep(1.5)
    driver.save_screenshot('assets/skyrai_ndre_nitrogen.png')

    driver.execute_script('switchLayer("ndwi");')
    time.sleep(1.5)
    driver.save_screenshot('assets/skyrai_ndwi_moisture.png')

    driver.execute_script('set3DTiltAngle(0); switchLayer("ndvi");')
    time.sleep(1.5)
    driver.save_screenshot('assets/skyrai_prescription.png')

    # ── 17. Build GIF ──
    print(f'Total frames: {len(frames)}')
    if frames:
        # 256 colors, full quality
        frames[0].save(
            'assets/skyrai_walkthrough.gif',
            save_all=True,
            append_images=frames[1:],
            duration=FRAME_MS,
            loop=0,
            optimize=False
        )
        raw_size = os.path.getsize('assets/skyrai_walkthrough.gif')
        print(f'Raw GIF: {raw_size:,} bytes ({raw_size/1024/1024:.1f} MB)')

        # If too large (>25MB), optimize with 192 colors
        if raw_size > 25 * 1024 * 1024:
            print('Optimizing...')
            opt_frames = []
            for f in frames:
                q = f.quantize(colors=192, method=Image.Quantize.MEDIANCUT).convert('RGB')
                opt_frames.append(q)
            opt_frames[0].save(
                'assets/skyrai_walkthrough.gif',
                save_all=True,
                append_images=opt_frames[1:],
                duration=FRAME_MS,
                loop=0,
                optimize=True
            )
            final_size = os.path.getsize('assets/skyrai_walkthrough.gif')
            print(f'Optimized GIF: {final_size:,} bytes ({final_size/1024/1024:.1f} MB)')
        else:
            print('Size OK, no optimization needed.')

    print('Done.')

finally:
    driver.quit()
