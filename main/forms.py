from django import forms
from .models import UserCar, CarReview

class UserCarForm(forms.ModelForm):
    class Meta:
        model = UserCar
        fields = ['brand', 'model', 'year', 'fuel_type', 'mileage', 'fuel_consumption', 'image']
        widgets = {
            'year': forms.NumberInput(attrs={'min': 1900, 'max': 2024}),
            'mileage': forms.NumberInput(attrs={'min': 0}),
            'fuel_consumption': forms.NumberInput(attrs={'min': 0, 'step': '0.1'})
        }

class CarReviewForm(forms.ModelForm):
    class Meta:
        model = CarReview
        fields = ['pros', 'cons', 'common_issues']
        widgets = {
            'pros': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Aracın beğendiğiniz yönlerini yazın...'}),
            'cons': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Aracın beğenmediğiniz yönlerini yazın...'}),
            'common_issues': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Aracın kronik sorunlarını yazın...'})
        } 