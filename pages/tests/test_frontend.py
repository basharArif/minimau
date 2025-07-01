import os
from bs4 import BeautifulSoup
import pytest
from django.urls import reverse, resolve
from django.conf import settings
from django.views.generic import TemplateView
import sitecore.urls
from pages.views import (
    HomeView,
    ServiceView,
    SearchView,
    AboutView,
    ProductDetailView,
    ServiceDetailView,
)

# Collect URL patterns from pages/urls.py
URLS = [
    ("home", "pages/index.html", HomeView),
    ("about", "pages/about.html", AboutView),
    ("contact", "pages/contact.html", TemplateView),
    ("service", "pages/service.html", ServiceView),
    ("team", "pages/team.html", TemplateView),
    ("blog", "pages/blog-three-column.html", TemplateView),
    ("search", "pages/search.html", SearchView),
    ("product_detail", "pages/product_detail.html", ProductDetailView),
    ("service_detail", "pages/service_detail.html", ServiceDetailView),
]


@pytest.mark.django_db
@pytest.mark.parametrize("name, template, view", URLS)
def test_url_resolution(name, template, view):
    if name == "product_detail":
        url = reverse(f'pages:{name}', kwargs={'url_slug': 'test-product'})
    elif name == "service_detail":
        url = reverse(f'pages:{name}', kwargs={'url_slug': 'test-service'})
    else:
        url = reverse(f'pages:{name}')
    match = resolve(url)
    if hasattr(match.func, 'view_class'):
        assert match.func.view_class is view
    else:
        assert match.func is view
    if view is TemplateView:
        assert match.func.view_initkwargs["template_name"] == template


@pytest.mark.django_db
@pytest.mark.parametrize("name, _template, _view", URLS)
def test_html_structure(client, name, _template, _view):
    if name == "product_detail":
        # Create a dummy product for testing
        from cms_content.models import Product
        Product.objects.create(
            name="Test Product",
            short_description="A short description.",
            hero_image='product_heroes/test_hero.jpg',
            hero_image_alt_text="Test Hero Image",
            main_description="Main description of the test product.",
            url_slug="test-product",
            order=1
        )
        response = client.get(reverse(f'pages:{name}', kwargs={'url_slug': 'test-product'}))
    elif name == "service_detail":
        # Create a dummy service for testing
        from cms_content.models import Service
        Service.objects.create(
            name="Test Service",
            short_description="A short description.",
            image='service_images/test_service.jpg',
            image_alt_text="Test Service Image",
            url_slug="test-service",
            order=1
        )
        response = client.get(reverse(f'pages:{name}', kwargs={'url_slug': 'test-service'}))
    else:
        response = client.get(reverse(f'pages:{name}'))
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.html and soup.head and soup.body
    assert soup.title is not None

    # verify static asset references exist
    for tag in soup.find_all(src=True):
        src = tag["src"]
        if src.startswith(settings.STATIC_URL):
            rel_path = src[len(settings.STATIC_URL) :]
            found = any(
                os.path.exists(os.path.join(static_dir, rel_path))
                for static_dir in settings.STATICFILES_DIRS
            )
            assert found, f"Missing static asset: {src}"


def test_root_url_configuration():
    import pages.urls

    assert any(
        getattr(p.pattern, "_route", None) == ""
        and getattr(p, "urlconf_name", None) is pages.urls
        for p in sitecore.urls.urlpatterns
    )