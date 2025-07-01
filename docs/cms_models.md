# CMS Model Definitions

This document provides detailed definitions for the Django models required to implement the Content Management System (CMS). Each model is designed to capture specific content elements from the existing HTML templates, ensuring that all text, images, and links can be dynamically managed while preserving the current design and layout.

## Core Principles for Model Design:

*   **Granularity**: Break down content into the smallest logical units.
*   **Reusability**: Design models so content can be reused across different sections or pages where appropriate.
*   **Flexibility**: Allow for variations in content structure (e.g., optional fields).
*   **Admin Usability**: Ensure models are intuitive and easy to manage within the Django Admin.
*   **Design Mapping**: Every field directly corresponds to a specific piece of content or attribute in the existing HTML.

---

## Model Definitions

### 0. `TimeStampBaseModel` (Abstract)

This is an abstract base model that provides `created_at` and `updated_at` fields for automatic tracking of creation and modification times. All other CMS models will inherit from this model.

**Purpose**: To provide common timestamp fields for all content models, aiding in auditing and content management.

**Fields**:

*   `created_at` (DateTimeField, `auto_now_add=True`):
    *   **Purpose**: Automatically sets the creation timestamp when an object is first created.
    *   **Verbose Name**: "Created At"
*   `updated_at` (DateTimeField, `auto_now=True`):
    *   **Purpose**: Automatically updates the timestamp every time the object is saved.
    *   **Verbose Name**: "Last Updated At"

---


### 1. `PageContent` Model

**Inherits from**: `TimeStampBaseModel`

This model will store generic content blocks that are not part of a specific product, service, feature, or timeline event. It's designed for sections like hero banners, mission/vision statements, and general text blocks that appear on various pages.

**Purpose**: To manage static text, titles, subtitles, and background images for general page sections.

**Inherits from**: `TimeStampBaseModel`

**Mapping to HTML**:
*   `templates/pages/about.html`: "About Leafloat Robotics Hero", "Mission & Vision", "Call to Action" sections.
*   `templates/pages/service.html`: "Our Services" hero section.
*   Potentially other general text blocks on `index.html` or other pages if they are not covered by `Product` or `Service` models.

**Inherits from**: `TimeStampBaseModel`

**Fields**:

*   `page_name` (CharField, `max_length=50`, `verbose_name="Page Name"`, `help_text="e.g., home, about, service"`):
    *   **Purpose**: Identifies which page this content block belongs to.
    *   **Rationale**: Allows filtering content for a specific page.
    *   **Example Values**: "about", "service".
*   `section_identifier` (CharField, `max_length=100`, `verbose_name="Section Identifier"`, `help_text="Unique ID for the section on the page, e.g., hero_section, mission_section"`):
    *   **Purpose**: A unique identifier for a specific section within a page.
    *   **Rationale**: Allows targeting specific content blocks on a page.
    *   **Example Values**: "about_hero", "about_mission", "about_vision", "about_cta", "service_hero".
*   `title` (CharField, `max_length=255`, `blank=True`, `null=True`, `verbose_name="Title"`, `help_text="Main heading for the section"`):
    *   **Purpose**: Main heading for the section.
    *   **Mapping**: `<h2>` or `<h3>` tags (e.g., "About Leafloat Robotics", "Our Mission", "Our Services").
*   `subtitle` (CharField, `max_length=255`, `blank=True`, `null=True`, `verbose_name="Subtitle"`, `help_text="Secondary heading or lead-in text"`):
    *   **Purpose**: Secondary heading or lead-in text.
    *   **Mapping**: `<p class="lead">` (e.g., "At Leafloat Robotics, we are pioneers...").
*   `body_text` (TextField, `blank=True`, `null=True`, `verbose_name="Body Text"`, `help_text="Main paragraph content for the section"`):
    *   **Purpose**: Main paragraph content for the section.
    *   **Mapping**: `<p>` tags within a section (e.g., the paragraph under "Our Mission").
*   `background_image` (ImageField, `upload_to='page_backgrounds/'`, `blank=True`, `null=True`, `verbose_name="Background Image"`, `help_text="Background image for the section"`):
    *   **Purpose**: Background image for sections (e.g., hero banners).
    *   **Mapping**: `style="background-image: url(...)"` attributes.
    *   **Example**: `images/about/banner.png`, `images/bg/service-bg.png`.
*   `background_image_alt_text` (CharField, `max_length=255`, `blank=True`, `null=True`, `verbose_name="Background Image Alt Text"`, `help_text="Alt text for the background image"`):
    *   **Purpose**: Alt text for accessibility of background images.
*   `order` (IntegerField, `default=0`, `verbose_name="Order"`, `help_text="Display order of this content block within its section"`):
    *   **Purpose**: To define the display order of `PageContent` instances if multiple blocks are associated with the same `page_name` and `section_identifier` (e.g., multiple paragraphs).

### 2. `CallToAction` Model

This model will store individual call-to-action buttons or links associated with a `PageContent` block.

**Purpose**: To manage dynamic buttons and their links within a specific content section.

**Inherits from**: `TimeStampBaseModel`

**Mapping to HTML**:
*   `templates/pages/about.html`: "Ready to Collaborate?" section's buttons (`Contact Us`, `Request Demo`, `Join Our Team`).

**Fields**:

*   `page_content` (ForeignKey to `PageContent`, `on_delete=models.CASCADE`, `related_name='call_to_actions'`, `verbose_name="Page Content Block"`):
    *   **Purpose**: Links a CTA button to its parent `PageContent` block.
    *   **Rationale**: Allows managing CTAs directly from the `PageContent` admin.
*   `button_text` (CharField, `max_length=100`, `verbose_name="Button Text"`):
    *   **Purpose**: The visible text on the button.
    *   **Mapping**: `<a>` tag content (e.g., "Contact Us").
*   `button_url` (URLField, `verbose_name="Button URL"`, `help_text="URL the button links to"`):
    *   **Purpose**: The URL the button links to.
    *   **Mapping**: `href` attribute of `<a>` tag (e.g., `/contact/`).
*   `order` (IntegerField, `default=0`, `verbose_name="Order"`, `help_text="Display order of the button"`):
    *   **Purpose**: To define the display order of buttons within a CTA section.

### 3. `Product` Model

This is the main model for each product, holding its core information and linking to related content like images and sections.

**Purpose**: To manage the primary details of each product, displayed on the homepage and as the main header on its detail page.

**Inherits from**: `TimeStampBaseModel`

**Mapping to HTML**:
*   `templates/pages/index.html`: Each product block in the "Portfolio Slider".
*   `templates/pages/productX.html`: The main title (`<h1>`) and introductory paragraph.

**Fields**:

*   `name` (CharField, `max_length=255`, `unique=True`, `verbose_name="Product Name"`):
    *   **Purpose**: The product's main name.
    *   **Mapping**: `<h4><a href="...">` on `index.html`, `<h1>` on `productX.html`.
    *   **Example**: "Robodogs", "Unmanned Aerial Vehicles (UAVs)".
*   `short_description` (TextField, `verbose_name="Short Description"`, `help_text="Brief tagline or category for the product, used on the homepage"`):
    *   **Purpose**: A brief tagline or category for the product, used on the homepage.
    *   **Mapping**: `<span class="category"><a>` on `index.html` (e.g., "Agile Autonomous Inspection Units").
*   `hero_image` (ImageField, `upload_to='product_heroes/'`, `verbose_name="Hero Image"`, `help_text="Primary image for homepage slider and product detail carousel"`):
    *   **Purpose**: The primary image for the product, used on the homepage slider and as the first image in the carousel on the detail page.
    *   **Mapping**: `style="background-image: url(...)"` on `index.html`, `<img>` in `carousel-item active` on `productX.html`.
    *   **Example**: `images/products/1.png`, `images/products/robodog.png`.
*   `hero_image_alt_text` (CharField, `max_length=255`, `verbose_name="Hero Image Alt Text"`):
    *   **Purpose**: Alt text for the hero image.
*   `main_description` (TextField, `verbose_name="Main Description"`, `help_text="Introductory paragraph on the product detail page"`):
    *   **Purpose**: The main introductory paragraph on the product detail page.
    *   **Mapping**: The first `<p>` tag in the "Product Content Column" on `productX.html`.
*   `url_slug` (SlugField, `unique=True`, `verbose_name="URL Slug"`, `help_text="URL-friendly identifier for the product"`):
    *   **Purpose**: A URL-friendly identifier for the product (e.g., `robodogs`, `unmanned-aerial-vehicles`).
    *   **Rationale**: Used to generate clean URLs like `/products/robodogs/`.
*   `conclusion_text` (TextField, `blank=True`, `null=True`, `verbose_name="Conclusion Text"`, `help_text="Concluding paragraph on the product detail page"`):
    *   **Purpose**: The concluding paragraph on the product detail page.
*   `order` (IntegerField, `default=0`, `verbose_name="Order"`, `help_text="Display order of products on the homepage slider"`):
    *   **Purpose**: To define the display order of products on the homepage slider.

### 4. `ProductImage` Model

This model will store additional images for a product, specifically for the carousel on the product detail page.

**Purpose**: To manage multiple images for a product's detail page carousel.

**Inherits from**: `TimeStampBaseModel`

**Mapping to HTML**:
*   `templates/pages/productX.html`: `<img>` tags within `carousel-item` (excluding the `active` one, which is `hero_image`).

**Fields**:

*   `product` (ForeignKey to `Product`, `on_delete=models.CASCADE`, `related_name='images'`, `verbose_name="Product"`):
    *   **Purpose**: Links an image to its parent `Product`.
*   `image` (ImageField, `upload_to='product_carousel/'`, `verbose_name="Image"`):
    *   **Purpose**: The image file.
*   `alt_text` (CharField, `max_length=255`, `verbose_name="Alt Text"`):
    *   **Purpose**: Alt text for the image.
*   `order` (IntegerField, `default=0`, `verbose_name="Order"`, `help_text="Display order in the product carousel"`):
    *   **Purpose**: To define the display order of images within the product carousel.

### 5. `ProductSection` Model

This model represents a major section within a product's detail page (e.g., "Key Features", "Applications").

**Purpose**: To structure the content on a product's detail page into logical sections.

**Inherits from**: `TimeStampBaseModel`

**Mapping to HTML**:
*   `templates/pages/productX.html`: `<h3>` tags like "Key Features", "Applications", "Competitive Advantages", "Future Developments".

**Fields**:

*   `product` (ForeignKey to `Product`, `on_delete=models.CASCADE`, `related_name='sections'`, `verbose_name="Product"`):
    *   **Purpose**: Links a section to its parent `Product`.
*   `title` (CharField, `max_length=255`, `verbose_name="Section Title"`, `help_text="Heading for the section, e.g., Key Features, Applications"`):
    *   **Purpose**: The heading for the section.
    *   **Example**: "Key Features", "Applications".
*   `order` (IntegerField, `default=0`, `verbose_name="Order"`, `help_text="Display order of sections on the product detail page"`):
    *   **Purpose**: To define the display order of sections on the product detail page.

### 6. `ProductSectionItem` Model

This model represents an individual list item within a `ProductSection`.

**Purpose**: To store the detailed bullet points or paragraphs within a product section.

**Inherits from**: `TimeStampBaseModel`

**Mapping to HTML**:
*   `templates/pages/productX.html`: `<li>` tags within `<ul>` lists under each `<h3>` section.

**Fields**:

*   `section` (ForeignKey to `ProductSection`, `on_delete=models.CASCADE`, `related_name='items'`, `verbose_name="Product Section"`):
    *   **Purpose**: Links an item to its parent `ProductSection`.
*   `text` (TextField, `verbose_name="Item Text"`, `help_text="Content of the list item. HTML formatting may be used."`):
    *   **Purpose**: The content of the list item. This will likely contain HTML (e.g., `<strong>` tags) and will require a rich text editor in the admin.
    *   **Example**: "<strong>AI-Driven Autonomy & Navigation</strong>: Advanced SLAM, obstacle detection, and GPS/RTK-enabled localization for precise navigation."
*   `order` (IntegerField, `default=0`, `verbose_name="Order"`, `help_text="Display order of items within the section"`):
    *   **Purpose**: To define the display order of items within a section.

### 7. `Service` Model

This model manages the service cards displayed on the services page.

**Purpose**: To manage the details of each service offered.

**Inherits from**: `TimeStampBaseModel`

**Mapping to HTML**:
*   `templates/pages/service.html`: Each "Service Card" block.

**Fields**:

*   `name` (CharField, `max_length=255`, `unique=True`, `verbose_name="Service Name"`):
    *   **Purpose**: The name of the service.
    *   **Mapping**: `<h4>` tag (e.g., "Non-GPS Navigation").
*   `short_description` (TextField, `verbose_name="Short Description"`, `help_text="Brief description of the service"`):
    *   **Purpose**: A brief description of the service.
    *   **Mapping**: `<p class="text-muted">` tag.
*   `image` (ImageField, `upload_to='service_images/'`, `verbose_name="Service Image"`):
    *   **Purpose**: The image associated with the service card.
    *   **Mapping**: `<img>` tag (e.g., `images/products/product4.png`).
*   `image_alt_text` (CharField, `max_length=255`, `verbose_name="Service Image Alt Text"`):
    *   **Purpose**: Alt text for the service image.
*   `url_slug` (SlugField, `unique=True`, `verbose_name="URL Slug"`, `help_text="URL-friendly identifier for the service"`):
    *   **Purpose**: A URL-friendly identifier for the service.
    *   **Rationale**: Used to generate clean URLs like `/service/non-gps-navigation/`.
*   `order` (IntegerField, `default=0`, `verbose_name="Order"`, `help_text="Display order of service cards"`):
    *   **Purpose**: To define the display order of service cards on the services page.

### 8. `Feature` Model

This model manages the "Why Choose Leafloat Robotics" feature blocks on the About page.

**Purpose**: To manage the individual feature items.

**Inherits from**: `TimeStampBaseModel`

**Mapping to HTML**:
*   `templates/pages/about.html`: Each "feature-box" block.

**Fields**:

*   `title` (CharField, `max_length=255`, `verbose_name="Feature Title"`):
    *   **Purpose**: The title of the feature.
    *   **Mapping**: `<h5>` tag (e.g., "Expertise in Autonomy").
*   `description` (TextField, `verbose_name="Description"`, `help_text="Brief description of the feature"`):
    *   **Purpose**: A brief description of the feature.
    *   **Mapping**: `<p>` tag.
*   `icon_class` (CharField, `max_length=100`, `verbose_name="Icon Class"`, `help_text="Font Awesome icon class, e.g., fa fa-cogs"`):
    *   **Purpose**: The Font Awesome icon class.
    *   **Mapping**: `<i>` tag's `class` attribute (e.g., "fa fa-cogs").
*   `order` (IntegerField, `default=0`, `verbose_name="Order"`, `help_text="Display order of features"`):
    *   **Purpose**: To define the display order of features.

### 9. `TimelineEvent` Model

This model manages the "Our Journey" timeline events on the About page.

**Purpose**: To manage historical events in the company's journey.

**Inherits from**: `TimeStampBaseModel`

**Mapping to HTML**:
*   `templates/pages/about.html`: Each timeline event block.

**Fields**:

*   `year` (IntegerField, `verbose_name="Year"`):
    *   **Purpose**: The year of the event.
    *   **Mapping**: `<h6><strong>` tag (e.g., "2020").
*   `description` (TextField, `verbose_name="Description"`, `help_text="Brief description of the event"`):
    *   **Purpose**: A brief description of the event.
    *   **Mapping**: `<p class="small">` tag (e.g., "Founded in Malaysia").
*   `order` (IntegerField, `default=0`, `verbose_name="Order"`, `help_text="Display order of timeline events"`):
    *   **Purpose**: To define the display order of timeline events.

### 10. `Capability` Model

This model manages the "What We Do" cards on the About page.

**Purpose**: To manage the individual capability items.

**Inherits from**: `TimeStampBaseModel`

**Mapping to HTML**:
*   `templates/pages/about.html`: Each "What We Do" card block.

**Fields**:

*   `title` (CharField, `max_length=255`, `verbose_name="Capability Title"`):
    *   **Purpose**: The title of the capability.
    *   **Mapping**: `<h5>` tag (e.g., "Autonomous Robotics").
*   `description` (TextField, `verbose_name="Description"`, `help_text="Brief description of the capability"`):
    *   **Purpose**: A brief description of the capability.
    *   **Mapping**: `<p>` tag.
*   `image` (ImageField, `upload_to='capabilities/'`, `verbose_name="Image"`):
    *   **Purpose**: The image associated with the capability card.
    *   **Mapping**: `div` with `background-image` style.
*   `image_alt_text` (CharField, `max_length=255`, `verbose_name="Image Alt Text"`):
    *   **Purpose**: Alt text for the capability image.
*   `order` (IntegerField, `default=0`, `verbose_name="Order"`, `help_text="Display order of capabilities"`):
    *   **Purpose**: To define the display order of capabilities.

---

## Relationships Summary

*   `PageContent` can have multiple `CallToAction` instances.
*   `Product` can have multiple `ProductImage` instances.
*   `Product` can have multiple `ProductSection` instances.
*   `ProductSection` can have multiple `ProductSectionItem` instances.

---

This detailed model definition should provide a solid foundation for implementing the CMS, ensuring all existing content can be dynamically managed.
