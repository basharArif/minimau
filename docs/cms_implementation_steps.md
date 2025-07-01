# CMS Implementation Steps

This document outlines the step-by-step process for implementing the Content Management System (CMS) based on the model definitions in `cms_models.md`. The implementation will proceed in phases, ensuring a structured and manageable approach.

## Phase 1: Foundational Content Models & Admin Integration

**Objective**: Create the Django models and make them manageable via the Django Admin.

**Steps**:

1.  **Create `cms_content` Django App**:
    *   Run `python manage.py startapp cms_content`.
    *   Add `'cms_content'` to `INSTALLED_APPS` in `sitecore/settings/base.py`.

2.  **Define Models in `cms_content/models.py`**:
    *   Translate the model definitions from `cms_models.md` into Django model classes in `cms_content/models.py`.
    *   Ensure all models inherit from `TimeStampBaseModel`.
    *   Implement all field types, `max_length`, `blank`, `null`, `default`, `unique`, `upload_to` attributes, `verbose_name`, `help_text`, and `ForeignKey` relationships (including `on_delete` and `related_name`) as defined.
    *   For `ImageField`, ensure `Pillow` is installed (`pip install Pillow`).

3.  **Create Initial Migrations**:
    *   Run `python manage.py makemigrations cms_content`.
    *   Run `python manage.py migrate` to apply the new database schema.

4.  **Register Models in `cms_content/admin.py`**:
    *   Import all defined models.
    *   Register each model using `admin.site.register(YourModel)`.
    *   Implement `ModelAdmin` classes for each model to customize the admin interface:
        *   `list_display`: Fields to show in the list view.
        *   `list_filter`: Fields to filter by.
        *   `search_fields`: Fields to search by.
        *   `prepopulated_fields`: For `SlugField` (e.g., `{'url_slug': ('name',)}`).
    *   Implement `StackedInline` or `TabularInline` for related models:
        *   `CallToActionInline` for `PageContent`.
        *   `ProductImageInline` and `ProductSectionInline` for `Product`.
        *   `ProductSectionItemInline` for `ProductSection`.

5.  **Populate Initial Content (Manual via Admin)**:
    *   Access the Django Admin (`/admin/`).
    *   Manually create instances for `PageContent`, `Product`, `Service`, `Feature`, `TimelineEvent`, and `Capability` based on the existing static content in your HTML files.
    *   Upload images as required.
    *   This step is crucial for testing the model structure and admin interface.

## Phase 2: Dynamic Template Integration

**Objective**: Modify existing Django templates to fetch and display content dynamically from the new CMS models.

**Steps**:

1.  **Update `pages/views.py`**:
    *   Modify existing views (e.g., `StaticTemplateView` for general pages) or create new ones (e.g., `ProductDetailView`, `ServiceDetailView`).
    *   Query the new CMS models to retrieve the relevant content based on the URL or other parameters.
    *   Pass the retrieved model instances to the template context.
    *   For product detail pages, create a `ProductDetailView` that takes the `url_slug` as a parameter and fetches the corresponding `Product` object along with its related `images` and `sections`.

2.  **Refactor `pages/urls.py`**:
    *   Update URL patterns to point to the new views.
    *   Add new URL patterns for product and service detail pages using `path('products/<slug:url_slug>/', ProductDetailView.as_view(), name='product_detail')`.
    *   Remove the loop that generates product URLs if they are now handled by a single dynamic URL.

3.  **Modify Templates in `templates/pages/`**:
    *   **`index.html`**: Replace hardcoded product data with a loop iterating over `Product` objects from the context.
    *   **`about.html`**: Replace hardcoded content in hero, mission/vision, features, timeline, and CTA sections with data from `PageContent`, `Feature`, `TimelineEvent`, and `CallToAction` objects.
    *   **`service.html`**: Replace hardcoded service cards with a loop iterating over `Service` objects.
    *   **Create `product_detail.html`**: This new template will replace all `productX.html` files. It will dynamically render the product name, main description, image carousel (iterating `ProductImage`s), and all sections (iterating `ProductSection`s and their `ProductSectionItem`s).
    *   Replace all `{% static 'images/...' %}` tags for dynamic content with `{{ object.image.url }}` or similar.
    *   Use Django template tags (`{% for %}`, `{% if %}`, `{{ object.field }}`) to display content.

4.  **Test Thoroughly**:
    *   Verify that all pages render correctly with dynamic content.
    *   Check all links and images.
    *   Ensure content updates in the admin are reflected on the frontend.

## Phase 3: Advanced Content Management Features

**Objective**: Enhance the content editing experience and improve website functionality.

**Steps**:

1.  **Integrate Rich Text Editor**:
    *   Choose a Django-compatible rich text editor (e.g., `django-ckeditor`, `django-tinymce`).
    *   Install the chosen package and configure it in `settings.py`.
    *   Change `TextField` to the rich text field type (e.g., `RichTextField`) in `cms_content/models.py` for fields like `PageContent.body_text`, `Product.main_description`, `ProductSectionItem.text`, `Service.short_description`, `Feature.description`, `TimelineEvent.description`.
    *   Run `makemigrations` and `migrate`.

2.  **Implement SEO Fields**:
    *   Add `seo_title` (CharField), `meta_description` (TextField), and `meta_keywords` (CharField) to relevant models (`PageContent`, `Product`, `Service`).
    *   Update `admin.py` to include these fields.
    *   Modify `base.html` to dynamically populate `<title>`, `<meta name="description">`, and `<meta name="keywords">` tags based on the current page's content.

3.  **Image Optimization/Management (Optional but Recommended)**:
    *   Consider `django-imagekit` for automatic image resizing and caching.
    *   Implement image processing in views or templates as needed.

4.  **Automate Slug Generation**:
    *   Ensure `prepopulated_fields` is correctly set in `admin.py` for `url_slug` fields.
    *   For more complex slug generation (e.g., ensuring uniqueness across different models), consider overriding the `save()` method in your models.

## Phase 4: Specialized Content (e.g., Blog/News)

**Objective**: Introduce more complex content types with their own specific structures and display logic.

**Steps**:

1.  **Define Blog Models**:
    *   Create `BlogPost`, `Category`, and `Tag` models in `cms_content/models.py` (or a new `blog` app).
    *   Include fields like `title`, `slug`, `author` (ForeignKey to `User`), `publish_date`, `content` (RichTextField), `featured_image`, `category` (ForeignKey), `tags` (ManyToManyField).

2.  **Create Blog Migrations**:
    *   Run `python manage.py makemigrations` and `migrate`.

3.  **Register Blog Models in Admin**:
    *   Make `BlogPost`, `Category`, `Tag` manageable in the Django Admin.

4.  **Develop Blog Views and Templates**:
    *   Create `BlogListView` to display a list of blog posts.
    *   Create `BlogPostDetailView` for individual blog posts.
    *   Design `blog_list.html` and `blog_detail.html` templates.

## Testing and Verification

*   **Unit Tests**: Write tests for all new models and views.
*   **Functional Tests**: Use Django's `TestCase` to simulate user interactions and verify dynamic content rendering.
*   **Manual Testing**: Thoroughly browse the website after each phase to ensure all content is displayed correctly and the design remains intact.

## Deployment Considerations

*   Ensure `MEDIA_ROOT` and `MEDIA_URL` are correctly configured for serving uploaded images in production.
*   Configure your web server (e.g., Nginx, Apache) to serve static and media files efficiently.

This detailed plan provides a clear roadmap for implementing the CMS. Each step builds upon the previous one, allowing for systematic development and testing.
