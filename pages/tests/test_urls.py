import pytest
from django.urls import reverse, resolve
from pages import views

@pytest.mark.django_db
class TestUrls:
    def test_home_url(self):
        url = reverse('pages:home')
        assert resolve(url).func.view_class == views.HomeView

    def test_about_url(self):
        url = reverse('pages:about')
        assert resolve(url).func.view_class == views.AboutView

    def test_contact_url(self):
        url = reverse('pages:contact')
        assert resolve(url).func.view_class.__name__ == 'TemplateView'

    def test_service_url(self):
        url = reverse('pages:service')
        assert resolve(url).func.view_class == views.ServiceView

    def test_service_detail_url(self):
        url = reverse('pages:service_detail', kwargs={'url_slug': 'some-slug'})
        assert resolve(url).func.view_class == views.ServiceDetailView

    def test_search_url(self):
        url = reverse('pages:search')
        assert resolve(url).func.view_class == views.SearchView

    def test_team_url(self):
        url = reverse('pages:team')
        assert resolve(url).func.view_class.__name__ == 'TemplateView'

    def test_blog_url(self):
        url = reverse('pages:blog')
        assert resolve(url).func.view_class.__name__ == 'TemplateView'

    def test_product_detail_url(self):
        url = reverse('pages:product_detail', kwargs={'url_slug': 'some-slug'})
        assert resolve(url).func.view_class == views.ProductDetailView
