from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Categories)
class Admin_Categories(admin.ModelAdmin):
    list_display = ['id', 'name', 'deleted']

@admin.register(Size)    
class Admin_Size(admin.ModelAdmin):
    list_display = ['id', 'category_id', 'size', 'deleted']

@admin.register(Product)
class Admin_Product(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'description', 'category_id', 'deleted']

@admin.register(Order)
class Admin_Order(admin.ModelAdmin):
    list_display = ['id', 'shipping_address', 'total_payment', 'contact_person', 'contact_number', 'email', 'quantity', 'date', 'payment_status']

@admin.register(Orders_Detail)
class Admin_Order_Details(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'product_id', 'size_id', 'quantity', 'unit_price', 'product_total']

