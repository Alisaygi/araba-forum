from django.contrib import admin
from .models import CarNews, UserCar, CarReview

@admin.register(CarNews)
class CarNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')
    search_fields = ('title', 'content')
    list_filter = ('date_posted', 'author')

@admin.register(UserCar)
class UserCarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'owner', 'fuel_type')
    search_fields = ('brand', 'model', 'owner__username')
    list_filter = ('fuel_type', 'year')

@admin.register(CarReview)
class CarReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'date_posted')
    search_fields = ('car__brand', 'car__model', 'pros', 'cons', 'common_issues')
    list_filter = ('date_posted',)
