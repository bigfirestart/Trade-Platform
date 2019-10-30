from django.urls import path
from . import views, getter

urlpatterns = [
    path('assets/create', views.createAsset),
    path('tenders/create', views.createTender),
    path('tenders/<int:tender_id>/buy', views.buyTender),
    path('assets', getter.getAssets),
    path('assets/<int:asset_id>', getter.getAsset),
    path('tenders', getter.getTenders),
    path('tenders/<int:tender_id>', getter.getTender),
    path('commodities', getter.getCommodities)
]
