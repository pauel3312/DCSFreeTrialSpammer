# DCSFreeTrialSpammer

This is a python script, with a selenium and a pyautogui based alternative
the Pyautogui version is considered not reliable enough, and will probably be deleted in future commits.
In order to use the script, you need to add several files after cloning the repo, that I will keep private.
The templates are:

in logins.txt:
```
<index of the next account to use>
<username1>
<username2>
...
```

UserPasswords.json contains a single JSON-formatted dictionary, keys are usernames as defined in logins.txt, values are the passwords to the corresponding DCS accounts

UserOTPSecrets.json contains a single JSON-formatted dictionary, keys are usernames as defined in logins.txt, values are the time-based one time password secrets to the corresponding DCS accounts.

