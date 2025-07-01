from django import template
from cms_content.models import Product

register = template.Library()

@register.simple_tag
def get_products():
    return Product.objects.all()