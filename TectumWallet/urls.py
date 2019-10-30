from . import views
from django.urls import path

urlpatterns = [
    path('transaction', views.startTransaction)
]
