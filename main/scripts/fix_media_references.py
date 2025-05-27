import os
import django
import sys

# Proje kök dizinini sys.path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from main.models import CarNews, UserCar

# Doğrudan proje kökünden media/ klasörünü kullan
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

folders = ['news_images', 'car_images']

# Tüm dosya adlarını topla
media_files = {}
for folder in folders:
    folder_path = os.path.join(MEDIA_ROOT, folder)
    if not os.path.exists(folder_path):
        print(f"Klasör yok: {folder_path}, atlanıyor.")
        continue
    for filename in os.listdir(folder_path):
        media_files[f'{folder}/{filename}'] = True

# CarNews
for obj in CarNews.objects.exclude(image=''):
    if obj.image and str(obj.image) not in media_files:
        folder = 'news_images'
        folder_path = os.path.join(MEDIA_ROOT, folder)
        if not os.path.exists(folder_path):
            print(f"Klasör yok: {folder_path}, atlanıyor.")
            continue
        base = os.path.splitext(os.path.basename(str(obj.image)))[0]
        ext = os.path.splitext(str(obj.image))[1]
        for f in os.listdir(folder_path):
            if f.startswith(base) and f.endswith(ext):
                print(f'CarNews: {obj.image} -> {folder}/{f}')
                obj.image = f'{folder}/{f}'
                obj.save()
                break

# UserCar
for obj in UserCar.objects.exclude(image=''):
    if obj.image and str(obj.image) not in media_files:
        folder = 'car_images'
        folder_path = os.path.join(MEDIA_ROOT, folder)
        if not os.path.exists(folder_path):
            print(f"Klasör yok: {folder_path}, atlanıyor.")
            continue
        base = os.path.splitext(os.path.basename(str(obj.image)))[0]
        ext = os.path.splitext(str(obj.image))[1]
        for f in os.listdir(folder_path):
            if f.startswith(base) and f.endswith(ext):
                print(f'UserCar: {obj.image} -> {folder}/{f}')
                obj.image = f'{folder}/{f}'
                obj.save()
                break

print('Veritabanındaki tüm görsel yolları dosya sistemiyle eşleştirildi ve düzeltildi.') 