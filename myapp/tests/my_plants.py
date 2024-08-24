import pytest
from django.urls import reverse
from django.utils import timezone
from myapp.models import Plant, User

@pytest.mark.django_db
def test_my_plants_view_display(client, django_user_model):
    # Tworzenie użytkownika i zalogowanie
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    # Tworzenie przykładowej rośliny
    plant = Plant.objects.create(name='Aloe Vera', user=user)

    # Sprawdzenie wyświetlania listy roślin
    url = reverse('my_plants')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Aloe Vera' in response.content.decode()


@pytest.mark.django_db
def test_my_plants_view_no_plants(client, django_user_model):
    # Tworzenie użytkownika i zalogowanie
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    # Sprawdzenie wyświetlania komunikatu, gdy brak roślin
    url = reverse('my_plants')
    response = client.get(url)
    assert response.status_code == 200
    assert 'You have no plants.' in response.content.decode()


@pytest.mark.django_db
def test_my_plants_view_water_plant(client, django_user_model):
    # Tworzenie użytkownika i zalogowanie
    user = django_user_model.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    # Tworzenie przykładowej rośliny
    plant = Plant.objects.create(name='Aloe Vera', user=user)
    original_last_watered = plant.last_watered

    # Akcja podlewania rośliny
    url = reverse('water_plant', args=[plant.pk])
    response = client.post(url)

    # Sprawdzenie, czy czas ostatniego podlewania został zaktualizowany
    plant.refresh_from_db()
    assert response.status_code == 302  # Przekierowanie po sukcesie
    assert plant.last_watered > original_last_watered
