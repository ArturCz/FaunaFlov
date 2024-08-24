import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_login_page_status(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_page_template(client):
    url = reverse('login')
    response = client.get(url)
    assert 'login.html' in (t.name for t in response.templates)

@pytest.mark.django_db
def test_login_with_valid_credentials(client):
    # Utwórz użytkownika testowego
    user = User.objects.create_user(username='testuser', password='password123')

    # Spróbuj zalogować się przy użyciu poprawnych danych logowania
    url = reverse('login')
    response = client.post(url, {'username': 'testuser', 'password': 'password123'})

    # Sprawdź, czy użytkownik został przekierowany po zalogowaniu
    assert response.status_code == 302
    assert response.url == reverse('main')

