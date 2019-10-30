from Auth.views import checkToken
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from JsonFactory.JsonFactory import Forbidden


@csrf_exempt
def getTime(request):
    if checkToken(request):
        return JsonResponse({'time': str(datetime.now())})
    else:
        return Forbidden("Invalid token ")
