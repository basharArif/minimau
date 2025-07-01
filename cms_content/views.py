from django.shortcuts import render, get_object_or_404
from .models import CaseStudy, WhitePaper, Blog

def case_studies(request):
    case_studies = CaseStudy.objects.all()
    return render(request, 'pages/case_studies.html', {'case_studies': case_studies})

def white_papers(request):
    white_papers = WhitePaper.objects.all()
    return render(request, 'pages/white_papers.html', {'white_papers': white_papers})

def blog_detail(request, slug):
    blog_post = get_object_or_404(Blog, url_slug=slug)
    return render(request, 'pages/blog-details-left-sidebar.html', {'blog_post': blog_post})
