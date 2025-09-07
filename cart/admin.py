from django.contrib import admin
from .models import Order, Item

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total", "date")
    list_filter = ("user", "date")
    ordering = ("-date",)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "movie", "price", "quantity")
    list_filter = ("order", "movie")
