import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url,template",
    [
        ("home", "pages/index.html"),
        ("about", "pages/about.html"),
        ("contact", "pages/contact.html"),
        ("service", "pages/service.html"),
        ("team", "pages/team.html"),
        ("blog", "pages/blog-three-column.html"),
    ],
)
def test_pages(client, url, template):
    response = client.get(reverse(f'pages:{url}'))
    assert response.status_code == 200
    assert template in [t.name for t in response.templates]