import json

users = "./logins.txt"
passwords_JSON = "./UserPasswords.json"
OTP_secrets_JSON = "./UserOTPSecrets.json"

file = open(passwords_JSON, "r")
passwords_dict: dict[str: str] = json.loads(file.read())
file.close()

file = open(OTP_secrets_JSON, "r")
OTP_Dict: dict[str: str] = json.loads(file.read())
file.close()


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
