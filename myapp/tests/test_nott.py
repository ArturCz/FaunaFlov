import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import Plant, Notification

@pytest.mark.django_db
def test_notification_form_display(client, django_user_model):
    # Tworzenie użytkownika i logowanie
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    # Tworzenie przykładowej rośliny
    Plant.objects.create(name='Aloe Vera', user=user)

    # Sprawdzenie wyświetlania formularza
    url = reverse('notifications')
    response = client.get(url)
    assert response.status_code == 200
    assert b'Enter your Telegram ID' in response.content

@pytest.mark.django_db
def test_notification_creation(client, django_user_model):
    # Tworzenie użytkownika i logowanie
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    # Tworzenie przykładowej rośliny
    plant = Plant.objects.create(name='Aloe Vera', user=user)

    # Wysyłanie formularza z danymi
    url = reverse('notifications')
    data = {
        'plant': plant.id,
        'telegram_id': '123456789',
        'message': 'Remember to water your plant!',
    }
    response = client.post(url, data)

    # Sprawdzenie, czy powiadomienie zostało zapisane
    assert response.status_code == 200
    assert Notification.objects.filter(user=user, plant=plant).exists()

@pytest.mark.django_db
def test_notification_creation_missing_telegram_id(client, django_user_model):
    # Tworzenie użytkownika i logowanie
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    # Tworzenie przykładowej rośliny
    plant = Plant.objects.create(name='Aloe Vera', user=user)

    # Wysyłanie formularza bez ID Telegrama
    url = reverse('notifications')
    data = {
        'plant': plant.id,
        'telegram_id': '',
        'message': 'Remember to water your plant!',
    }
    response = client.post(url, data)

    # Sprawdzenie, czy powiadomienie nie zostało zapisane i zwrócono formularz z błędami
    assert response.status_code == 200
    assert b'Telegram ID' in response.content
    assert not Notification.objects.filter(user=user, plant=plant).exists()
