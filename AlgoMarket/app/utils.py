from email import message
import requests
from django.template.loader import render_to_string
import os

key = os.environ.get('MAILGUN')

def email(mail_subject, to_email, message=None, html=None):
    if message:
        ret = requests.post(
            "https://api.mailgun.net/v3/mg.tomorine.codes/messages",
            auth=("api", key),
            data={"from": "AlgoMarket <AlgoMarket@tomorine.codes>",
                "to": [to_email],
                "subject": mail_subject,
                "text": message}
        )
    elif html:
        ret = requests.post(
            "https://api.mailgun.net/v3/mg.tomorine.codes/messages",
            auth=("api", key),
            data={"from": "AlgoMarket <AlgoMarket@tomorine.codes>",
                "to": [to_email],
                "subject": mail_subject,
                "html": html}
        )
    return ret.status_code
    
def service_seller_notification(request, service, store_id):
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

def service_buyer_notification(request, service, store_id):
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
    email(mail_subject, request.user.email, html=message)

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