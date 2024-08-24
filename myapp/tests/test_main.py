import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_main_page_status(client, django_user_model):
    # Logowanie użytkownika
    username = 'testuser'
    password = 'password123'
    user = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)

    # Sprawdzenie, czy strona główna zwraca status 200
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 200
    assert 'FaunaFlov is' in response.content.decode()  # Sprawdzenie, czy strona zawiera odpowiedni tekst


@pytest.mark.django_db
def test_main_page_links(client, django_user_model):
    # Logowanie użytkownika
    username = 'testuser'
    password = 'password123'
    user = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)

    # Sprawdzenie, czy linki na stronie głównej są dostępne
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 200

    # Sprawdzenie, czy linki do innych stron są obecne
    assert reverse('add_plant') in response.content.decode()
    assert reverse('my_plants') in response.content.decode()
    assert reverse('notifications') in response.content.decode()
    assert reverse('logout') in response.content.decode()


@pytest.mark.django_db
def test_main_page_redirect_for_anonymous_user(client):
    # Sprawdzenie, czy niezalogowany użytkownik jest przekierowany na stronę logowania
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 302  # Sprawdzenie, czy nastąpiło przekierowanie
    assert response.url == f"{reverse('login')}?next={url}"  # Sprawdzenie poprawnego przekierowania z parametrem next
