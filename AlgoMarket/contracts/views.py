from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from app.models import Service, Transaction, User, Perk, Subscription
from contracts.helpers import INITIAL_FUNDS, add_standalone_account, add_transaction, cli_passphrase_for_account, initial_funds_sender
from contracts.models import Account

from app.utils import *
import app.utils as utils
from django.template.loader import render_to_string

from django.contrib import messages

# Create your views here.
def create_account(request, username):
    user = get_object_or_404(User, username=username)
    accounts = Account.objects.filter(user=user)
    if len(accounts) >= 1:
        return redirect('accounts', username)
    private_key, address = add_standalone_account()
    account = Account.objects.create(user=user, address=address, private_key=private_key)

    # initialize the account to have INITIAL_FUNDS given
    sender = initial_funds_sender()
    add_transaction(sender, address, cli_passphrase_for_account(sender), INITIAL_FUNDS, "Initial Funds")

    return redirect('accounts', username)

def accounts(request, username):
    user = get_object_or_404(User, username=username)
    accounts = Account.objects.filter(user=user)
    context = {}
    if len(accounts) > 0:
        balance = accounts[0].balance()
        if balance == "Error":
            messages.error(request, "Indexer down")
            return redirect("profile", username)
        balance /= 10000
        context = {"accounts": accounts, 'balance': balance}
    return render(request, "contracts/accounts.html", context=context)

def account_page(request, address):
    context = {"account": Account.instance_from_address(address)}
    return render(request, "contracts/account_page.html", context)

def purchase(request, sender, store_id):
    sender_user = get_object_or_404(User, username=sender)
    sender_account = Account.accounts_from_user(sender_user)
    if sender_account:
        sender_account = sender_account[0]
    else:
        messages.error(request, "This account has no account please set up an account first before purchasing!")
        return redirect("profile", sender_user.username)
    store = get_object_or_404(Service, id=store_id)
    store_account = Account.accounts_from_user(store.seller)
    if store_account:
        store_account = store_account[0]
    else:
        messages.error(request, "The store owner does not have an Algorand account set up!")
        return redirect("store", store_id)
    
    balance = sender_account.balance()
    if balance == "Error":
        messages.error(request, "Indexer down")
        return redirect("profile", sender)
    
    if sender_account.balance() < store.price * 10000:
        messages.error(request, "You do not have enough Algos to buy this service!")
        return redirect("store", store_id)
    
    error_field, error_description = add_transaction(sender_account.address, store_account.address, sender_account.passphrase, store.price*10000, f"store {store.id}")
    if error_field != "":
        messages.error(request, "Indexer might have died.")
        return redirect("profile", sender_user.username)
        
    service = Service.objects.get(pk=store_id)
    # Email notifications
    service_buyer_notification(request, service, store_id) # to buyer
    service_seller_notification(request, service, store_id) # to seller
    
    # Save transactions in buyer history
    transaction = Transaction(product=service, buyer=sender_user, price=store.price)
    transaction.save()

    messages.success(request, "Service purchase successful, please check your history for transaction")
    
    return redirect("store", store_id)
    
def pledge(request, sender, store_id, choice):
    sender_user = get_object_or_404(User, username=sender)
    sender_account = Account.accounts_from_user(sender_user)
    if sender_account:
        sender_account = sender_account[0]
    else:
        messages.error(request, "This account has no account please set up an account first before subscribing!")
        return redirect("profile", sender_user.username)
    store = get_object_or_404(Service, id=store_id)
    store_account = Account.accounts_from_user(store.seller)
    
    subs = get_object_or_404(Subscription, seller=store.seller) # Subscription costs
    sub_cost = [0, subs.pro_price, subs.premium_price]
    perk = get_object_or_404(Perk, service=store)
        
    if store_account:
        store_account = store_account[0]
    else:
        messages.error(request, "The store owner does not have an Algorand account set up!")
        return redirect("store", store_id)
    
    balance = sender_account.balance()
    if balance == "Error":
        messages.error(request, "Indexer down")
        return redirect("profile", sender)
    
    if sender_account.balance() < sub_cost[choice] * 10000:
        messages.error(request, "You do not have enough Algos to buy this subscription!")
        return redirect("store", store_id)
    error_field, error_description = add_transaction(sender_account.address, store_account.address, sender_account.passphrase, sub_cost[choice]*10000, f"store {store.id}")
        
    if error_field != "":
        messages.error(request, "Indexer might have died.")
        return redirect("profile", sender_user.username)
    
    names = ["Free", "Pro Tier", "Premium Tier"]
    tier_name = names[choice]
        
    # Email notifications
    subscription_b_notification(store, sender_user, sub_cost[choice], tier_name)
    
    # Save transactions
    transaction = Transaction(subscription=subs, buyer=sender_user, price=sub_cost[choice], tier=tier_name)
    transaction.save()

    messages.success(request, "Subscription purchase successful, please check your history for transaction")
    
    return redirect("store", store_id)
    
    