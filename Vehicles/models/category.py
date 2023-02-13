from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=20)
    # slug=models.SlugField(max_length=20)
    class Meta:
        ordering=('-name',)
    # @staticmethod
    # def get_all_categories():
    #     return Category.objects.all()

    def __str__(self):
        return self.name  
    # def get_absolute_url(self):
    #     return reverse('vehicle:vehicle_by_category', args=[self.slug])