from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class CarNews(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Car News"
        ordering = ['-date_posted']
    
    def __str__(self):
        return self.title

class UserCar(models.Model):
    FUEL_TYPES = [
        ('benzin', 'Benzin'),
        ('dizel', 'Dizel'),
        ('lpg', 'LPG'),
        ('elektrik', 'Elektrik'),
        ('hibrit', 'Hibrit'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    mileage = models.IntegerField()
    fuel_consumption = models.FloatField()
    image = models.ImageField(upload_to='car_images/', null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

class CarReview(models.Model):
    car = models.ForeignKey(UserCar, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pros = models.TextField()
    cons = models.TextField()
    common_issues = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Review for {self.car} by {self.user.username}"
