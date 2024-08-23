import pytest
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from myapp.models import Plant

@pytest.mark.django_db
def test_my_plants_view_post(client):
    user = User.objects.create_user(username='testuser', password='789789789')
    client.login(username='testuser', password='789789789')

    plant = Plant.objects.create(name='Rose', user=user)

    assert plant.last_watered is not None
    original_last_watered = plant.last_watered

    # Post do widoku
    url = reverse('water_plant', args=[plant.pk])
    response = client.post(url)

    # Refresh na strone
    plant.refresh_from_db()

    # Check czy sie rozni
    assert plant.last_watered > original_last_watered

    # Check na przekierowanie
    assert response.status_code == 302
    assert response.url == reverse('my_plants')
