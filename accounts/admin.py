from django.contrib import admin

from .models import Customer, Product, Order, Tag


# @admin.register()  must be used only when you intend creating an adminModel class
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
