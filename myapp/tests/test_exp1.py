import pytest
from django.contrib.auth.models import User
from myapp.models import Plant


@pytest.mark.django_db
def test_create_plant():
    user = User.objects.create_user(username='testuser', password='12345')
    plant = Plant.objects.create(name='Rose', user=user)

    assert plant.name == 'Rose'
    assert plant.user.username == 'testuser'
