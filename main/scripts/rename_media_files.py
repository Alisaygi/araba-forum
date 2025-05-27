import os
from unidecode import unidecode
import django
import sys

# Proje kök dizinini sys.path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')
django.setup()

from main.models import CarNews, UserCar

MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')

folders = ['news_images', 'car_images']

for folder in folders:
    folder_path = os.path.join(MEDIA_ROOT, folder)
    if not os.path.exists(folder_path):
        continue
    for filename in os.listdir(folder_path):
        new_filename = unidecode(filename)
        if new_filename != filename:
            src = os.path.join(folder_path, filename)
            dst = os.path.join(folder_path, new_filename)
            os.rename(src, dst)
            print(f"Renamed: {filename} -> {new_filename}")
            # Veritabanında güncelle
            if folder == 'news_images':
                CarNews.objects.filter(image=f'{folder}/{filename}').update(image=f'{folder}/{new_filename}')
            elif folder == 'car_images':
                UserCar.objects.filter(image=f'{folder}/{filename}').update(image=f'{folder}/{new_filename}')

print("Tüm dosya adları ve veritabanı yolları güncellendi.") 