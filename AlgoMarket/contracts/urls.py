from django.urls import path

from . import views

urlpatterns = [
    path('create_account/<str:username>', views.create_account, name="create_account"),
    path('account/<str:address>', views.account_page, name="account_page"),
    path('accounts/<str:username>', views.accounts, name="accounts"),
    path('purchase/<str:sender>/<int:store_id>', views.purchase, name="purchase"),
    path('pledge/<str:sender>/<int:store_id>/<int:choice>', views.pledge, name='pledge')
]