import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    "url,template",
    [
        ("home", "pages/index.html"),
        ("about", "pages/about.html"),
        ("contact", "pages/contact.html"),
        ("service", "pages/service.html"),
        ("team", "pages/team.html"),
        ("team-dark", "pages/team-dark.html"),
        ("blog", "pages/blog-three-column.html"),
        ("blog-post", "pages/blog-details-left-sidebar.html"),
    ]
    + [(f"product-{i}", f"pages/product{i}.html") for i in range(1, 7)],
)
def test_pages(client, url, template):
    response = client.get(reverse(url))
    assert response.status_code == 200
    assert template in [t.name for t in response.templates]
