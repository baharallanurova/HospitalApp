from django.contrib import admin
from .models import Medicine, Pharmacist, Cart, Order

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'medicine_type', 'medicine_category', 'price', 'stock_quantity']
    list_filter = ['medicine_type', 'medicine_category']
    search_fields = ['name']

@admin.register(Pharmacist)
class PharmacistAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number']
    search_fields = ['name', 'email']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'quantity', 'purchased']
    list_filter = ['purchased']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'created']
    list_filter = ['ordered']