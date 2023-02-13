from django.contrib import admin
from .models.vehicle import Vehicle
from .models.category import Category
# Register your models here.


admin.site.register(Vehicle)
admin.site.register(Category)