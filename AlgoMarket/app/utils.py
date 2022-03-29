from . import requests

def email(mail_subject, message, to_email):
    ret = requests.post(
        "https://api.mailgun.net/v3/sandbox49891cb350ed47018e9d4289ddff229a.mailgun.org/messages",
        auth=("api", "26102838b5cf4e8fbcf16b5a93902635-90ac0eb7-3cf59ac2"),
        data={"from": "Tamarine.me <autofeedback@tamarine.me>",
            "to": [to_email],
            "subject": mail_subject,
            "text": message}
    )
    return ret.status_code
    