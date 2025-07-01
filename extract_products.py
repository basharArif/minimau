import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

html_file_path = Path("/home/arif/leafloat/templates/pages/index.html")
html_content = html_file_path.read_text()

products_data = []

soup = BeautifulSoup(html_content, 'html.parser')

# Find the main container for portfolio items
portfolio_slider = soup.find('div', class_='portfolio-slider-5')

if portfolio_slider:
    # Find all individual product blocks
    # Each product is within a div with class 'col pl-5 pr-5'
    product_blocks = portfolio_slider.find_all('div', class_='col pl-5 pr-5')

    order = 0
    for block in product_blocks:
        name_tag = block.find('h4', class_='title').find('a')
        short_description_tag = block.find('span', class_='category').find('a')
        image_style = block.find('a', class_='portfolio-image').get('style')
        href_tag = block.find('a', class_='portfolio-image').get('href')

        name = name_tag.get_text(strip=True) if name_tag else ""
        short_description = short_description_tag.get_text(strip=True) if short_description_tag else ""

        hero_image = ""
        if image_style:
            # Extract URL from style attribute: background-image: url({% static 'images/products/1.png' %});
            match = re.search(r"url\({% static '([^']+)' %}\)", image_style)
            if match:
                hero_image = match.group(1)

        url_slug = ""
        if href_tag:
            # Extract slug from href: /products/1/
            match = re.search(r"/products/(\d+)/", href_tag)
            if match:
                # Using the product name to generate a more meaningful slug
                url_slug = name.lower().replace(' ', '-').replace('(', '').replace(')', '')

        if name and short_description and hero_image and url_slug:
            products_data.append({
                "model": "cms_content.Product",
                "fields": {
                    "name": name,
                    "short_description": short_description,
                    "hero_image": hero_image,
                    "hero_image_alt_text": name, # Using name as alt text for now
                    "main_description": "", # To be populated from productX.html
                    "conclusion_text": "", # To be populated from productX.html
                    "url_slug": url_slug,
                    "order": order
                }
            })
            order += 1

print(json.dumps(products_data, indent=2))