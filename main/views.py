from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.db.models import Avg, Min, Max, Count, F
from .models import CarNews, UserCar, CarReview
from .forms import UserCarForm, CarReviewForm

# Create your views here.

def home(request):
    news = CarNews.objects.all()[:5]  # Son 5 haber
    latest_cars = UserCar.objects.all().order_by('-date_posted')[:6]  # Son 6 araç
    return render(request, 'main/home.html', {
        'news': news,
        'latest_cars': latest_cars
    })

def news_list(request):
    news = CarNews.objects.all()
    return render(request, 'main/news_list.html', {'news': news})

def news_detail(request, pk):
    news = get_object_or_404(CarNews, pk=pk)
    return render(request, 'main/news_detail.html', {'news': news})

@login_required
def add_car(request):
    if request.method == 'POST':
        form = UserCarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            messages.success(request, 'Arabanız başarıyla eklendi!')
            return redirect('car_detail', pk=car.pk)
    else:
        form = UserCarForm()
    return render(request, 'main/add_car.html', {'form': form})

def car_list(request):
    # Base queryset
    cars = UserCar.objects.all().order_by('-date_posted')
    title = 'Tüm Arabalar'

    # Filter by owner if my_cars is requested
    if request.user.is_authenticated and request.GET.get('my_cars') == 'true':
        cars = cars.filter(owner=request.user)
        title = 'Arabalarım'
    
    # Apply search filters
    brand_query = request.GET.get('brand')
    model_query = request.GET.get('model')
    
    if brand_query:
        cars = cars.filter(brand__icontains=brand_query)
    
    if model_query:
        cars = cars.filter(model__icontains=model_query)
    
    return render(request, 'main/car_list.html', {
        'cars': cars,
        'title': title,
        'show_add_button': True
    })

def car_detail(request, pk):
    car = get_object_or_404(UserCar, pk=pk)
    reviews = car.reviews.all().order_by('-date_posted')
    
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = CarReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            messages.success(request, 'Yorumunuz başarıyla eklendi!')
            return redirect('car_detail', pk=pk)
    else:
        review_form = CarReviewForm()
    
    return render(request, 'main/car_detail.html', {
        'car': car,
        'reviews': reviews,
        'review_form': review_form
    })

@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    user_cars = UserCar.objects.filter(owner=user).order_by('-date_posted')
    car_reviews = CarReview.objects.filter(car__owner=user).order_by('-date_posted')
    
    if user == request.user:
        news_posts = CarNews.objects.filter(author=user).order_by('-date_posted')
    else:
        news_posts = CarNews.objects.filter(author=user, is_published=True).order_by('-date_posted')
    
    context = {
        'profile_user': user,
        'user_cars': user_cars,
        'car_reviews': car_reviews,
        'news_posts': news_posts,
    }
    return render(request, 'main/profile.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Hesabınız başarıyla oluşturuldu!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Başarıyla giriş yaptınız!')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız!')
    return redirect('home')

@login_required
def user_settings(request):
    if request.method == 'POST':
        dark_mode = request.POST.get('dark_mode') == 'true'
        request.session['dark_mode'] = dark_mode
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('settings')
    
    dark_mode = request.session.get('dark_mode', False)
    return render(request, 'main/settings.html', {
        'dark_mode': dark_mode
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Kullanıcı bilgilerini güncelle
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        messages.success(request, 'Profil bilgileriniz başarıyla güncellendi!')
        return redirect('profile')
    
    return render(request, 'main/edit_profile.html')

@login_required
def my_news(request):
    news = CarNews.objects.filter(author=request.user).order_by('-date_posted')
    return render(request, 'main/my_news.html', {'news': news})

@login_required
def edit_news(request, pk):
    news = get_object_or_404(CarNews, pk=pk, author=request.user)
    
    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.content = request.POST.get('content')
        if request.FILES.get('image'):
            news.image = request.FILES['image']
        news.save()
        messages.success(request, 'Haber başarıyla güncellendi!')
        return redirect('my_news')
    
    return render(request, 'main/edit_news.html', {'news': news})

@login_required
def delete_news(request, pk):
    news = get_object_or_404(CarNews, pk=pk, author=request.user)
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Haber başarıyla silindi!')
        return redirect('my_news')
    
    return render(request, 'main/delete_news_confirm.html', {'news': news})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Şifreniz başarıyla değiştirildi!')
            return redirect('profile')
        else:
            messages.error(request, 'Lütfen aşağıdaki hataları düzeltin.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'main/change_password.html', {
        'form': form,
        'title': 'Şifre Değiştir'
    })

@login_required
def edit_car(request, pk):
    car = get_object_or_404(UserCar, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = UserCarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Araba bilgileri başarıyla güncellendi!')
            return redirect('car_detail', pk=car.pk)
    else:
        form = UserCarForm(instance=car)
    
    return render(request, 'main/edit_car.html', {
        'form': form,
        'car': car
    })

@login_required
def delete_car(request, pk):
    car = get_object_or_404(UserCar, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Araba paylaşımı başarıyla silindi!')
        return redirect('car_list')
    
    return render(request, 'main/delete_car_confirm.html', {'car': car})

@login_required
def edit_review(request, pk):
    review = get_object_or_404(CarReview, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = CarReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Yorumunuz başarıyla güncellendi!')
            return redirect('car_detail', pk=review.car.pk)
    else:
        form = CarReviewForm(instance=review)
    
    return render(request, 'main/edit_review.html', {
        'form': form,
        'review': review
    })

@login_required
def delete_review(request, pk):
    review = get_object_or_404(CarReview, pk=pk, user=request.user)
    car_pk = review.car.pk
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Yorumunuz başarıyla silindi!')
        return redirect('car_detail', pk=car_pk)
    
    return render(request, 'main/delete_review_confirm.html', {'review': review})

def car_statistics(request):
    # Yakıt tipine göre istatistikler
    fuel_stats = []
    for fuel_type, fuel_name in UserCar.FUEL_TYPES:
        stats = UserCar.objects.filter(fuel_type=fuel_type)
        if stats.exists():
            avg_consumption = stats.aggregate(Avg('fuel_consumption'))['fuel_consumption__avg']
            min_car = stats.order_by('fuel_consumption').first()
            max_car = stats.order_by('-fuel_consumption').first()
            count = stats.count()
            
            fuel_stats.append({
                'fuel_type_display': fuel_name,
                'avg_consumption': avg_consumption,
                'min_consumption': min_car.fuel_consumption,
                'min_car_brand': min_car.brand,
                'min_car_model': min_car.model,
                'max_consumption': max_car.fuel_consumption,
                'max_car_brand': max_car.brand,
                'max_car_model': max_car.model,
                'count': count
            })
    
    # En ekonomik 5 araç
    most_economic_cars = UserCar.objects.all().order_by('fuel_consumption')[:5]
    
    return render(request, 'main/car_statistics.html', {
        'fuel_stats': fuel_stats,
        'most_economic_cars': most_economic_cars
    })
