from django.db import models

class TimeStampBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated At")

    class Meta:
        abstract = True
        ordering = ['created_at']

class PageContent(TimeStampBaseModel):
    page_name = models.CharField(max_length=50, verbose_name="Page Name", help_text="e.g., home, about, service")
    section_identifier = models.CharField(max_length=100, verbose_name="Section Identifier", help_text="Unique ID for the section on the page, e.g., hero_section, mission_section")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Title", help_text="Main heading for the section")
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subtitle", help_text="Secondary heading or lead-in text")
    body_text = models.TextField(blank=True, null=True, verbose_name="Body Text", help_text="Main paragraph content for the section")
    background_image = models.ImageField(upload_to='page_backgrounds/', blank=True, null=True, verbose_name="Background Image", help_text="Background image for the section")
    background_image_alt_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="Background Image Alt Text", help_text="Alt text for the background image")
    order = models.IntegerField(default=0, verbose_name="Order", help_text="Display order of this content block within its section")

    class Meta(TimeStampBaseModel.Meta):
        unique_together = ('page_name', 'section_identifier')
        ordering = ['page_name', 'section_identifier', 'order']
        verbose_name = "Page Content"
        verbose_name_plural = "Page Contents"

    def __str__(self):
        return f"{self.page_name} - {self.section_identifier}"

class CallToAction(TimeStampBaseModel):
    page_content = models.ForeignKey(PageContent, on_delete=models.CASCADE, related_name='call_to_actions', verbose_name="Page Content Block")
    button_text = models.CharField(max_length=100, verbose_name="Button Text")
    button_url = models.URLField(verbose_name="Button URL", help_text="URL the button links to")
    order = models.IntegerField(default=0, verbose_name="Order", help_text="Display order of the button")

    class Meta(TimeStampBaseModel.Meta):
        ordering = ['page_content', 'order']
        verbose_name = "Call To Action Button"
        verbose_name_plural = "Call To Action Buttons"

    def __str__(self):
        return f"{self.button_text} ({self.page_content.page_name} - {self.page_content.section_identifier})"

class Product(TimeStampBaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="Product Name")
    short_description = models.TextField(verbose_name="Short Description", help_text="Brief tagline or category for the product, used on the homepage")
    hero_image = models.ImageField(upload_to='product_heroes/', verbose_name="Hero Image", help_text="Primary image for homepage slider and product detail carousel")
    hero_image_alt_text = models.CharField(max_length=255, verbose_name="Hero Image Alt Text")
    main_description = models.TextField(verbose_name="Main Description", help_text="Introductory paragraph on the product detail page")
    conclusion_text = models.TextField(blank=True, null=True, verbose_name="Conclusion Text", help_text="Concluding paragraph on the product detail page")
    url_slug = models.SlugField(unique=True, verbose_name="URL Slug", help_text="URL-friendly identifier for the product")
    order = models.IntegerField(default=0, verbose_name="Order", help_text="Display order of products on the homepage slider")

    class Meta(TimeStampBaseModel.Meta):
        ordering = ['order']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

class ProductImage(TimeStampBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Product")
    image = models.ImageField(upload_to='product_carousel/', verbose_name="Image")
    alt_text = models.CharField(max_length=255, verbose_name="Alt Text")
    order = models.IntegerField(default=0, verbose_name="Order", help_text="Display order in the product carousel")

    class Meta(TimeStampBaseModel.Meta):
        ordering = ['product', 'order']
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"{self.product.name} Image {self.order}"

class ProductSection(TimeStampBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sections', verbose_name="Product")
    title = models.CharField(max_length=255, verbose_name="Section Title", help_text="Heading for the section, e.g., Key Features, Applications")
    order = models.IntegerField(default=0, verbose_name="Order", help_text="Display order of sections on the product detail page")

    class Meta(TimeStampBaseModel.Meta):
        ordering = ['product', 'order']
        verbose_name = "Product Section"
        verbose_name_plural = "Product Sections"

    def __str__(self):
        return f"{self.product.name} - {self.title}"

class ProductSectionItem(TimeStampBaseModel):
    section = models.ForeignKey(ProductSection, on_delete=models.CASCADE, related_name='items', verbose_name="Product Section")
    text = models.TextField(verbose_name="Item Text", help_text="Content of the list item. HTML formatting may be used.")
    order = models.IntegerField(default=0, verbose_name="Order", help_text="Display order of items within the section")

    class Meta(TimeStampBaseModel.Meta):
        ordering = ['section', 'order']
        verbose_name = "Product Section Item"
        verbose_name_plural = "Product Section Items"

    def __str__(self):
        return f"{self.section.title} Item {self.order}"

class Service(TimeStampBaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="Service Name")
    short_description = models.TextField(verbose_name="Short Description", help_text="Brief description of the service")
    image = models.ImageField(upload_to='service_images/', verbose_name="Service Image")
    image_alt_text = models.CharField(max_length=255, verbose_name="Service Image Alt Text")
    url_slug = models.SlugField(unique=True, verbose_name="URL Slug", help_text="URL-friendly identifier for the service")
    order = models.IntegerField(default=0, verbose_name="Order", help_text="Display order of service cards")

    class Meta(TimeStampBaseModel.Meta):
        ordering = ['order']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name

class Feature(TimeStampBaseModel):
    title = models.CharField(max_length=255, verbose_name="Feature Title")
    description = models.TextField(verbose_name="Description", help_text="Brief description of the feature")
    icon_class = models.CharField(max_length=100, verbose_name="Icon Class", help_text="Font Awesome icon class, e.g., fa fa-cogs")
    order = models.IntegerField(default=0, verbose_name="Order", help_text="Display order of features")

    class Meta(TimeStampBaseModel.Meta):
        ordering = ['order']
        verbose_name = "Feature"
        verbose_name_plural = "Features"

    def __str__(self):
        return self.title

class TimelineEvent(TimeStampBaseModel):
    year = models.IntegerField(verbose_name="Year")
    description = models.TextField(verbose_name="Description", help_text="Brief description of the event")
    order = models.IntegerField(default=0, verbose_name="Order", help_text="Display order of timeline events")

    class Meta(TimeStampBaseModel.Meta):
        ordering = ['year', 'order']
        verbose_name = "Timeline Event"
        verbose_name_plural = "Timeline Events"

    def __str__(self):
        return f"{self.year} - {self.description[:50]}..."

class Capability(TimeStampBaseModel):
    title = models.CharField(max_length=255, verbose_name="Capability Title")
    description = models.TextField(verbose_name="Description", help_text="Brief description of the capability")
    image = models.ImageField(upload_to='capabilities/', verbose_name="Image")
    image_alt_text = models.CharField(max_length=255, verbose_name="Image Alt Text")
    order = models.IntegerField(default=0, verbose_name="Order", help_text="Display order of capabilities")

    class Meta(TimeStampBaseModel.Meta):
        ordering = ['order']
        verbose_name = "Capability"
        verbose_name_plural = "Capabilities"

    def __str__(self):
        return self.title


class CaseStudy(TimeStampBaseModel):
    title = models.CharField(max_length=255, verbose_name="Title")
    short_description = models.TextField(verbose_name="Short Description")
    image = models.ImageField(upload_to='case_studies/', verbose_name="Image")
    image_alt_text = models.CharField(max_length=255, verbose_name="Image Alt Text")
    url_slug = models.SlugField(unique=True, verbose_name="URL Slug")
    order = models.IntegerField(default=0, verbose_name="Order")

    class Meta(TimeStampBaseModel.Meta):
        ordering = ['order']
        verbose_name = "Case Study"
        verbose_name_plural = "Case Studies"

    def __str__(self):
        return self.title


class WhitePaper(TimeStampBaseModel):
    title = models.CharField(max_length=255, verbose_name="Title")
    short_description = models.TextField(verbose_name="Short Description")
    file = models.FileField(upload_to='white_papers/', verbose_name="File")
    url_slug = models.SlugField(unique=True, verbose_name="URL Slug")
    order = models.IntegerField(default=0, verbose_name="Order")

    class Meta(TimeStampBaseModel.Meta):
        ordering = ['order']
        verbose_name = "White Paper"
        verbose_name_plural = "White Papers"

    def __str__(self):
        return self.title


class Blog(TimeStampBaseModel):
    title = models.CharField(max_length=255, verbose_name="Title")
    author = models.CharField(max_length=100, verbose_name="Author")
    publish_date = models.DateField(verbose_name="Publish Date")
    image = models.ImageField(upload_to='blog_images/', verbose_name="Image")
    image_alt_text = models.CharField(max_length=255, verbose_name="Image Alt Text")
    content = models.TextField(verbose_name="Content")
    url_slug = models.SlugField(unique=True, verbose_name="URL Slug")
    order = models.IntegerField(default=0, verbose_name="Order")

    class Meta(TimeStampBaseModel.Meta):
        ordering = ['publish_date', 'order']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title
