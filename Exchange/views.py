from django.shortcuts import render
from Auth.views import checkToken
from JsonFactory.JsonFactory import Forbidden, NotFound, OK
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from .models import *
from decimal import *
from .validator import *
from django.core import serializers
# Create your views here.


def createOrSumAsset(user, commodity, amount):
    if len(Asset.objects.filter(commodity=commodity, user=user)) > 0:
        asset = Asset.objects.get(commodity=commodity, user=user)
        asset.amount = asset.amount + amount
        asset.save()
        return asset
    else:
        asset = Asset.objects.create(
            commodity=commodity, user=user, amount=amount)
        return asset


def createAsset(request):
    data = json.loads(request.body)
    user_name = data['username']
    if checkToken(request):
        try:
            user = User.objects.get(username=user_name)
        except:
            return NotFound("No such user " + user_name)
        сommodity_name = data["Asset"]["Commodity"]["сommodity_name"]
        try:
            commodity = Commodity.objects.get(name=сommodity_name)
        except:
            return NotFound("No such commodity " + сommodity_name)
        amount = Decimal(data["Asset"]["ammount"])
        asset = createOrSumAsset(user, commodity, amount)
        return JsonResponse({"Success": "added", "amount": asset.amount})
    else:
        return Forbidden("Invalid token")


def createTender(request):
    data = json.loads(request.body)
    user_name = data['username']
    if checkToken(request):
        try:
            user = User.objects.get(username=user_name)
        except:
            return NotFound("No such user " + user_name)
        own_asset_commodity_name = data["Tender"]["OwnAsset"]["Commodity"]["сommodity_name"]
        wish_asset_commodity_name = data["Tender"]["WishAsset"]["Commodity"]["сommodity_name"]

        if own_asset_commodity_name == wish_asset_commodity_name:
            return Forbidden("You cant buy same commodity")

        own_asset_commodity_amount = Decimal(
            data["Tender"]["OwnAsset"]["amount"])
        wish_asset_commodity_amount = Decimal(
            data["Tender"]["WishAsset"]["amount"])
        commodity = validateCommodity(own_asset_commodity_name)
        if commodity is not None:
            own_asset = Asset.objects.filter(commodity=commodity, user=user)
            if len(own_asset) > 0:
                own_asset = own_asset[0]
                if ((Decimal(own_asset.amount) > own_asset_commodity_amount)
                        or (Decimal(own_asset.amount) == own_asset_commodity_amount) ) :
                    wish_commodity = validateCommodity(
                        wish_asset_commodity_name)
                    if wish_commodity is not None:
                        own_asset.amount = own_asset.amount - own_asset_commodity_amount
                        own_asset.save()
                        tender = Tender.objects.create(
                            user=user,
                            own_commodity=commodity,
                            own_commodity_ammount=own_asset_commodity_amount,
                            wish_commodity=wish_commodity,
                            wish_commodity_ammount=wish_asset_commodity_amount,
                            status="OnCreate")
                        tender.save()

                        return JsonResponse({"tender_id": str(tender.pk)})
                    else:
                        return Forbidden("No such commodity " + wish_asset_commodity_name)
                else:
                    return Forbidden("You have not such asset in this amount")
            else:
                return Forbidden("You have not such asset")
        else:
            return NotFound("No such commodity " + own_asset_commodity_name)

    else:
        return Forbidden("Invalid token")


def buyTender(request, tender_id):
    tender = validateTender(tender_id)
    if tender is not None:
        data = json.loads(request.body)
        user_name = data['username']
        if checkToken(request):
            user = validateUser(user_name)
            if user is not None:
                commodity = validateCommodity(tender.wish_commodity.name)
                asset = validateAsset(user, commodity)
                if asset is not None:
                    if ((asset.amount > tender.wish_commodity_ammount)
                            or (asset.amount == tender.wish_commodity_ammount)):
                        # decrease buyer amount
                        asset.amount = asset.amount - tender.wish_commodity_ammount
                        asset.save()
                        asset = createOrSumAsset(
                            tender.user, commodity, tender.wish_commodity_ammount)
                        asset = createOrSumAsset(
                            user, tender.own_commodity, tender.own_commodity_ammount)
                        tender.delete()
                        return JsonResponse({"Sucess": "trade done"})
                    else:
                        return Forbidden("You have not such asset in this amount")
                else:
                    return Forbidden("You have not such asset")
            else:
                return NotFound("No such user " + user_name)
        else:
            return Forbidden("Invalid token")
    else:
        return NotFound("No such tender")
