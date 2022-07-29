from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()

# Create your models here.

# class DiscountItem(models.Model):
#     name = models.CharField(max_length=255)
#     discount_amount = models.FloatField() 
#     create_date = models.DateField(auto_now=True)


class Product(models.Model):
    name = models.CharField(max_length= 100)
    slug = models.CharField(max_length=100,null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    total_product = models.IntegerField()
    create_date = models.DateField(auto_now=True)
    # update_date = models.DateField(auto_now=True)
    # discounts = models.ManyToManyField(DiscountItem, related_name='products')

    def __str__(self):
        return self.name

class Customer(models.Model):
    age = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    nickname = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.nickname
    
    class Meta:
        ordering = ['user']

class Address(models.Model):
    # STATE_LIST = [
    #     ('1', 'Selangor'),
    #     ('2', 'Johor'),
    #     ('3', 'Kedah'),
    #     ('4', 'Sabah'),
    #     ('5', 'Sarawak'),2
    #     ('6', 'Melaka'),
    #     ('7', 'Perak'),
    #     ('8', 'Perlis'),
    #     ('9', 'Kelantan'),
    #     ('10', 'Terengganu'),
    #     ('11', 'Pahang'),
    #     ('12', 'Kuala Lumpur'),
    #     ('13', 'Negeri Sembilan'),
    #     ('14', 'Pulau Pinang'),
    # ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default= '')
    address = models.CharField(max_length=255)
    postcode = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=255)

    def __str__(self):
        return self.customer.nickname

    class Meta:
        verbose_name_plural = "Addresses"

class OrderItem(models.Model):
    ORDER_STATUS = [
        ('P', 'Pending Payment'),
        ('T', 'Out for Delivery'),
        ('D', 'Delivered'),
    ]
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer')
    quantity = models.IntegerField(null=True)
    order_date = models.DateField(auto_now=True)
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS, default='P')

    def __str__(self):
        return self.product_id.name

    class Meta:
        verbose_name = "Order Item"

