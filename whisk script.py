# whisk_final_browser_stays_open.py
import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ---------- CONFIG ----------
# Make sure these paths are correct for your system
DRIVER_PATH = r"C:\Users\Abdulaziz\Downloads\edgedriver_win64\msedgedriver.exe"
PROMPTS_FILE = r"C:\Users\Abdulaziz\Documents\prompts.txt"
EDGE_PROFILE = r"C:\Users\Abdulaziz\AppData\Local\Microsoft\Edge\User Data"
PROFILE_DIR = "Default"
# ----------------------------

service = Service(DRIVER_PATH)
options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument(f"user-data-dir={EDGE_PROFILE}")
options.add_argument(f"profile-directory={PROFILE_DIR}")
options.add_argument("--start-maximized")

driver = webdriver.Edge(service=service, options=options)
wait = WebDriverWait(driver, 30)

driver.get("https://labs.google/fx/tools/whisk/project")

input("Please finish any manual login in the opened Edge window, then press Enter here to continue...")

# Single 5-second delay after login confirmation
print("\nLogin confirmed. Starting the first prompt in 5 seconds...")
time.sleep(5)


with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
    prompts = [line.strip() for line in f if line.strip()]

def find_textarea():
    """Finds the prompt input textarea using a list of fallback selectors."""
    candidates = [
        (By.ID, "nameInput"),
        (By.XPATH, "//textarea[contains(@placeholder,'Describe')]"),
        (By.CSS_SELECTOR, "textarea.sc-da7d3cfd-2"),
        (By.TAG_NAME, "textarea"),
    ]
    for by, sel in candidates:
        try:
            el = wait.until(EC.element_to_be_clickable((by, sel)))
            return el
        except TimeoutException:
            continue
    return None

def find_generate_button():
    """Finds the button using its specific aria-label and waits for it to be enabled."""
    try:
        button_xpath = "//button[@aria-label='Submit prompt' and not(@disabled)]"
        button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
        return button
    except TimeoutException:
        print("DEBUG: Timed out waiting for the button with aria-label='Submit prompt' to become clickable.")
        driver.save_screenshot("debug_button_not_found.png")
        return None

def wait_for_new_image(old_srcs, timeout=60):
    """Waits for a new image to appear on the page by comparing image sources."""
    end = time.time() + timeout
    while time.time() < end:
        imgs = driver.find_elements(By.TAG_NAME, "img")
        for img in imgs:
            src = img.get_attribute("src")
            if src and src not in old_srcs:
                return True
        time.sleep(0.5)
    return False

# Main loop to process each prompt
for idx, prompt in enumerate(prompts, 1):
    print(f"\n▶ Running prompt {idx}/{len(prompts)}: '{prompt}'")
    try:
        textarea = find_textarea()
        if not textarea:
            raise RuntimeError("Textarea not found. Cannot continue.")

        textarea.clear()
        textarea.send_keys(prompt)
        time.sleep(0.5)

        existing_srcs = {img.get_attribute("src") for img in driver.find_elements(By.TAG_NAME, "img") if img.get_attribute("src")}

        gen_button = find_generate_button()
        if not gen_button:
            raise RuntimeError("Generate button not found or it remained disabled.")

        driver.execute_script("arguments[0].click();", gen_button)
        print("→ Generate clicked, waiting for new image...")

        if wait_for_new_image(existing_srcs, timeout=90):
            print("✅ Image appeared successfully.")
        else:
            screenshot = f"whisk_timeout_{idx}.png"
            driver.save_screenshot(screenshot)
            print(f"⚠ Timeout waiting for generated image. Saved screenshot: {screenshot}")
        
        time.sleep(2)

    except Exception as e:
        screenshot = f"whisk_error_{idx}.png"
        try:
            driver.save_screenshot(screenshot)
        except Exception:
            pass
        print(f"❌ An error occurred for prompt {idx}: {e}\nSaved screenshot: {screenshot}")
        continue

# The script now ends here, leaving the browser open.
print("\n✅ All prompts processed. The browser will remain open.")