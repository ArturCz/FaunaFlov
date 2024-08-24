import pytest
from django.urls import reverse
from myapp.models import Plant

@pytest.mark.django_db
def test_add_plant_page_status(client, django_user_model):
    # Logowanie użytkownika
    username = 'testuser'
    password = 'password123'
    user = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)

    # Sprawdzenie, czy strona dodawania rośliny zwraca poprawny status HTTP 200
    url = reverse('add_plant')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Enter plant name' in response.content.decode()

@pytest.mark.django_db
def test_add_plant(client, django_user_model):
    # Logowanie użytkownika
    username = 'testuser'
    password = 'password123'
    user = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)

    # Dane do formularza
    data = {
        'name': 'Test Plant',
        'watering_interval': 7,
        'categories': []
    }

    # Wysłanie formularza
    url = reverse('add_plant')
    response = client.post(url, data)

    # Sprawdzenie, czy roślina została dodana
    assert Plant.objects.filter(name='Test Plant', user=user).exists()
    assert response.status_code == 302  # Przekierowanie po dodaniu

@pytest.mark.django_db
def test_add_plant_missing_name(client, django_user_model):
    # Logowanie użytkownika
    username = 'testuser'
    password = 'password123'
    user = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)

    # Dane do formularza bez nazwy rośliny
    data = {
        'name': '',
        'watering_interval': 7,
        'categories': []
    }

    # Wysłanie formularza
    url = reverse('add_plant')
    response = client.post(url, data)

    # Sprawdzenie, czy strona ponownie się załadowała z błędem
    assert response.status_code == 200

