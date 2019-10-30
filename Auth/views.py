from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import logout as django_logout
from JsonFactory.JsonFactory import Forbidden
# Create your views here.


def checkToken(request):
    data = json.loads(request.body)
    token = data["token"]
    username = data["username"]
    user = User.objects.get(username=username)
    valid_token = Token.objects.get(user=user)
    if valid_token.key == token:
        return True
    else:
        return False


@csrf_exempt
def getToken(request):
    data = json.loads(request.body)
    username = data["username"]
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            try:
                token = Token.objects.get(user=user)
                Token.objects.filter(user=user).update(
                    key=token.generate_key())
                token = Token.objects.get(user=user)
                return JsonResponse({"token": token.key})
            except:
                token = Token.objects.create(user=user)
                return JsonResponse({"token": token.key})
        else:
            return Forbidden("Disabled account")
    else:
        return Forbidden("Invalid login or password")
