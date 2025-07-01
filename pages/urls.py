from django.urls import path
from django.views.generic import TemplateView # Import TemplateView

app_name = 'pages'

from .views import (
    HomeView,
    ProductDetailView,
    ServiceView,
    ServiceDetailView,
    AboutView,
    SearchView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", TemplateView.as_view(template_name="pages/contact.html"), name="contact"),
    path("service/", ServiceView.as_view(), name="service"),
    path("service/<slug:url_slug>/", ServiceDetailView.as_view(), name="service_detail"),
    path("search/", SearchView.as_view(), name="search"),
    path("team/", TemplateView.as_view(template_name="pages/team.html"), name="team"),
    path("blog/", TemplateView.as_view(template_name="pages/blog-three-column.html"), name="blog"),
    path("products/<str:url_slug>/", ProductDetailView.as_view(), name="product_detail"),
]

# 404 page
urlpatterns.append(
    path(
        "404/",
        TemplateView.as_view(template_name="pages/404.html"),
        name="404",
    )
)
