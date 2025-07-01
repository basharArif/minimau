from django.urls import path
from . import views

app_name = 'cms_content'

urlpatterns = [
    path('case-studies/', views.case_studies, name='case_studies'),
    path('white-papers/', views.white_papers, name='white_papers'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
]
