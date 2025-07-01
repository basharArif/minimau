
import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from cms_content.models import Product, Service

@pytest.fixture
def test_product(db):
    """Fixture to create a test product."""
    return Product.objects.create(
        name="Test Product",
        short_description="A short description.",
        hero_image=SimpleUploadedFile("test_hero.jpg", b"file_content", content_type="image/jpeg"),
        hero_image_alt_text="Test Hero Image",
        main_description="Main description of the test product.",
        conclusion_text="Conclusion of the test product.",
        url_slug="test-product",
        order=1,
    )

@pytest.fixture
def test_service(db):
    """Fixture to create a test service."""
    return Service.objects.create(
        name="Test Service",
        short_description="A short description of the service.",
        image=SimpleUploadedFile("test_service.jpg", b"file_content", content_type="image/jpeg"),
        image_alt_text="Test Service Image",
        url_slug="test-service",
        order=1,
    )

@pytest.mark.django_db
def test_product_detail_view(client, test_product):
    """Test the product detail view."""
    url = reverse("pages:product_detail", kwargs={"url_slug": test_product.url_slug})
    response = client.get(url)
    assert response.status_code == 200
    assert "pages/product_detail.html" in [t.name for t in response.templates]
    assert response.context["product"].name == test_product.name

@pytest.mark.django_db
def test_product_detail_view_not_found(client):
    """Test the product detail view for a 404 error."""
    url = reverse("pages:product_detail", kwargs={"url_slug": "non-existent-product"})
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_service_detail_view_not_found(client):
    """Test the service detail view for a 404 error."""
    url = reverse("pages:service_detail", kwargs={"url_slug": "non-existent-service"})
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_search_view(client, test_product):
    """Test the search view."""
    url = reverse("pages:search")
    response = client.get(url, {"q": "Test"})
    assert response.status_code == 200
    assert "pages/search.html" in [t.name for t in response.templates]
    assert "Test Product" in response.content.decode()

@pytest.mark.django_db
def test_custom_500_view(client, monkeypatch):
    """Test the custom 500 view."""
    from pages.views import HomeView

    def error_get(self, request, *args, **kwargs):
        raise Exception("Making a 500 error")

    monkeypatch.setattr(HomeView, 'get', error_get)

    with pytest.raises(Exception):
        client.get(reverse('pages:home'))
