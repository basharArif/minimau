import os
from bs4 import BeautifulSoup
import pytest
from django.urls import reverse, resolve
from django.conf import settings
import sitecore.urls
from pages.views import StaticTemplateView

# Collect URL patterns from pages/urls.py
URLS = [
    ("home", "pages/index.html"),
    ("about", "pages/about.html"),
    ("contact", "pages/contact.html"),
    ("service", "pages/service.html"),
    ("team", "pages/team.html"),
    ("team-dark", "pages/team-dark.html"),
    ("blog", "pages/blog-three-column.html"),
    ("blog-post", "pages/blog-details-left-sidebar.html"),
] + [(f"product-{i}", f"pages/product{i}.html") for i in range(1, 7)]


@pytest.mark.parametrize("name, template", URLS)
def test_url_resolution(name, template):
    match = resolve(reverse(name))
    assert match.func.view_class is StaticTemplateView
    assert match.func.view_initkwargs["template_name"] == template


@pytest.mark.parametrize("name, _template", URLS)
def test_html_structure(client, name, _template):
    response = client.get(reverse(name))
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.html and soup.head and soup.body
    assert soup.title is not None

    # verify static asset references exist
    for tag in soup.find_all(src=True):
        src = tag["src"]
        if src.startswith(settings.STATIC_URL):
            rel_path = src[len(settings.STATIC_URL):]
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
