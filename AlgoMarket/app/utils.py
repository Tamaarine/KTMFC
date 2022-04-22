from email import message
import requests
from django.template.loader import render_to_string

def email(mail_subject, to_email,message=None, html=None):
    if message:
        ret = requests.post(
            "https://api.mailgun.net/v3/mg.tomorine.codes/messages",
            auth=("api", "key-d77738d4b20440dc3a3dc9c8ae6f4b3f"),
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
    
def service_b_notification(request, service, store_id):
    '''Email sent to buyer about their purchase '''
    mail_subject = "AlgoMarket - A Customer Has Purchase Your Service!"
    message = render_to_string('app/to_seller_email_template.html', {
        'seller': service.seller.username,
        'buyer': request.user.username,
        'buyer_email': request.user.email,
        'service_name': service.name,
        'service_description': service.description,
        'service_price': service.price,
        'store_num': store_id
    })
    email(mail_subject, service.seller.email, html=message)

def service_s_notification(request, service, store_id):
    '''Email sent to seller about the purchase that was made'''
    mail_subject = "AlgoMarket - Service Purchase Confirmation!"
    message = render_to_string('app/to_buyer_email_template.html', {
        'username': request.user.username,
        'seller_email': service.seller.email,
        'service_name': service.name,
        'service_description': service.description,
        'service_price': service.price,
        'store_num': store_id
    })
    email(mail_subject, service.seller.email, html=message)

def subscription_b_notification(store, sender_user, total, tier_name):
    '''Email sent to the buyer about the subscription that they made'''
    mail_subject = "AlgoMarket - Subscription Confirmation!"
    html_msg = render_to_string('app/subscription_purchase_email_template.html', context={
        'total_paid': total,
        'seller': store.seller.username,
        'buyer': sender_user.username,
        'subscription_tier': tier_name,
        'seller_email': store.seller.email
    })
    email(mail_subject, sender_user.email, html=html_msg)