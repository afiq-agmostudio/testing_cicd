from django.urls import path
from . import views

app_name = "booking"

urlpatterns=[
    #products path starts here
    path("products/", views.ProductList.as_view()),
    path("products/<int:id>", views.ProductDetail.as_view()),

    #customers path starts here
    path("customers/", views.CustomerList.as_view()),
    path("customers/<int:pk>", views.CustomerDetail.as_view(), name='customer-detail'),

    #adress path starts here
    path("address/", views.AddressList.as_view()),
    path("address/<int:pk>", views.AddressDetail.as_view()),

    #orderitems path starts here
    path("orderitems/", views.OrderItemsList.as_view()),
    path("orderitems/<int:pk>", views.OrderItemsDetail.as_view()),

]