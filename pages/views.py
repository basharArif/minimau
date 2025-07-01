from django.views.generic import TemplateView, DetailView
from django.shortcuts import render
from cms_content.models import Product, PageContent, Service, Feature, TimelineEvent, Capability


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

class SearchView(TemplateView):
    template_name = "pages/search.html"

# Remove Product7View as it will be handled by ProductDetailView
# Remove service_view, service_non_gps_view, service_nature_digitization_view, service_crowd_monitoring_view
# as they will be handled by ServiceView or ServiceDetailView
