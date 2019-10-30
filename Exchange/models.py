from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class Commodity(models.Model):
    name = models.CharField(max_length=50)
    measure = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Asset(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time_of_creation = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.commodity.name


class Tender(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='User', default="1")
    own_commodity = models.ForeignKey(
        Commodity, on_delete=models.CASCADE, related_name="own_commodity")
    own_commodity_ammount = models.DecimalField(max_digits=10, decimal_places=2)
    wish_commodity = models.ForeignKey(
        Commodity, on_delete=models.CASCADE, related_name="wish_commodity")
    wish_commodity_ammount = models.DecimalField(
        max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    time_of_creation = models.DateTimeField(default=datetime.now, blank=True)
