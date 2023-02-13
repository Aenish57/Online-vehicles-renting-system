from django.db import models
from .category import Category
from django.urls import reverse

# Creatig models for vehicles
class Vehicle(models.Model):
    Vehicle_id = models.AutoField
    Vehicle_name = models.CharField(max_length=60)
    Vehicle_company = models.CharField(max_length=60)
    Vehicle_model = models.CharField(max_length=60)
    category = models.ForeignKey(Category,on_delete=models.CASCADE , default=1)
    Vehicle_type = models.CharField(max_length=20)
    Vehicle_fuel = models.CharField(max_length=10)
    Vehicle_No_of_Seats = models.IntegerField()
    Vehicle_color = models.CharField(max_length=20)
    Vehicle_license_plate = models.CharField(max_length=30)
    Vehicle_uploaded_by = models.CharField(max_length=100)
    Vehicle_image1 = models.ImageField(upload_to='img/Vehicle_images/')
    Vehicle_image2 = models.ImageField(upload_to='img/Vehicle_images/')
    Vehicle_image3 = models.ImageField(upload_to='img/Vehicle_images/')
    isGeared = models.BooleanField()
    Vehicle_description = models.CharField(max_length=1500)
    Vehicle_price = models.IntegerField()
    class Meta:
        ordering=('-Vehicle_name',)

    def __str__(self):
        return self.Vehicle_license_plate + " : " + str(self.Vehicle_name) + " : " + str(self.category)
    
    def get_absolute_url(self):
        return reverse('base',args=[self.id,])