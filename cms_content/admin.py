from django.contrib import admin
from .models import (
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

class CallToActionInline(admin.TabularInline):
    model = CallToAction
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

class PageContentAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'section_identifier', 'title', 'order', 'created_at', 'updated_at')
    list_filter = ('page_name', 'section_identifier')
    search_fields = ('page_name', 'section_identifier', 'title', 'body_text')
    inlines = [CallToActionInline]
    readonly_fields = ('created_at', 'updated_at')

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

class ProductSectionItemInline(admin.TabularInline):
    model = ProductSectionItem
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

class ProductSectionInline(admin.StackedInline):
    model = ProductSection
    extra = 1
    inlines = [ProductSectionItemInline]
    readonly_fields = ('created_at', 'updated_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_slug', 'order', 'created_at', 'updated_at')
    search_fields = ('name', 'short_description', 'main_description', 'conclusion_text')
    prepopulated_fields = {'url_slug': ('name',)}
    inlines = [ProductImageInline, ProductSectionInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'short_description', 'url_slug', 'order', 'main_description', 'conclusion_text')
        }),
        ('Hero Image', {
            'fields': ('hero_image', 'hero_image_alt_text')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_slug', 'order', 'created_at', 'updated_at')
    search_fields = ('name', 'short_description')
    prepopulated_fields = {'url_slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class', 'order', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('year', 'description', 'order', 'created_at', 'updated_at')
    search_fields = ('year', 'description')
    readonly_fields = ('created_at', 'updated_at')

class CapabilityAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

# Register models with their custom Admin classes
admin.site.register(PageContent, PageContentAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(TimelineEvent, TimelineEventAdmin)
admin.site.register(Capability, CapabilityAdmin)

# Register models that are only used as inlines or don't need extensive customization
# but still need created_at/updated_at in their own admin view if accessed directly
class CallToActionAdmin(admin.ModelAdmin):
    list_display = ('button_text', 'button_url', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
admin.site.register(CallToAction, CallToActionAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
admin.site.register(ProductImage, ProductImageAdmin)

class ProductSectionAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
admin.site.register(ProductSection, ProductSectionAdmin)

class ProductSectionItemAdmin(admin.ModelAdmin):
    list_display = ('section', 'order', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
admin.site.register(ProductSectionItem, ProductSectionItemAdmin)