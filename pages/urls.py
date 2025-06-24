from django.urls import path

from .views import StaticTemplateView

urlpatterns = [
    path("", StaticTemplateView.as_view(template_name="pages/index.html"), name="home"),  # noqa: E501
    path(
        "about/",
        StaticTemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(
        "contact/",
        StaticTemplateView.as_view(template_name="pages/contact.html"),
        name="contact",
    ),
    path(
        "service/",
        StaticTemplateView.as_view(template_name="pages/service.html"),
        name="service",
    ),
    path(
        "team/",
        StaticTemplateView.as_view(template_name="pages/team.html"),
        name="team",
    ),
    path(
        "blog/",
        StaticTemplateView.as_view(template_name="pages/blog-three-column.html"),  # noqa: E501
        name="blog",
    ),
    path(
        "blog/post/",
        StaticTemplateView.as_view(
            template_name="pages/blog-details-left-sidebar.html"
        ),
        name="blog-post",
    ),
]

for i in range(1, 7):
    urlpatterns.append(
        path(
            f"products/{i}/",
            StaticTemplateView.as_view(template_name=f"pages/product{i}.html"),
            name=f"product-{i}",
        )
    )
