import pytest
from django.urls import reverse
from django.test import Client

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_homepage_loads_correctly(client):
    response = client.get(reverse('pages:home'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_about_page_loads_correctly(client):
    response = client.get(reverse('pages:about'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_contact_page_loads_correctly(client):
    response = client.get(reverse('pages:contact'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_main_service_page_loads_correctly(client):
    response = client.get(reverse('pages:service'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_blog_listing_page_loads_correctly(client):
    response = client.get(reverse('pages:blog'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_team_page_loads_correctly(client):
    response = client.get(reverse('pages:team'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_search_page_loads_correctly(client):
    response = client.get(reverse('pages:search'))
    assert response.status_code == 200

