from django.urls import path
from Products import views

app_name = "Products"

urlpatterns = [
    path("accounts/login/", views.loginform, name='login'),
    path("", views.Product_list, name='Products_list'),
    path("add", views.ProductsAdd, name='Products_add'),
    path("update/<str:ID>", views.ProductsUpdate, name='Products_update'),
    path("delete/<str:ID>", views.ProductsDelete, name='Products_delete'),
    path("search/", views.Productsearch, name='search'),
    path("download/", views.download_file, name='download'),
    path("Shopper_cart/",views.shooping_cart, name='Shopper_cart'),
    path("cart_add/<str:ID>",views.cart_add, name='cart_add'),
    path("cart_delete/<str:ID>",views.cart_delete, name='cart_delete')
]
