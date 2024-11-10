import pyautogui as agui
import pyperclip
import pyotp
import json
import time


users = "logins.txt"
passwords_JSON = "UserPasswords.json"
OTP_secrets_JSON = "UserOTPSecrets.json"

file = open(passwords_JSON, "r")
passwords_dict: dict[str: str] = json.loads(file.read())
file.close()

file = open(OTP_secrets_JSON, "r")
OTP_Dict: dict[str: str] = json.loads(file.read())
file.close()


def DCS_login(user: str) -> None:
    agui.moveTo(x=697, y=366)  # Works for 1440p 16:9 on chromium and Vivaldi.
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
    agui.hotkey("ctrl", "e")


def get_OTP(user: str) -> str:
    totp = pyotp.TOTP(OTP_Dict[user])
    return totp.now()


def get_user() -> str:
    file_tmp = open(users, "r")
    users_list = file_tmp.readlines()
    file_tmp.close()
    index = int(users_list[0])
    users_list[0] = (str(index+1)+"\n") if index+2 < len(users_list) else "0\n"
    file_tmp = open(users, "w")
    file_tmp.writelines(users_list)
    file_tmp.close()
    return users_list[index+1]


if __name__ == "__main__":
    DCS_login(get_user())
