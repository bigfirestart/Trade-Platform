from django.shortcuts import render
import json
from .models import Wallet , Transaction
from django.contrib.auth.models import User
from JsonFactory.JsonFactory import Forbidden, NotFound
from django.http import JsonResponse
from Auth.views import checkToken
from django.core import serializers
from decimal import Decimal
from django.forms.models import model_to_dict

# Create your views here.
def validateTransactionAmount(user, sum):
    user_balance = float(Wallet.objects.get(user = user).balance)
    if user_balance>=sum:
        return True
    else:
        return False
def startTransaction(request):
    data = json.loads(request.body)
    user_from_name = data['username']
    try:
        user_from = User.objects.get(username = user_from_name )
    except:
        return NotFound("No such user " + user_from_name)
    if checkToken(request):
        user_to_name = data['Transaction']['recipient']
        user_to = User.objects.get(username = user_to_name )
        transfer_amount = Decimal(data['Transaction']['amount'])
        print(transfer_amount)
        if validateTransactionAmount(user_from,transfer_amount):
            user_from_wallet= Wallet.objects.get(user = user_from)
            user_to_wallet = Wallet.objects.get(user = user_to)
            # if wallets are the same
            if user_from_wallet == user_to_wallet:
                return Forbidden("wallets cant be the same")

            #changing wallets balance
            user_from_wallet.balance = float(Decimal(user_from_wallet.balance) - transfer_amount)
            user_to_wallet.balance = float(Decimal(user_to_wallet.balance) + transfer_amount)
            user_to_wallet.save()
            user_from_wallet.save()

            #adding Transaction
            transaction = Transaction.objects.create(user_to = user_to , user_from =user_from ,
                                                    amount = float(transfer_amount))
            return JsonResponse({"Transaction id": transaction.id} , status =201)
        else:
            return Forbidden("Not enough money in the account")
    else:
        return Forbidden("Invalid token")
