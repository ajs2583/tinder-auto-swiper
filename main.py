import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv

# ─── Config & Constants ────────────────────────────────────────────────────────
load_dotenv()  # Load environment variables from .env file

TINDER_HOME_URL = "https://tinder.com/app/recs"

# ENVIRONMENT VARIABLES
FB_PHONE_NUMBER = os.getenv("FACEBOOK_PHONE_NUMBER")
FB_PASSWORD = os.getenv("FACEBOOK_PASSWORD")

if not FB_PHONE_NUMBER or not FB_PASSWORD:
    raise ValueError("Please set the FACEBOOK_PHONE_NUMBER and FACEBOOK_PASSWORD environment variables.")


# SELENIUM SELECTORS
TINDER_LOGIN_BUTTON_XPATH = (
    By.XPATH,
    '//*[@id="s67002758"]/div/div[1]/div/main/div[1]/div/div/div/div/div/header/div/div[2]/div[2]/a')

FACEBOOK_LOGIN_BUTTON_XPATH = (
    By.XPATH,
    '//*[@id="s-1661378318"]/div/div[1]/div/div[1]/div/div/div[2]/div[2]/span/div[2]/button')

FACEBOOK_PHONE_INPUT_XPATH = (
    By.XPATH,
    '//*[@id="email"]'
)

FACEBOOK_PASSWORD_INPUT_XPATH = (
    By.XPATH,
    '//*[@id="pass"]'
)

ALLOW_LOCATION_BUTTON_XPATH = (
    By.XPATH,
    '//*[@id="s-1661378318"]/div/div[1]/div/div/div[3]/button[1]'
)

ACCEPT_TERMS_BUTTON_XPATH = (
    By.XPATH,
    '//*[@id="s-1661378318"]/div/div[2]/div/div/div[1]/div[1]/button'
)

DECLINE_NOTIFICATIONS_BUTTON_XPATH = (
    By.XPATH,
    '//*[@id="s-1661378318"]/div/div/div/div/div[3]/button[2]'
)

LIKE_BUTTON_XPATH = (
    By.XPATH,
    '//*[@id="main-content"]/div[2]/div/div/div/div[1]/div/div/div[4]/div/div[4]/button'
)

MATCH_POPUP_XPATH = (
    By.XPATH,
    '//*[@id="s-1661378318"]/div/div[1]/div/div/div[2]/div[2]/button'
)

# ─── Setup Selenium ─────────────────────────────────────────────────────────────
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

driver.get(TINDER_HOME_URL)
driver.maximize_window()
body = driver.find_element(By.TAG_NAME, "body")

# ─── Login to Tinder via Facebook ───────────────────────────────────────────────
login_button = wait.until(
    EC.presence_of_element_located(TINDER_LOGIN_BUTTON_XPATH)
)
login_button.click()

facebook_login_button = wait.until(
    EC.presence_of_element_located(FACEBOOK_LOGIN_BUTTON_XPATH)
)
facebook_login_button.click()

# ─── Switch to Facebook popup window ────────────────────────────────────────────
main_window = driver.current_window_handle
time.sleep(2)  # Give time for popup to appear

for handle in driver.window_handles:
    if handle != main_window:
        driver.switch_to.window(handle)
        break

# ─── Enter Facebook Credentials ────────────────────────────────────────────────
facebook_phone_input = wait.until(
    EC.presence_of_element_located(FACEBOOK_PHONE_INPUT_XPATH)
)
facebook_password_input = wait.until(
    EC.presence_of_element_located(FACEBOOK_PASSWORD_INPUT_XPATH)
)

# Optional debugging
# print(f"Email input found: {facebook_phone_input.get_attribute('outerHTML')}")
# print(f"Password input found: {facebook_password_input.get_attribute('outerHTML')}")

# Send credentials
facebook_phone_input.send_keys(FB_PHONE_NUMBER)
facebook_password_input.send_keys(FB_PASSWORD)
facebook_password_input.send_keys(Keys.RETURN)
time.sleep(20)  # Wait for login to complete and complete captcha if needed

# ─── Switch back to Tinder main window ────────────────────────────────────────
driver.switch_to.window(main_window)

time.sleep(2)
# ─── Allow Location ──────────────────────────────────────────────
try:
    allow_location_button = wait.until(
        EC.presence_of_element_located(ALLOW_LOCATION_BUTTON_XPATH)
    )
    allow_location_button.click()
except NoSuchElementException:
    print("No location button found, continuing...")

# ─── Accept Tinder's Terms and Conditions ──────────────────────────────────────
try:
    accept_terms_button = wait.until(
        EC.presence_of_element_located(ACCEPT_TERMS_BUTTON_XPATH)
    )
    accept_terms_button.click()
except NoSuchElementException:
    print("No terms and conditions button found, continuing...")

# ─── Decline notifications ────────────────────────────────────────────────────────────────
try:
    decline_notifications_button = wait.until(
        EC.presence_of_element_located(DECLINE_NOTIFICATIONS_BUTTON_XPATH)
    )
    decline_notifications_button.click()
except NoSuchElementException:
    print("No notifications button found, continuing...")

# ─── Main Loop ─────────────────────────────────────────────────────────────────────

try:
    num = 0
    for n in range(100):
        time.sleep(2)  # Wait for Tinder to load new cards
        try:
            # Check if the like button is disabled or a "no more likes" message appears
            like_button = wait.until(
                EC.presence_of_element_located(LIKE_BUTTON_XPATH)
            )
            if not like_button.is_enabled():
                print("Out of likes. Exiting...")
                break
            like_button.click()
            num += 1
            print(f"{num}. Liked a profile!")
        except NoSuchElementException:
            print("No like button found, possibly out of likes. Exiting...")
            break
except KeyboardInterrupt:
    print("Exiting...")

try:
    # Wait for the match popup to appear
    match_popup = wait.until(
        EC.presence_of_element_located(MATCH_POPUP_XPATH)
    )
    match_popup.click()
finally:
    driver.quit()

