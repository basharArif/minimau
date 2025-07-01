from django.views.generic import TemplateView, DetailView, ListView
from django.shortcuts import render
from cms_content.models import Product, PageContent, Service, Feature, TimelineEvent, Capability, Blog, CaseStudy, WhitePaper
from django.db.models import Q


class StaticTemplateView(TemplateView):
    template_name = ""

def custom_500_view(request):
    return render(request, "pages/500.html", status=500)

class HomeView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('order')
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product_detail.html'
    context_object_name = 'product'
    slug_field = 'url_slug'
    slug_url_kwarg = 'url_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_images'] = self.object.images.all().order_by('order')
        context['product_sections'] = self.object.sections.all().order_by('order')
        for section in context['product_sections']:
            section.items_list = section.items.all().order_by('order')
        return context

class ServiceView(TemplateView):
    template_name = "pages/service.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all().order_by('order')
        context['hero_content'] = PageContent.objects.filter(page_name='service', section_identifier='hero_section').first()
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'pages/service_detail.html'
    context_object_name = 'service'
    slug_field = 'url_slug'
    slug_url_kwarg = 'url_slug'

class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_content'] = PageContent.objects.filter(page_name='about', section_identifier='hero_section').first()
        context['mission_content'] = PageContent.objects.filter(page_name='about', section_identifier='mission_section').first()
        context['vision_content'] = PageContent.objects.filter(page_name='about', section_identifier='vision_section').first()
        context['cta_content'] = PageContent.objects.filter(page_name='about', section_identifier='cta_section').first()
        if context['cta_content']:
            context['cta_buttons'] = context['cta_content'].call_to_actions.all().order_by('order')
        context['capabilities'] = Capability.objects.all().order_by('order')
        context['features'] = Feature.objects.all().order_by('order')
        context['timeline_events'] = TimelineEvent.objects.all().order_by('order')
        return context

class CaseStudiesView(TemplateView):
    template_name = "pages/case-studies.html"

class WhitePapersView(TemplateView):
    template_name = "pages/white-papers.html"

class SearchView(ListView):
    template_name = "pages/search.html"
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            products = Product.objects.filter(Q(name__icontains=query) | Q(short_description__icontains=query))
            services = Service.objects.filter(Q(name__icontains=query) | Q(short_description__icontains=query))
            blogs = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
            case_studies = CaseStudy.objects.filter(Q(title__icontains=query) | Q(short_description__icontains=query))
            white_papers = WhitePaper.objects.filter(Q(title__icontains=query) | Q(short_description__icontains=query))

            # Combine querysets
            results = list(products) + list(services) + list(blogs) + list(case_studies) + list(white_papers)
            return results
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

# Remove Product7View as it will be handled by ProductDetailView
# Remove service_view, service_non_gps_view, service_nature_digitization_view, service_crowd_monitoring_view
# as they will be handled by ServiceView or ServiceDetailView


class ContactView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_content'] = PageContent.objects.filter(page_name='contact', section_identifier='contact_section').first()
        return context

class BlogView(TemplateView):
    template_name = "pages/blog-grid-left-sidebar.html"

class BlogDetailView(TemplateView):
    template_name = "pages/blog-details-left-sidebar.html"

class PortfolioView(TemplateView):
    template_name = "pages/portfolio-details.html"

class TeamView(TemplateView):
    template_name = "pages/team.html"

class FaqView(TemplateView):
    template_name = "pages/faq.html"

class Error404View(TemplateView):
    template_name = "pages/404.html"

class Error500View(TemplateView):
    template_name = "pages/500.html"

class ForgetPasswordView(TemplateView):
    template_name = "pages/forget-password.html"

class LoginView(TemplateView):
    template_name = "pages/login.html"

class RegisterView(TemplateView):
    template_name = "pages/register.html"

class PrivacyPolicyView(TemplateView):
    template_name = "pages/privacy-policy.html"

class TermsOfServiceView(TemplateView):
    template_name = "pages/terms-of-service.html"

class ComingSoonView(TemplateView):
    template_name = "pages/coming-soon.html"