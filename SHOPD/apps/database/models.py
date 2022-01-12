from django.db import models
from datetime import datetime, timedelta
from django.core.validators import MaxValueValidator
from django.utils import timezone
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, verbose_name="Nombres")
    last_name = models.CharField(max_length=150, verbose_name="Apellidos")
    birthday = models.DateField(default=timezone.now, verbose_name="FechaNacimiento")
    email = models.EmailField(max_length=50, verbose_name="Email", unique=True)
    password = models.CharField(max_length=150, verbose_name="Password")
    contract_start = models.DateField(default=timezone.now, verbose_name="Inicio Contrato", null=True)
    contract_end = models.DateField(default=timezone.now, verbose_name="Fin Contrato", null=True)
    salary = models.IntegerField(default=0, null=True, blank=False)

    def __str__(self):
        return str(self.user)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=CASCADE, verbose_name="userId", null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    

    def __str__(self):
        return str(self.transaction_id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

    @property
    def shipping(self):
        shipping = True
        orderitems = self.orderitem_set.all()
        
        return shipping


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")

    def __str__(self):
        return self.name        

class Category(models.Model):
    name =  models.CharField(max_length=50, verbose_name="Categoria")

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=CASCADE, verbose_name="Marca", null=True)
    name = models.CharField(max_length=50, verbose_name="Nombre")
    price = models.PositiveIntegerField(validators=[MaxValueValidator(1000000)], verbose_name="Precio")
    description = models.TextField(verbose_name="Descripcion", null=True)
    stock = models.PositiveIntegerField(validators=[MaxValueValidator(10000)], verbose_name="Stock", default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=CASCADE, verbose_name="productId", null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

   

    @property
    def get_total(self):
        total= self.product.price * self.quantity
        return total 

class ShippingAdress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    adress = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    pais = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.adress
