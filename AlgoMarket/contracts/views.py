from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from app.models import Service, User
from contracts.helpers import INITIAL_FUNDS, add_standalone_account, add_transaction, cli_passphrase_for_account, initial_funds_sender
from contracts.models import Account

from app.utils import *
import app.utils as utils
from django.template.loader import render_to_string

# Create your views here.
def create_account(request, username):
    user = get_object_or_404(User, username=username)
    private_key, address = add_standalone_account()
    account = Account.objects.create(user=user, address=address, private_key=private_key)

    # initialize the account to have INITIAL_FUNDS given
    sender = initial_funds_sender()
    add_transaction(sender, address, cli_passphrase_for_account(sender), INITIAL_FUNDS, "Initial Funds")

    return redirect('accounts', username)

def accounts(request, username):
    user = get_object_or_404(User, username=username)
    accounts = Account.objects.filter(user=user)

    return render(request, "contracts/accounts.html", context={"accounts": accounts})

def account_page(request, address):
    context = {"account": Account.instance_from_address(address)}
    return render(request, "contracts/account_page.html", context)

def purchase(request, sender, store_id):
    sender_user = get_object_or_404(User, username=sender)
    sender_account = Account.accounts_from_user(sender_user)
    if sender_account:
        sender_account = sender_account[0]
    else:
        raise Http404("No accounts found.")
    store = get_object_or_404(Service, id=store_id)
    store_account = Account.accounts_from_user(store.seller)
    if store_account:
        store_account = store_account[0]
    else:
        raise Http404("Seller does not have account setup.")
    error_field, error_description = add_transaction(sender_account.address, store_account.address, sender_account.passphrase, store.price*10000, f"store {store.id}")
    if error_field != "":
        raise Http404(error_description)
        
    # Add email to notify the seller about the purchase
    service = Service.objects.get(pk=store_id)
    
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
    to_email = service.seller.email
    utils.email(mail_subject, message, to_email)
    
    mail_subject = "AlgoMarket - Service Purchase Confirmation!"
    message = render_to_string('app/to_buyer_email_template.html', {
        'username': request.user.username,
        'seller_email': service.seller.email,
        'service_name': service.name,
        'service_description': service.description,
        'service_price': service.price,
        'store_num': store_id
    })
    to_email = request.user.email
    utils.email(mail_subject, message, to_email)
    
    return redirect("accounts", request.user.username)