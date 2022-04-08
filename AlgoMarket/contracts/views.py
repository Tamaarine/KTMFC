from django.shortcuts import get_object_or_404, render, redirect

from app.models import User
from contracts.helpers import INITIAL_FUNDS, add_standalone_account, add_transaction, cli_passphrase_for_account, initial_funds_sender
from contracts.models import Account

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