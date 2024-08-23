from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Model reprezentujący kategorię rośliny
class Category(models.Model):
    name = models.CharField(max_length=100)
# Model reprezentujący roślinę należącą do użytkownika

class Plant(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_watered = models.DateTimeField(default=timezone.now)
    photo = models.OneToOneField('Photo', on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

# Model reprezentujący harmonogram podlewania rośliny
class WateringSchedule(models.Model):
    plant = models.OneToOneField(Plant, on_delete=models.CASCADE)
    watering_interval = models.PositiveIntegerField(default=7)

# Model reprezentujący zdjęcie rośliny
class Photo(models.Model):
    image = models.ImageField(upload_to='plant_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Model reprezentujący powiadomienie dla użytkownika
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    telegram_id = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
