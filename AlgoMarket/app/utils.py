import requests

def email(mail_subject, to_email,message=None, html=None):
    if message:
        ret = requests.post(
            "https://api.mailgun.net/v3/mg.tomorine.codes/messages",
            auth=("api", "key-c58ccd7ad317aedc36d768f389bebae6"),
            data={"from": "AlgoMarket <AlgoMarket@tomorine.codes>",
                "to": [to_email],
                "subject": mail_subject,
                "text": message}
        )
    elif html:
        ret = requests.post(
            "https://api.mailgun.net/v3/mg.tomorine.codes/messages",
            auth=("api", "key-c58ccd7ad317aedc36d768f389bebae6"),
            data={"from": "AlgoMarket <AlgoMarket@tomorine.codes>",
                "to": [to_email],
                "subject": mail_subject,
                "html": html}
        )
    return ret.status_code