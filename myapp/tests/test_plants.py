import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import Plant

#check czy sie wyswietla roslina
@pytest.mark.django_db
def test_my_plants_view(client):
    user = User.objects.create_user(username='testuser', password='789789789')
    client.login(username='testuser', password='789789789')

    Plant.objects.create(name='Rose', user=user)

    url = reverse('my_plants')
    response = client.get(url)

    assert response.status_code == 200
    assert 'Rose' in response.content.decode()