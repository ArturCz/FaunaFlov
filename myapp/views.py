from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Plant, WateringSchedule, Category, Photo, Notification
from myapp.utils import send_telegram_message


# Widok do logowania
class Login_page(LoginView):
    template_name = 'login.html'


# Widok do strony głównej + testowe wysyłanie wiadomości przez bota
class Main_Page(LoginRequiredMixin, View):
    def get(self, request):
        chat_id = int(1973369305)  # ID testowego użytkownika Telegram
        send_telegram_message(chat_id, message='coderslab')  # Testowe wysyłanie wiadomości
        return render(request, 'main.html')


# Widok do dodawania roślin
class Add_Palnt(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()  # Pobieranie dostępnych kategorii do formularza
        return render(request, "add_plant.html", {'categories': categories})

    def post(self, request):
        # Pobieranie danych z formularza
        name = request.POST.get('name')
        watering_interval = request.POST.get('watering_interval')
        photo_file = request.FILES.get('photo')
        categories = request.POST.getlist('categories')  # Pobieranie wybranych kategorii (relacja Many-to-Many)

        if name == "":  # Sprawdzanie, czy nazwa rośliny została podana
            return redirect('add_plant')

        # Obsługa zdjęcia rośliny (jeśli nie podano, przypisywany jest obraz domyślny)
        if photo_file:
            photo = Photo(image=photo_file)
            photo.save()
        else:
            default_image_path = 'plant_photos/default_plant.jpg'  # Ścieżka do domyślnego zdjęcia
            photo = Photo(image=default_image_path)
            photo.save()

        # Tworzenie obiektu Plant
        plant = Plant(
            name=name,
            photo=photo,  # Przypisanie zdjęcia do rośliny
            user=request.user  # Przypisanie rośliny do zalogowanego użytkownika
        )
        plant.save()

        # Tworzenie obiektu WateringSchedule
        if type(watering_interval) == int:
            water = WateringSchedule(
                plant=plant,
                watering_interval=watering_interval  # Przypisanie interwału podlewania
            )
            water.save()
        else:
            water = WateringSchedule(
                plant=plant,
            )
            water.save()

        # Przypisywanie relacji Many-to-Many (kategorie)
        if categories:
            plant.categories.set(categories)

        return redirect('add_plant')  # Przekierowanie po zapisaniu rośliny


# Widok do przeglądania roślin użytkownika
class My_plants(LoginRequiredMixin, View):
    def get(self, request):
        plants = Plant.objects.filter(user=request.user)  # Pobieranie roślin zalogowanego użytkownika
        return render(request, 'my_plants.html', {'plants': plants})

    def post(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk, user=request.user)  # Pobieranie konkretnej rośliny użytkownika
        plant.last_watered = timezone.now()  # Aktualizacja czasu ostatniego podlewania
        plant.save()
        return redirect('my_plants')  # Przekierowanie po zapisaniu zmian


# Widok do zarządzania powiadomieniami
class Notifications(LoginRequiredMixin, View):
    def get(self, request):
        plants = Plant.objects.filter(user=request.user)  # Pobieranie roślin użytkownika do wyboru w formularzu
        return render(request, 'nottifcation.html', {'plants': plants})

    def post(self, request):
        plant_id = request.POST.get('plant')  # Pobieranie wybranej rośliny
        telegram_id = request.POST.get('telegram_id')  # Pobieranie ID Telegrama użytkownika
        message = request.POST.get('message')  # Pobieranie wiadomości do wysłania

        if telegram_id == "":  # Sprawdzanie, czy podano ID Telegrama
            plants = Plant.objects.filter(user=request.user)
            return render(request, 'nottifcation.html', {'plants': plants})

        plant = Plant.objects.get(id=plant_id, user=request.user)  # Pobieranie rośliny przypisanej do użytkownika
        notification = Notification.objects.create(
            user=request.user,
            plant=plant,
            telegram_id=telegram_id,
            message=message
        )
        notification.save()
        plants = Plant.objects.filter(user=request.user)
        return render(request, 'nottifcation.html', {'plants': plants})


# Widok detali rośliny
class Plant_details(LoginRequiredMixin, View):
    def get(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk, user=request.user)  # Pobieranie konkretnej rośliny
        print(plant.photo.image.url)

        photo_url = plant.photo.image.url  # Pobieranie URL zdjęcia rośliny

        return render(request, 'plant_details.html', {
            'plant': plant,
            'name': plant.name,
            'last_watered': plant.last_watered,
            'photo_url': photo_url,
            'categories': plant.categories.all(),
        })


# Widok do wylogowywania użytkownika
class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)  # Wylogowanie użytkownika
        return redirect('login')  # Przekierowanie na stronę logowania
