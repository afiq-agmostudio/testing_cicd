from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status

from .models import Product, Customer, Address, OrderItem
from .serializers import ProductSerializers, CustomerSerializers, OrderItemSerializers, AddressSerializers

# Create your views here.

#Product view starts here
class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    # def get(self, request):
    #     product = Product.objects.all()
    #     prod_serializers = ProductSerializers(product,many=True)
    #     return Response(prod_serializers.data)
    
    # def post(self,request):
    #     product_serializers = ProductSerializers(data=request.data)
    #     product_serializers.is_valid(raise_exception=True)
    #     product_serializers.save()
    #     return Response(product_serializers.data, status = status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        prod_serializers = ProductSerializers(product)
        return Response(prod_serializers.data)


#Product view ends here

#Customer view starts here
class CustomerList(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers

    # def get(self, request):
    #     customer = Customer.objects.all()
    #     customer_serializers = CustomerSerializers(customer,many=True)
    #     return Response(customer_serializers.data)

    # def post(self, request):
    #     customer_serializers = CustomerSerializers(data=request.data)
    #     customer_serializers.is_valid(raise_exception=True)
    #     customer_serializers.save()
    #     return Response(customer_serializers.data, status = status.HTTP_201_CREATED)


class CustomerDetail(APIView):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer_serializers = CustomerSerializers(customer)
        return Response(customer_serializers.data)

    def put(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer_serializers = CustomerSerializers(customer,data=request.data)
        customer_serializers.is_valid(raise_exception=True)
        customer_serializers.save()
        return Response(customer_serializers.data)

    def delete(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)       


#Customer view ends here

#Address view starts here

class AddressList(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializers

class AddressDetail(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializers

#Address view ends here

# Order view starts here
class OrderItemsList(ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializers

    # def get(self, request):
    #     order_items = OrderItem.objects.select_related('customer_id','product_id').all()
    #     order_serializers = OrderItemSerializers(order_items, many=True, context={'request': request})
    #     return Response(order_serializers.data)

class OrderItemsDetail(ListCreateAPIView):
    queryset = OrderItem.objects.select_related('customer_id','product_id').all()
    serializer_class = OrderItemSerializers

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request):
        orderitems_serializers = CustomerSerializers(data=request.data, context={'request': request})
        orderitems_serializers.is_valid(raise_exception=True)
        orderitems_serializers.save()
        return Response(orderitems_serializers.data, status = status.HTTP_201_CREATED)
    
    #basic class-based
    # def get(self, request, id):
    #     order_items = get_object_or_404(OrderItem, pk=id)
    #     order_serializers = OrderItemSerializers(order_items,context={'request': request})
    #     return Response(order_serializers.data)


#Order view ends here