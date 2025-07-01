# CMS Content Population Guide

This document provides instructions on how to populate the CMS models with content using the Django administration interface. This process is crucial after setting up the models and before integrating them into the frontend templates.

## General Steps for Populating Content

1.  **Access Django Admin**: Open your web browser and navigate to the Django admin interface, typically at `http://127.0.0.1:8000/admin/` (or your deployed domain followed by `/admin/`).

2.  **Log In**: Use your superuser credentials to log in.

3.  **Navigate to Models**: On the admin homepage, you will see a list of your installed applications and their registered models. Click on the model you wish to populate (e.g., `PageContent`, `Products`, `Services`).

4.  **Add New Instance**: Click the "Add [Model Name]" button (e.g., "Add Page content", "Add Product") to create a new entry.

5.  **Fill in Fields**: Fill in the fields according to the content you want to make dynamic. Refer to your existing HTML files (`templates/pages/*.html`) to extract the text, image paths, and other data.

    *   **Text Fields**: Copy and paste text directly.
    *   **Image Fields**: Upload the corresponding image files. Ensure you have the images available locally.
    *   **URL Fields**: Enter the full URL or relative path as needed.
    *   **Slug Fields**: If `prepopulated_fields` is configured in `admin.py`, the slug will auto-fill as you type the name/title. Otherwise, enter a URL-friendly slug manually (lowercase, hyphens instead of spaces).
    *   **Order Fields**: Use the `order` field to control the display sequence of items within a section or list.

6.  **Save**: Click "Save" to create the new content instance. If there are related models (e.g., `ProductImage` for `Product`, `ProductSection` for `Product`), you will typically manage them as inlines directly on the parent model's add/change form.

7.  **Repeat**: Repeat the process for all necessary content elements.

## Specific Content Population Examples

### Populating `PageContent` (e.g., About Page Hero)

1.  Go to `Page contents` in the admin.
2.  Click "Add Page content".
3.  **`page_name`**: `about`
4.  **`section_identifier`**: `about_hero`
5.  **`title`**: `About Leafloat Robotics`
6.  **`subtitle`**: `At Leafloat Robotics, we are pioneers in AI-driven solutions...` (copy the full lead paragraph).
7.  **`background_image`**: Upload `images/about/banner.png`.
8.  **`background_image_alt_text`**: `Leafloat Robotics Banner`.
9.  **`order`**: `0` (or leave default).
10. Save.

### Populating `Product` (e.g., Robodogs)

1.  Go to `Products` in the admin.
2.  Click "Add Product".
3.  **`name`**: `Robodogs`
4.  **`short_description`**: `Agile Autonomous Inspection Units`
5.  **`hero_image`**: Upload `images/products/robodog.png`.
6.  **`hero_image_alt_text`**: `Robodog`
7.  **`main_description`**: Copy the introductory paragraph from `product1.html`.
8.  **`url_slug`**: `robodogs` (will likely auto-fill).
9.  **`order`**: `0`.
10. **Related `ProductImage`s (Carousel)**: In the "Images" inline section, add new images for the carousel (e.g., `images/products/1.png`, `images/products/2.png`), providing alt text and order for each.
11. **Related `ProductSection`s**: In the "Sections" inline section, add new sections:
    *   **Section 1**: `title`: `Key Features`, `order`: `0`.
        *   **Related `ProductSectionItem`s**: Add each `<li>` item from the "Key Features" list in `product1.html` as a new item, copying the full text (including `<strong>` tags if applicable) into the `text` field, and setting the `order`.
    *   **Section 2**: `title`: `Applications`, `order`: `1`.
        *   **Related `ProductSectionItem`s**: Add items similarly.
    *   Continue for "Competitive Advantages" and "Future Developments".
12. Save.

### Populating `Service` (e.g., Non-GPS Navigation)

1.  Go to `Services` in the admin.
2.  Click "Add Service".
3.  **`name`**: `Non-GPS Navigation`
4.  **`short_description`**: `Enables drones and ground vehicles to operate in GPS-denied environments...`
5.  **`image`**: Upload `images/products/product4.png`.
6.  **`image_alt_text`**: `Non-GPS Navigation`.
7.  **`url_slug`**: `non-gps-navigation`.
8.  **`order`**: `0`.
9.  Save.

### Populating `Feature` (e.g., Expertise in Autonomy)

1.  Go to `Features` in the admin.
2.  Click "Add Feature".
3.  **`title`**: `Expertise in Autonomy`
4.  **`description`**: `Leading the way in self-governing robotic systems.`
5.  **`icon_class`**: `fa fa-cogs`
6.  **`order`**: `0`.
7.  Save.

### Populating `TimelineEvent` (e.g., 2020)

1.  Go to `Timeline events` in the admin.
2.  Click "Add Timeline event".
3.  **`year`**: `2020`
4.  **`description`**: `Founded in Malaysia`
5.  **`order`**: `0`.
6.  Save.

### Populating `CallToAction` (e.g., Contact Us)

1.  Go to the `PageContent` instance for the "About Page CTA" section.
2.  In the "Call to actions" inline section, click "Add Call to action".
3.  **`button_text`**: `Contact Us`
4.  **`button_url`**: `/contact/`
5.  **`order`**: `0`.
6.  Save the `PageContent` instance.

## Important Notes

*   **Image Paths**: When extracting image paths from HTML, remember they are relative to the `static/` directory. You will upload the actual image files to the Django admin, and Django will handle their storage and serving.
*   **Rich Text**: If you integrate a rich text editor (Phase 3), you will use its interface to format text (e.g., bolding, lists) for fields like `ProductSectionItem.text`.
*   **Consistency**: Ensure consistency in `page_name` and `section_identifier` values to correctly map content to templates.

By following these steps, you can systematically transfer your static website content into the dynamic CMS, making it fully manageable through the Django admin interface.
