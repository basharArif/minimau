
import pytest
from io import StringIO
import os
from django.core.management import call_command
from cms_content.models import Product, Service

@pytest.mark.django_db
def test_populate_cms_data_command(tmp_path):
    """Test the populate_cms_data management command."""
    # Create a dummy extracted_content.json file in the project root
    json_content = '''
    {
        "page_contents": [],
        "products": [
            {
                "model": "cms_content.Product",
                "fields": {
                    "name": "Test Product from Command",
                    "short_description": "A short description.",
                    "hero_image": "test_hero.jpg",
                    "hero_image_alt_text": "Test Hero Image",
                    "main_description": "Main description of the test product.",
                    "conclusion_text": "Conclusion of the test product.",
                    "url_slug": "test-product-from-command",
                    "order": 1
                }
            }
        ],
        "services": [],
        "features": [],
        "timeline_events": [],
        "capabilities": [],
        "call_to_actions": []
    }
    '''
    json_file_path = os.path.join(os.getcwd(), "extracted_content.json")
    with open(json_file_path, "w") as f:
        f.write(json_content)

    # Run the command
    out = StringIO()
    call_command("populate_cms_data", stdout=out)

    # Check the output
    output = out.getvalue()
    assert "CMS data population complete." in output

    # Check that the data was created
    assert Product.objects.filter(name="Test Product from Command").exists()

    # Clean up the dummy file
    os.remove(json_file_path)

@pytest.mark.django_db
def test_populate_cms_data_file_not_found():
    """Test the populate_cms_data command when the JSON file is not found."""
    out = StringIO()
    call_command("populate_cms_data", stdout=out)
    output = out.getvalue()
    assert "Error: The file extracted_content.json was not found." in output

@pytest.mark.django_db
def test_populate_cms_data_invalid_json(tmp_path):
    """Test the populate_cms_data command with invalid JSON."""
    json_content = '{"products": [{"model": "cms_content.Product", "fields":,}]}'
    json_file_path = os.path.join(os.getcwd(), "extracted_content.json")
    with open(json_file_path, "w") as f:
        f.write(json_content)

    out = StringIO()
    call_command("populate_cms_data", stdout=out)
    output = out.getvalue()
    assert "Error: Invalid JSON" in output

    os.remove(json_file_path)

@pytest.mark.django_db
def test_populate_cms_data_update(tmp_path):
    """Test that the populate_cms_data command updates existing data."""
    # First, create a product
    Product.objects.create(name="Test Product", url_slug="test-product", short_description="Initial description")

    # Now, create a JSON file with the same product but a new description
    json_content = '''
    {
        "page_contents": [],
        "products": [
            {
                "model": "cms_content.Product",
                "fields": {
                    "name": "Test Product",
                    "url_slug": "test-product",
                    "short_description": "Updated description."
                }
            }
        ],
        "services": [],
        "features": [],
        "timeline_events": [],
        "capabilities": [],
        "call_to_actions": []
    }
    '''
    json_file_path = os.path.join(os.getcwd(), "extracted_content.json")
    with open(json_file_path, "w") as f:
        f.write(json_content)

    out = StringIO()
    call_command("populate_cms_data", stdout=out)
    output = out.getvalue()
    assert "CMS data population complete." in output

    # Check that the product was updated
    product = Product.objects.get(name="Test Product")
    assert product.short_description == "Updated description."

    os.remove(json_file_path)
