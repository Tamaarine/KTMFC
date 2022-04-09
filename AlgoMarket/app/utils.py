import requests

def email(mail_subject, message, to_email):
    ret = requests.post(
        "https://api.mailgun.net/v3/mg.tomorine.codes/messages",
		auth=("api", "key-c58ccd7ad317aedc36d768f389bebae6"),
        data={"from": "AlgoMarket <AlgoMarket@tomorine.codes>",
            "to": [to_email],
            "subject": mail_subject,
            "text": message}
    )
    return ret.status_code