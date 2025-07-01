import json
from django.core.management.base import BaseCommand
from django.db import transaction
from cms_content.models import (
    PageContent,
    CallToAction,
    Product,
    ProductImage,
    ProductSection,
    ProductSectionItem,
    Service,
    Feature,
    TimelineEvent,
    Capability,
)

from django.utils.text import slugify

import os
from django.conf import settings

# ... (rest of the imports)

class Command(BaseCommand):
    help = 'Populates the CMS database with initial content from extracted_content.json'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting CMS data population...'))

        json_file_path = os.path.join(settings.BASE_DIR, 'extracted_content.json')
        try:
            with open(json_file_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Error: The file extracted_content.json was not found.'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error: Invalid JSON in extracted_content.json.'))
            return

        # Dictionaries to store mappings from slug/identifier to actual model instances
        # This is crucial for resolving ForeignKey relationships
        page_content_lookup = {}
        product_lookup = {}
        product_section_lookup = {}

        with transaction.atomic():
            # 1. Create PageContent instances
            self.stdout.write(self.style.MIGRATE_HEADING('Populating PageContent...'))
            for entry in data['page_contents']:
                fields = entry['fields']
                page_content, created = PageContent.objects.get_or_create(
                    page_name=fields['page_name'],
                    section_identifier=fields['section_identifier'],
                    defaults={
                        'title': fields.get('title'),
                        'subtitle': fields.get('subtitle'),
                        'body_text': fields.get('body_text'),
                        'background_image': fields.get('background_image'),
                        'background_image_alt_text': fields.get('background_image_alt_text'),
                        'order': fields.get('order', 0),
                    }
                )
                page_content_lookup[f"{fields['page_name']}_{fields['section_identifier']}"] = page_content
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created PageContent: {page_content}'))
                else:
                    self.stdout.write(self.style.WARNING(f'PageContent already exists: {page_content}'))

            # 2. Create Product instances
            self.stdout.write(self.style.MIGRATE_HEADING('Populating Products...'))
            # Filter only actual Product models, not related ProductImage/Section/Item
            product_entries = [p for p in data['products'] if p['model'] == 'cms_content.Product']
            for entry in product_entries:
                fields = entry['fields']
                product, created = Product.objects.update_or_create(
                    url_slug=slugify(fields['name']),
                    defaults={
                        'name': fields['name'],
                        'short_description': fields.get('short_description', ''),
                        'hero_image': fields.get('hero_image', ''),
                        'hero_image_alt_text': fields.get('hero_image_alt_text', ''),
                        'main_description': fields.get('main_description', ''),
                        'conclusion_text': fields.get('conclusion_text', ''),
                        'order': fields.get('order', 0),
                    }
                )
                product_lookup[fields['url_slug']] = product
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created Product: {product}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Product already exists: {product}'))

            # 3. Create Service instances
            self.stdout.write(self.style.MIGRATE_HEADING('Populating Services...'))
            for entry in data['services']:
                fields = entry['fields']
                service, created = Service.objects.get_or_create(
                    url_slug=slugify(fields['name']),
                    defaults={
                        'name': fields['name'],
                        'short_description': fields.get('short_description', ''),
                        'image': fields.get('image', ''),
                        'image_alt_text': fields.get('image_alt_text', ''),
                        'order': fields.get('order', 0),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created Service: {service}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Service already exists: {service}'))

            # 4. Create Feature instances
            self.stdout.write(self.style.MIGRATE_HEADING('Populating Features...'))
            for entry in data['features']:
                fields = entry['fields']
                feature, created = Feature.objects.get_or_create(
                    title=fields['title'],
                    defaults={
                        'description': fields.get('description', ''),
                        'icon_class': fields.get('icon_class', ''),
                        'order': fields.get('order', 0),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created Feature: {feature}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Feature already exists: {feature}'))

            # 5. Create TimelineEvent instances
            self.stdout.write(self.style.MIGRATE_HEADING('Populating TimelineEvents...'))
            for entry in data['timeline_events']:
                fields = entry['fields']
                timeline_event, created = TimelineEvent.objects.get_or_create(
                    year=fields['year'],
                    description=fields['description'], # Assuming description + year makes it unique enough for get_or_create
                    defaults={
                        'order': fields.get('order', 0),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created TimelineEvent: {timeline_event}'))
                else:
                    self.stdout.write(self.style.WARNING(f'TimelineEvent already exists: {timeline_event}'))

            # 6. Create Capability instances
            self.stdout.write(self.style.MIGRATE_HEADING('Populating Capabilities...'))
            for entry in data['capabilities']:
                fields = entry['fields']
                capability, created = Capability.objects.get_or_create(
                    title=fields['title'],
                    defaults={
                        'description': fields.get('description', ''),
                        'image': fields.get('image', ''),
                        'image_alt_text': fields.get('image_alt_text', ''),
                        'order': fields.get('order', 0),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created Capability: {capability}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Capability already exists: {capability}'))

            # 7. Create CallToAction instances (requires PageContent to exist)
            self.stdout.write(self.style.MIGRATE_HEADING('Populating CallToActions...'))
            for entry in data['call_to_actions']:
                fields = entry['fields']
                page_content_key = fields['page_content'] # This is the section_identifier
                # Correctly reference the PageContent instance using its page_name and section_identifier
                page_content_instance = page_content_lookup.get(page_content_key)

                if page_content_instance:
                    call_to_action, created = CallToAction.objects.get_or_create(
                        page_content=page_content_instance,
                        button_text=fields['button_text'],
                        defaults={
                            'button_url': fields.get('button_url', ''),
                            'order': fields.get('order', 0),
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created CallToAction: {call_to_action}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'CallToAction already exists: {call_to_action}'))
                else:
                    self.stdout.write(self.style.ERROR(f'PageContent not found for CallToAction: {page_content_key}'))

            # 8. Create ProductSection instances (requires Product to exist)
            self.stdout.write(self.style.MIGRATE_HEADING('Populating ProductSections...'))
            product_section_entries = [p for p in data['products'] if p['model'] == 'cms_content.ProductSection']
            for entry in product_section_entries:
                fields = entry['fields']
                product_slug = fields['product']
                product_instance = product_lookup.get(product_slug)

                if product_instance:
                    product_section, created = ProductSection.objects.get_or_create(
                        product=product_instance,
                        title=fields['title'],
                        defaults={
                            'order': fields.get('order', 0),
                        }
                    )
                    product_section_lookup[f"{product_slug}_{fields['title']}"] = product_section
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created ProductSection: {product_section}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'ProductSection already exists: {product_section}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Product not found for ProductSection: {product_slug}'))

            # 9. Create ProductImage instances (requires Product to exist)
            self.stdout.write(self.style.MIGRATE_HEADING('Populating ProductImages...'))
            product_image_entries = [p for p in data['products'] if p['model'] == 'cms_content.ProductImage']
            for entry in product_image_entries:
                fields = entry['fields']
                product_slug = fields['product']
                product_instance = product_lookup.get(product_slug)

                if product_instance:
                    product_image, created = ProductImage.objects.get_or_create(
                        product=product_instance,
                        image=fields['image'], # Assuming image path is unique enough
                        defaults={
                            'alt_text': fields.get('alt_text', ''),
                            'order': fields.get('order', 0),
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created ProductImage: {product_image}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'ProductImage already exists: {product_image}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Product not found for ProductImage: {product_slug}'))

            # 10. Create ProductSectionItem instances (requires ProductSection to exist)
            self.stdout.write(self.style.MIGRATE_HEADING('Populating ProductSectionItems...'))
            product_section_item_entries = [p for p in data['products'] if p['model'] == 'cms_content.ProductSectionItem']
            for entry in product_section_item_entries:
                fields = entry['fields']
                section_title = fields['section']
                product_slug_for_section = fields['product'] if 'product' in fields else None # Need to get product slug for section lookup

                # Find the associated ProductSection instance
                # This is tricky because ProductSectionItem only has section title, not product slug in the JSON
                # We need to infer the product slug from the context of the extraction
                # For now, assuming section title is unique enough or will be resolved by a more complex lookup
                # A better approach would be to include product_slug in ProductSectionItem JSON
                section_instance = None
                if product_slug_for_section:
                    section_instance = product_section_lookup.get(f"{product_slug_for_section}_{section_title}")
                else:
                    # Fallback: try to find section by title only (less robust)
                    section_instance = ProductSection.objects.filter(title=section_title).first()

                if section_instance:
                    product_section_item, created = ProductSectionItem.objects.get_or_create(
                        section=section_instance,
                        text=fields['text'], # Assuming text + section makes it unique enough
                        defaults={
                            'order': fields.get('order', 0),
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created ProductSectionItem: {product_section_item}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'ProductSectionItem already exists: {product_section_item}'))
                else:
                    self.stdout.write(self.style.ERROR(f'ProductSection not found for ProductSectionItem: {section_title}'))

        self.stdout.write(self.style.SUCCESS('CMS data population complete.'))
