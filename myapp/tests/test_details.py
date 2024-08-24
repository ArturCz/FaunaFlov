import pytest
from django.urls import reverse
from myapp.models import Plant, Category, Photo, User
from django.test import Client

@pytest.mark.django_db
def test_plant_details_view_display(client, django_user_model):
    # Tworzenie użytkownika i logowanie
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    # Tworzenie przykładowej rośliny z kategoriami
    plant = Plant.objects.create(name='Aloe Vera', user=user)
    category1 = Category.objects.create(name='Indoor')
    category2 = Category.objects.create(name='Succulent')
    plant.categories.add(category1, category2)

    # Sprawdzenie wyświetlania szczegółów rośliny
    url = reverse('plant_details', args=[plant.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert 'Aloe Vera' in response.content.decode()
    assert 'Indoor' in response.content.decode()
    assert 'Succulent' in response.content.decode()


@pytest.mark.django_db
def test_plant_details_view_with_photo(client, django_user_model):
    # Tworzenie użytkownika i logowanie
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    # Tworzenie przykładowej rośliny z kategorią i zdjęciem
    photo = Photo.objects.create(image='plant_photos/aloe_vera.jpg')
    plant = Plant.objects.create(name='Aloe Vera', user=user, photo=photo)

    # Sprawdzenie wyświetlania zdjęcia rośliny
    url = reverse('plant_details', args=[plant.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert 'src="/media/plant_photos/aloe_vera.jpg"' in response.content.decode()


@pytest.mark.django_db
def test_plant_details_view_no_photo(client, django_user_model):
    # Tworzenie użytkownika i logowanie
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    # Tworzenie przykładowej rośliny bez zdjęcia
    plant = Plant.objects.create(name='Aloe Vera', user=user)

    # Sprawdzenie wyświetlania komunikatu, gdy brak zdjęcia
    url = reverse('plant_details', args=[plant.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert 'No photo available.' in response.content.decode()
