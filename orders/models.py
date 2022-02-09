from django.db import models
from django.contrib.postgres.fields import JSONField
from djmoney.models.fields import MoneyField
from django.contrib.sessions.models import Session
from django.forms import ModelForm

# Create your models here.

#USERS - fn, ln, email, un


#PIZZA Names


#PIZZA Prices
class Pizza(models.Model):
    name = models.CharField(max_length=64)
    toppings = models.IntegerField()
    small = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    large = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    def __str__(self):
        return f"{self.id} - {self.name}, Small: {self.small} and Large: {self.large}, Toppings: {self.toppings}"

#pizza toppings
class Toppings(models.Model):
    topping = models.CharField(max_length=64, unique=True)
    topping_type = models.CharField(max_length=64)

    
    
#SUBS
class Subs(models.Model):
    name = models.CharField(max_length=64)
    small = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    large = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    def __str__(self):
        return f"{self.id} - {self.name}, Small: {self.small} and Large: {self.large}"
    

#SALAD
class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    def __str__(self):
        return f"{self.id} - {self.name}, Price: {self.price}"

#PASTA
class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    def __str__(self):
        return f"{self.id} - {self.name}, Price: {self.price}"
    
#ORDERS
class Orders(models.Model):
    username = models.CharField(max_length=64, default=None)
    date = models.DateTimeField(auto_now_add=True)
    order = JSONField(default=dict)
    status = models.CharField(max_length=64, default=None)
    
class ToppingForm(ModelForm):
    class Meta:
        model = Pizza
        fields = ["toppings"]
        