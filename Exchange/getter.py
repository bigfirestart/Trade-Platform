from django.core import serializers
import json
from django.shortcuts import render
from Auth.views import checkToken
from JsonFactory.JsonFactory import Forbidden, NotFound, OK
from django.http import JsonResponse
from .validator import *


def getAsset(request, asset_id):
    data = json.loads(request.body)
    user_name = data['username']
    if checkToken(request):
        user = validateUser(user_name)
        if user is not None:
            asset = Asset.objects.filter(pk=asset_id)
            if len(asset) > 0:
                if asset[0].user == user:
                    data = serializers.serialize("json", [asset[0], ])
                    data = json.loads(data)
                    return JsonResponse(data, status=200, safe=False)

                else:
                    return Forbidden("You have no rigths for this asset")
            else:
                return NotFound("No such asset with id: " + str(asset_id))
        else:
            return NotFound("No such user " + user_name)
    else:
        return Forbidden("Invalid token")


def getAssets(request):
    data = json.loads(request.body)
    user_name = data['username']
    if checkToken(request):
        user = validateUser(user_name)
        if user is not None:
            assets = Asset.objects.filter(user=user)
            if len(assets) > 0:
                data = serializers.serialize("json", assets)
                data = json.loads(data)
                return JsonResponse(data, status=200, safe=False)
            else:
                return Forbidden("You have no assets")
        else:
            return NotFound("No such user " + user_name)

    else:
        return Forbidden("Invalid token")


def getTender(request, tender_id):
    data = json.loads(request.body)
    user_name = data['username']
    if checkToken(request):
        user = validateUser(user_name)
        if user is not None:
            tender = Tender.objects.filter(pk=tender_id)
            if len(tender) > 0:
                data = serializers.serialize("json", [tender[0], ])
                data = json.loads(data)
                return JsonResponse(data, status=200, safe=False)
            else:
                return NotFound("No such tender with id: " + str(tender_id))
        else:
            return NotFound("No such user " + user_name)
    else:
        return Forbidden("Invalid token")


def getTenders(request):
    tender = Tender.objects.all()
    if len(tender) > 0:
        data = serializers.serialize("json", tender)
        data = json.loads(data)
        return JsonResponse(data, status=200, safe=False)
    else:
        return NotFound("No tenders")


def getCommodities(request):
    commodities = Commodity.objects.all()
    if len(commodities) > 0:
        data = serializers.serialize("json", commodities)
        data = json.loads(data)
        return JsonResponse(data, status=200, safe=False)
    else:
        return NotFound("No commodities")
