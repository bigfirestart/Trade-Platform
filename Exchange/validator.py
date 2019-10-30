from .models import Commodity, Asset , Tender
from django.contrib.auth.models import User


def validateCommodity(commodity_name):
    try:
        commodity = Commodity.objects.get(name=commodity_name)
        return commodity
    except:
        return None

def validateTender(tender_id):
    try:
        tender = Tender.objects.get(pk = tender_id )
        return tender
    except:
        return None
def validateUser(username):
    try:
        user = User.objects.get(username=username)
        return user
    except:
        return None
def validateAsset(user,commodity ):
    try:
        asset = Asset.objects.get(user = user, commodity = commodity)
        return asset
    except:
        return None
