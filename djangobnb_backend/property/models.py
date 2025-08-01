from django.db import models
import uuid
from django.conf import settings
from useraccount.models import User

# Create your models here.
class Property(models.Model):
    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    guests = models.IntegerField()
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/properties')
    landlord = models.ForeignKey(User, related_name='properties', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    favorited = models.ManyToManyField(User, related_name='favorites', blank=True)
    
    class Meta:
        verbose_name = ('Предложение')
        verbose_name_plural = ('Предложения')
    
    def image_url(self):
        return f'{settings.WEBSITE_URL}{self.image.url}'
    
    def __str__(self):
        return f'{self.title} - {self.country_code}'
    
    
class Reservation(models.Model):
    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, related_name='reservations', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_nights = models.IntegerField()
    guests = models.IntegerField()
    total_price = models.FloatField()
    created_by = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE) # Имя обратной связи (User.reservations.all())
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = ('Брони')
    