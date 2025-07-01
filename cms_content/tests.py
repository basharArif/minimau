
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify
from .models import (
    Product,
    ProductImage,
    ProductSection,
    ProductSectionItem,
    Service,
    Feature,
    TimelineEvent,
    Capability,
    PageContent,
    CallToAction,
)

@pytest.mark.django_db
def test_product_creation():
    """Test the creation of a Product instance."""
    product = Product.objects.create(
        name="Test Product",
        short_description="A short description.",
        hero_image=SimpleUploadedFile("test_hero.jpg", b"file_content", content_type="image/jpeg"),
        hero_image_alt_text="Test Hero Image",
        main_description="Main description of the test product.",
        conclusion_text="Conclusion of the test product.",
        url_slug="test-product",
        order=1,
    )
    assert product.name == "Test Product"
    assert product.url_slug == "test-product"
    assert str(product) == "Test Product"

@pytest.mark.django_db
def test_service_creation():
    """Test the creation of a Service instance."""
    service = Service.objects.create(
        name="Test Service",
        short_description="A short description of the service.",
        image=SimpleUploadedFile("test_service.jpg", b"file_content", content_type="image/jpeg"),
        image_alt_text="Test Service Image",
        url_slug="test-service",
        order=1,
    )
    assert service.name == "Test Service"
    assert service.url_slug == "test-service"
    assert str(service) == "Test Service"

@pytest.mark.django_db
def test_page_content_creation():
    """Test the creation of a PageContent instance."""
    page_content = PageContent.objects.create(
        page_name="home",
        section_identifier="hero",
        title="Welcome to our Website",
        subtitle="The best place for all your needs.",
        body_text="This is the main content of the hero section.",
        order=1,
    )
    assert page_content.title == "Welcome to our Website"
    assert str(page_content) == "home - hero"

@pytest.mark.django_db
def test_call_to_action_creation():
    """Test the creation of a CallToAction instance."""
    page_content = PageContent.objects.create(page_name="home", section_identifier="cta")
    cta = CallToAction.objects.create(
        page_content=page_content,
        button_text="Click Me",
        button_url="https://example.com",
        order=1,
    )
    assert cta.button_text == "Click Me"
    assert str(cta) == "Click Me (home - cta)"
