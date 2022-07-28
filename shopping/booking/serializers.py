from itertools import product
from rest_framework import serializers
from decimal import Decimal

from .models import Product, Customer, Address, OrderItem

class ProductSerializers(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','name','price','price_with_gst','total_product']

    price_with_gst = serializers.SerializerMethodField(method_name = 'calculate_gst')

    def calculate_gst(self, product : Product):
        tax = product.price * Decimal(1.06)
        return round(tax,2)

    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length = 100)
    # price = serializers.DecimalField(max_digits = 6, decimal_places = 2) # user source = models.attribute if naming is not the same as serializers

class CustomerSerializers(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'age', 'user']
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length = 100)
    # email = serializers.CharField(max_length = 255)
    # address = serializers.PrimaryKeyRelatedField(
    #     queryset = Address.objects.all()
    # )

class AddressSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Address
        fields = ['id','customer', 'address', 'postcode', 'city', 'state']
    
    customer = serializers.PrimaryKeyRelatedField(
        queryset = Address.objects.all()
    )


class OrderItemSerializers(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id','product_id','customer_id', 'quantity','order_status']

    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset = Customer.objects.all(),
    )

    # def create(self, validated_data):
    #     return OrderItem.objects.create(**validated_data)
    # customer_id = serializers.RelatedField(read_only=True)
    # customer = serializers.HyperlinkedRelatedField(
    #     queryset = Customer.objects.all(),
    #     view_name = 'customer-detail',
    #     source = 'customer_id'
    # )
    # customer_name = serializers.PrimaryKeyRelatedField(
    #     queryset = Customer.objects.all(),
    #     source = 'customer_id'
    # )