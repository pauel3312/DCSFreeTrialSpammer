from typing import Optional
import pyautogui
import pyautogui as agui
import pyperclip
import time
from load_secrets import passwords_dict, get_user, get_OTP

SCROLL_LENGTH = 950

trials_address = "https://www.digitalcombatsimulator.com/en/personal/licensing/trial/"
shop_address = "https://www.digitalcombatsimulator.com/en/shop/modules/"
page_argument = "?PAGEN_1="


class NoTrialButtonException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, kwargs)


def DCS_login(user: str) -> None:
    move_to_address(trials_address)
    time.sleep(1)
    agui.moveTo(x=697, y=385)  # Works for 1440p 16:9 on chromium and Vivaldi.
    agui.click()
    pyperclip.copy(user)
    agui.hotkey('ctrl', 'v')
    agui.move(0, 69)
    agui.click()
    pyperclip.copy(passwords_dict[user])
    agui.hotkey('ctrl', 'v')
    agui.hotkey("Enter")
    time.sleep(.3)
    agui.typewrite(get_OTP(user))
    agui.hotkey("Enter")
    move_to_address(shop_address)


def move_to_address(address: str) -> None:
    agui.click()
    agui.hotkey("ctrl", "e")
    pyperclip.copy(address)
    agui.hotkey("Backspace")
    agui.hotkey("ctrl", "v")
    agui.hotkey("Enter")


def take_trial(user: str) -> None:
    print("starting first image find...")
    try:
        agui.click(agui.locateCenterOnScreen("images_to_find/try_button_shop.png", grayscale=False))
    except pyautogui.ImageNotFoundException:
        print("first image find failed, starting second try...")
        try:
            agui.click(agui.locateCenterOnScreen("images_to_find/try_button_shop_2.png", grayscale=False))
        except pyautogui.ImageNotFoundException:
            raise NoTrialButtonException
    agui.typewrite(get_OTP(user))
    try:
        agui.click(agui.locateCenterOnScreen("images_to_find/verify_code_button.png", grayscale=False))
    except pyautogui.ImageNotFoundException:
        return
    agui.hotkey("esc")
    time.sleep(.5)


def trials_on_page(user: str, page_number: Optional[int] = 1) -> None:
    screenshot = agui.screenshot()
    is_ended = False
    move_to_address(shop_address + page_argument + str(page_number))
    while not is_ended:
        try:
            take_trial(user)
            move_to_address(shop_address + page_argument + str(page_number))
            agui.hotkey("ctrl", "f5")
            time.sleep(2)
        except NoTrialButtonException:
            print("Bot image finds failed, attempting scroll...")
            agui.scroll(-SCROLL_LENGTH)
            new_screenshot = agui.screenshot()
            if new_screenshot == screenshot:
                is_ended = True
            else:
                screenshot = new_screenshot


def trials_on_all_pages(user: str) -> None:
    for page_number in range(5, 7):
        trials_on_page(user, page_number)


if __name__ == "__main__":
    usr = get_user()
    DCS_login(usr)
    trials_on_all_pages(usr)
