import email
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AlgoMarket.settings")

import django
django.setup()

from app.models import Transaction
from app.utils import email

# Set up as a cron task to run monthly

for transaction in Transaction.objects.all():
    if transaction.subscription:
        subject = "Subscription Renewl"
        target = transaction.seller
        msg = f"Your {transaction.tier} tier subscription from {transaction.subscription.seller.username} has expired. \
            Please renewl the subscription if you like to continue."
        email(subject, target.email, message=msg)