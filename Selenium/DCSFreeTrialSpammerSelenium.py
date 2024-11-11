import time
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from load_secrets import *
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c

DEFAULT_WAIT = 1

LOGIN_BUTTON_ID = "login-line"
LOGIN_USER_ID = "USER_LOGIN"
LOGIN_PASSWORD_ID = "USER_PASSWORD"
LOGIN_OTP_ID = "USER_OTP"

SHOP_TRIAL_TEXT = "Trial"
SHOP_TRIAL_OK_TEXT = "Trial period"
TRIAL_OTP_ID = "OTP"
TRIAL_OTP_VERIFY_NAME = "Otp"

usr = get_user()

shop_address = "https://www.digitalcombatsimulator.com/en/shop/modules/"
terrains_address = "https://www.digitalcombatsimulator.com/en/shop/terrains/"
page_argument = "?PAGEN_1="

options = Options()
# options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)
driver.get(shop_address)


class NoTrialButtonException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def is_logged_in() -> bool:
    login_span = driver.find_element(By.ID, LOGIN_BUTTON_ID)
    if login_span.text == "Login":
        return False
    elif login_span.text == "Logout / Profile":
        return True
    else:
        raise Exception(f"Login check failed: login span text ({login_span.text}) is incorrect")


def login(user: str) -> None:
    if is_logged_in():
        return
    driver.find_element(By.ID, LOGIN_BUTTON_ID).click()
    driver.find_element(By.ID, LOGIN_USER_ID).send_keys(user)
    driver.find_element(By.ID, LOGIN_PASSWORD_ID).send_keys(passwords_dict[user])
    driver.find_element(By.ID, LOGIN_USER_ID).send_keys(Keys.ENTER)
    resolve_OTP_login(user)
    time.sleep(.5)
    if not is_logged_in():
        login(user)


def resolve_OTP_login(user: str) -> None:
    login_otp = WebDriverWait(driver, 10).until(e_c.visibility_of_element_located((By.ID, LOGIN_OTP_ID)))
    login_otp.send_keys(get_OTP(user))
    login_otp.send_keys(Keys.ENTER)


def resolve_OTP(user: str) -> None:
    otp_textbox = WebDriverWait(driver, 10).until(e_c.visibility_of_element_located((By.ID, TRIAL_OTP_ID)))
    time.sleep(DEFAULT_WAIT*5)
    otp_textbox.send_keys(get_OTP(user))
    driver.find_element(By.NAME, TRIAL_OTP_VERIFY_NAME).click()


def get_trial_button() -> WebElement:
    buttons = driver.find_elements(By.XPATH, f"//*[contains(text(), '{SHOP_TRIAL_TEXT}')]")
    for button in buttons:
        if button.text == "" or button.text == SHOP_TRIAL_OK_TEXT:
            continue
        return button
    raise NoTrialButtonException(f"No valid trial button was found")


def resolve_trial_button(trial_button: WebElement, user: str) -> None:
    driver.execute_script("arguments[0].scrollIntoView(true);", trial_button)
    trial_button.click()
    resolve_OTP(user)


def resolve_all_trials_on_page(user: str, page_number: int, address: str) -> None:
    while 1:
        driver.get(str(address+page_argument+str(page_number)))
        time.sleep(DEFAULT_WAIT)
        try:
            button = get_trial_button()
        except NoTrialButtonException:
            return
        time.sleep(DEFAULT_WAIT)
        try:
            resolve_trial_button(button, user)
        except ElementClickInterceptedException:
            continue


def resolve_all_trials(user: str) -> None:
    for i in range(1, 7):
        resolve_all_trials_on_page(user, i, shop_address)
    for i in (1, 2):
        resolve_all_trials_on_page(user, i, terrains_address)


if __name__ == "__main__":
    login(usr)
    time.sleep(DEFAULT_WAIT)
    resolve_all_trials(usr)
