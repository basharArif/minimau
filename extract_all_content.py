
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

all_extracted_data = {
    "products": [],
    "page_contents": [],
    "call_to_actions": [],
    "capabilities": [],
    "services": [],
    "features": [],
    "timeline_events": []
}

# Helper function to clean and escape text for JSON
def clean_text_for_json(text):
    if text is None:
        return ""
    # Remove all non-printable ASCII characters except for common whitespace (tab, newline, carriage return)
    # This is to prevent issues with json.dumps if it encounters truly invalid control characters
    cleaned_text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return cleaned_text

# --- Extract Product data from index.html (re-using previous logic) ---
html_file_path_index = Path("/home/arif/leafloat/templates/pages/index.html")
html_content_index = html_file_path_index.read_text()
soup_index = BeautifulSoup(html_content_index, 'html.parser')
portfolio_slider = soup_index.find('div', class_='portfolio-slider-5')

if portfolio_slider:
    product_blocks_index = portfolio_slider.find_all('div', class_='col pl-5 pr-5')
    order = 0
    for block in product_blocks_index:
        name_tag = block.find('h4', class_='title').find('a')
        short_description_tag = block.find('span', class_='category').find('a')
        image_style = block.find('a', class_='portfolio-image').get('style')
        href_tag = block.find('a', class_='portfolio-image').get('href')

        name = clean_text_for_json(name_tag.get_text(strip=True)) if name_tag else ""
        short_description = clean_text_for_json(short_description_tag.get_text(strip=True)) if short_description_tag else ""

        hero_image = ""
        if image_style:
            match = re.search(r"url\({% static '([^']+)' %}\)", image_style)
            if match:
                hero_image = clean_text_for_json(match.group(1))

        url_slug = ""
        if href_tag:
            url_slug = clean_text_for_json(name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace(':', '')) # Added .replace(':', '')

        if name and short_description and hero_image and url_slug:
            all_extracted_data["products"].append({
                "model": "cms_content.Product",
                "fields": {
                    "name": name,
                    "short_description": short_description,
                    "hero_image": hero_image,
                    "hero_image_alt_text": name, # Using name as alt text for now
                    "main_description": "", # Placeholder
                    "conclusion_text": "", # Placeholder
                    "url_slug": url_slug,
                    "order": order
                }
            })
            order += 1

# --- Extract Product Details from productX.html files ---
# Create a temporary dictionary to hold product entries for easy lookup
# This will be used to update existing product entries or create new ones
products_lookup = {p["fields"]["name"].lower().strip(): p for p in all_extracted_data["products"] if p["model"] == "cms_content.Product"}

for i in range(1, 8):
    product_html_file_path = Path(f"/home/arif/leafloat/templates/pages/product{i}.html")
    if not product_html_file_path.exists():
        continue

    html_content_product = product_html_file_path.read_text()
    soup_product = BeautifulSoup(html_content_product, 'html.parser')

    product_name_tag = soup_product.find('div', class_='product-hero-title').find('h1')
    product_name_from_html = clean_text_for_json(product_name_tag.get_text(strip=True)) if product_name_tag else f"Product {i}"
    normalized_product_name_from_html = product_name_from_html.lower().strip()

    current_product_entry = products_lookup.get(normalized_product_name_from_html)

    if not current_product_entry:
        # If product not found from index.html, create a new one
        url_slug = clean_text_for_json(product_name_from_html.lower().replace(' ', '-').replace('(', '').replace(')', '').replace(':', '')) # Added .replace(':', '')
        current_product_entry = {
            "model": "cms_content.Product",
            "fields": {
                "name": product_name_from_html,
                "short_description": "",
                "hero_image": "", # Will try to find from product page
                "hero_image_alt_text": product_name_from_html,
                "main_description": "",
                "conclusion_text": "",
                "url_slug": url_slug,
                "order": len(all_extracted_data["products"]) # Add to end
            }
        }
        all_extracted_data["products"].append(current_product_entry)
        products_lookup[normalized_product_name_from_html] = current_product_entry # Add to lookup

    content_column = soup_product.find('div', class_='col-lg-5 col-12')
    if content_column:
        paragraphs = content_column.find_all('p')
        if paragraphs:
            current_product_entry["fields"]["main_description"] = clean_text_for_json(paragraphs[0].get_text(strip=True))
            if len(paragraphs) > 1:
                current_product_entry["fields"]["conclusion_text"] = clean_text_for_json(paragraphs[-1].get_text(strip=True))

    # Extract Product Images (carousel)
    carousel_inner = soup_product.find('div', class_='carousel-inner')
    if carousel_inner:
        img_order = 0
        for img_tag in carousel_inner.find_all('img'):
            img_src = img_tag.get('src')
            img_alt = img_tag.get('alt', '')
            # Use re.sub to remove {% static '...' %} and then replace /static/
            clean_src = clean_text_for_json(re.sub(r"{% static '([^']+)' %}", r"\1", img_src).replace('/static/', ''))

            # Only add if it's not the hero image (which is already in Product model)
            # This check is a bit simplistic, might need refinement if hero_image is not always the first
            if clean_src != current_product_entry["fields"]["hero_image"]:
                all_extracted_data["products"].append({
                    "model": "cms_content.ProductImage",
                    "fields": {
                        "product": current_product_entry["fields"]["url_slug"], # Link by slug
                        "image": clean_src,
                        "alt_text": clean_text_for_json(img_alt),
                        "order": img_order
                    }
                })
                img_order += 1
            elif not current_product_entry["fields"]["hero_image"]:
                # If hero_image was not set from index.html, set it from the first image here
                current_product_entry["fields"]["hero_image"] = clean_src
                current_product_entry["fields"]["hero_image_alt_text"] = clean_text_for_json(img_alt)

    # Extract Product Sections and Items
    product_sections_html = content_column.find_all('h3', class_='mt-4') if content_column else []
    section_order = 0
    for section_h3 in product_sections_html:
        section_title = clean_text_for_json(section_h3.get_text(strip=True))
        section_data = {
            "model": "cms_content.ProductSection",
            "fields": {
                "product": current_product_entry["fields"]["url_slug"], # Link by slug
                "title": section_title,
                "order": section_order
            }
        }
        all_extracted_data["products"].append(section_data)

        # Get the ul/p following the h3
        current_element = section_h3.next_sibling
        item_order = 0
        while current_element:
            if current_element.name == 'ul':
                for li_tag in current_element.find_all('li'):
                    item_text = clean_text_for_json(str(li_tag)) # Keep HTML formatting and escape newlines
                    all_extracted_data["products"].append({
                        "model": "cms_content.ProductSectionItem",
                        "fields": {
                            "product": current_product_entry["fields"]["url_slug"], # Add product slug
                            "section": section_title, # Link by title
                            "text": item_text,
                            "order": item_order
                        }
                    })
                    item_order += 1
                break # Stop after finding the ul
            elif current_element.name == 'p': # Handle paragraphs that might follow a section title
                item_text = clean_text_for_json(str(current_element)) # Keep HTML formatting and escape newlines
                all_extracted_data["products"].append({
                    "model": "cms_content.ProductSectionItem",
                    "fields": {
                        "product": current_product_entry["fields"]["url_slug"], # Add product slug
                        "section": section_title, # Link by title
                        "text": item_text,
                        "order": item_order
                    }
                })
                item_order += 1
                # If it's a paragraph, continue to next sibling to see if there are more
                current_element = current_element.next_sibling
            else:
                current_element = current_element.next_sibling

            # Stop if we hit another h3 or end of content_column
            if current_element and current_element.name == 'h3' and 'mt-4' in current_element.get('class', []):
                break

        section_order += 1


# --- Extract PageContent, CallToAction, Capability, Feature, TimelineEvent from about.html ---
html_file_path_about = Path("/home/arif/leafloat/templates/pages/about.html")
html_content_about = html_file_path_about.read_text()
soup_about = BeautifulSoup(html_content_about, 'html.parser')

# About Leafloat Robotics Hero
hero_section = soup_about.find('div', class_='section-wrap', style=re.compile(r'images/about/banner.png'))
if hero_section:
    title_tag = hero_section.find('h2', class_='block-title')
    subtitle_tag = hero_section.find('p', class_='lead')
    bg_image_match = re.search(r"url\({% static '([^']+)' %}\)", hero_section.get('style', ''))

    all_extracted_data["page_contents"].append({
        "model": "cms_content.PageContent",
        "fields": {
            "page_name": "about",
            "section_identifier": "hero_section",
            "title": clean_text_for_json(title_tag.get_text(strip=True)) if title_tag else "",
            "subtitle": clean_text_for_json(subtitle_tag.get_text(strip=True)) if subtitle_tag else "",
            "body_text": clean_text_for_json(""),
            "background_image": clean_text_for_json(bg_image_match.group(1)) if bg_image_match else "",
            "background_image_alt_text": "About Page Banner",
            "order": 0
        }
    })

# What We Do Cards (Capabilities)
what_we_do_section = soup_about.find('div', class_="section-wrap bg-light-grey") # Refined selector
if what_we_do_section:
    capability_cards = what_we_do_section.find_all('div', class_='card')
    cap_order = 0
    for card in capability_cards:
        cap_title_tag = card.find('h5')
        cap_desc_tag = card.find('p')
        cap_image_div = card.find('div', style=re.compile(r'background-image'))
        cap_image = ""
        if cap_image_div:
            img_match = re.search(r"url\({% static '([^']+)' %}\)", cap_image_div.get('style', ''))
            if img_match:
                cap_image = clean_text_for_json(img_match.group(1))

        all_extracted_data["capabilities"].append({
            "model": "cms_content.Capability",
            "fields": {
                "title": clean_text_for_json(cap_title_tag.get_text(strip=True)) if cap_title_tag else "",
                "description": clean_text_for_json(cap_desc_tag.get_text(strip=True)) if cap_desc_tag else "",
                "image": cap_image,
                "image_alt_text": clean_text_for_json(cap_title_tag.get_text(strip=True)) if cap_title_tag else "",
                "order": cap_order
            }
        })
        cap_order += 1

# Mission & Vision
mission_vision_section = soup_about.find('div', class_='section-wrap', style=re.compile(r'images/bg/service-bg.png'))
if mission_vision_section:
    mission_col = mission_vision_section.find('div', class_='col-lg-6')
    if mission_col:
        mission_title_tag = mission_col.find('h3')
        mission_body_tag = mission_col.find('p')
        all_extracted_data["page_contents"].append({
            "model": "cms_content.PageContent",
            "fields": {
                "page_name": "about",
                "section_identifier": "mission_section",
                "title": clean_text_for_json(mission_title_tag.get_text(strip=True)) if mission_title_tag else "",
                "body_text": clean_text_for_json(mission_body_tag.get_text(strip=True)) if mission_body_tag else "",
                "background_image": "images/bg/service-bg.png",
                "background_image_alt_text": "Mission Background",
                "order": 1
            }
        })

    vision_col = mission_vision_section.find_all('div', class_='col-lg-6')
    if len(vision_col) > 1:
        vision_title_tag = vision_col[1].find('h3')
        vision_body_tag = vision_col[1].find('p')
        all_extracted_data["page_contents"].append({
            "model": "cms_content.PageContent",
            "fields": {
                "page_name": "about",
                "section_identifier": "vision_section",
                "title": clean_text_for_json(vision_title_tag.get_text(strip=True)) if vision_title_tag else "",
                "body_text": clean_text_for_json(vision_body_tag.get_text(strip=True)) if vision_body_tag else "",
                "background_image": "images/bg/service-bg.png",
                "background_image_alt_text": "Vision Background",
                "order": 2
            }
        })

# Why Leafloat - Feature Blocks
why_leafloat_section = soup_about.find('div', class_='section-wrap bg-grey pt-80 pb-80')
if why_leafloat_section:
    feature_h3 = why_leafloat_section.find('h3', class_='block-title')
    all_extracted_data["page_contents"].append({
        "model": "cms_content.PageContent",
        "fields": {
            "page_name": "about",
            "section_identifier": "why_choose_section",
            "title": clean_text_for_json(feature_h3.get_text(strip=True)) if feature_h3 else "",
            "order": 3
        }
    })
    feature_boxes = why_leafloat_section.find_all('div', class_='feature-box')
    feat_order = 0
    for box in feature_boxes:
        icon_tag = box.find('i')
        feat_title_tag = box.find('h5')
        feat_desc_tag = box.find('p')
        all_extracted_data["features"].append({
            "model": "cms_content.Feature",
            "fields": {
                "title": clean_text_for_json(feat_title_tag.get_text(strip=True)) if feat_title_tag else "",
                "description": clean_text_for_json(feat_desc_tag.get_text(strip=True)) if feat_desc_tag else "",
                "icon_class": clean_text_for_json(' '.join(icon_tag.get('class', []))) if icon_tag else "",
                "order": feat_order
            }
        })
        feat_order += 1

# Journey Timeline
journey_section = soup_about.find('div', class_='section-wrap section pt-80 pb-80', style=False, recursive=False) # Target the third section-wrap
if journey_section:
    timeline_h3 = journey_section.find('h3', class_='block-title')
    all_extracted_data["page_contents"].append({
        "model": "cms_content.PageContent",
        "fields": {
            "page_name": "about",
            "section_identifier": "journey_section",
            "title": clean_text_for_json(timeline_h3.get_text(strip=True)) if timeline_h3 else "",
            "order": 4
        }
    })
    timeline_cols = journey_section.find_all('div', class_='col-md-3')
    time_order = 0
    for col in timeline_cols:
        year_tag = col.find('strong')
        desc_tag = col.find('p', class_='small')
        all_extracted_data["timeline_events"].append({
            "model": "cms_content.TimelineEvent",
            "fields": {
                "year": int(clean_text_for_json(year_tag.get_text(strip=True))) if year_tag else 0,
                "description": clean_text_for_json(desc_tag.get_text(strip=True)) if desc_tag else "",
                "order": time_order
            }
        })
        time_order += 1

# Call to Action
cta_section = soup_about.find('div', class_='section-wrap section bg-dark text-white pt-100 pb-100')
if cta_section:
    cta_title_tag = cta_section.find('h3', class_='block-title')
    cta_body_tag = cta_section.find('p', class_='text-white')
    all_extracted_data["page_contents"].append({
        "model": "cms_content.PageContent",
        "fields": {
            "page_name": "about",
            "section_identifier": "cta_section",
            "title": clean_text_for_json(cta_title_tag.get_text(strip=True)) if cta_title_tag else "",
            "body_text": clean_text_for_json(cta_body_tag.get_text(strip=True)) if cta_body_tag else "",
            "order": 5
        }
    })
    cta_buttons = cta_section.find_all('a', class_=re.compile(r'btn'))
    btn_order = 0
    for btn in cta_buttons:
        all_extracted_data["call_to_actions"].append({
            "model": "cms_content.CallToAction",
            "fields": {
                "page_content": "about_cta_section", # Link by section_identifier
                "button_text": clean_text_for_json(btn.get_text(strip=True)),
                "button_url": clean_text_for_json(btn.get('href', '')),
                "order": btn_order
            }
        })
        btn_order += 1

# --- Extract Service data from service.html ---
html_file_path_service = Path("/home/arif/leafloat/templates/pages/service.html")
html_content_service = html_file_path_service.read_text()
soup_service = BeautifulSoup(html_content_service, 'html.parser')

# Our Services Hero
service_hero_section = soup_service.find('div', class_='col-12 col-lg-8 text-center mb-80')
if service_hero_section:
    title_tag = service_hero_section.find('h2', class_='block-title')
    subtitle_tag = service_hero_section.find('p', class_='lead')
    all_extracted_data["page_contents"].append({
        "model": "cms_content.PageContent",
        "fields": {
            "page_name": "service",
            "section_identifier": "hero_section",
            "title": clean_text_for_json(title_tag.get_text(strip=True)) if title_tag else "",
            "subtitle": clean_text_for_json(subtitle_tag.get_text(strip=True)) if subtitle_tag else "",
            "order": 0
        }
    })

# Service Cards
service_cards_container = soup_service.find('div', class_='col-12').find('div', class_='row')
if service_cards_container:
    service_cards = service_cards_container.find_all('a', class_='service-card')
    svc_order = 0
    for card in service_cards:
        svc_name_tag = card.find('h4')
        svc_desc_tag = card.find('p', class_='text-muted')
        svc_image_tag = card.find('img')
        svc_href = card.get('href', '')

        svc_name = clean_text_for_json(svc_name_tag.get_text(strip=True)) if svc_name_tag else ""
        svc_desc = clean_text_for_json(svc_desc_tag.get_text(strip=True)) if svc_desc_tag else ""
        svc_image = clean_text_for_json(re.sub(r"{% static '([^']+)' %}", r"\1", svc_image_tag.get('src', '')).replace('/static/', '')) if svc_image_tag else ""
        svc_alt_text = clean_text_for_json(svc_image_tag.get('alt', '')) if svc_image_tag else ""
        svc_url_slug = clean_text_for_json(svc_href.strip('/').replace('service-', '')) # Extract slug from /service-slug/

        all_extracted_data["services"].append({
            "model": "cms_content.Service",
            "fields": {
                "name": svc_name,
                "short_description": svc_desc,
                "image": svc_image,
                "image_alt_text": svc_alt_text,
                "url_slug": svc_url_slug,
                "order": svc_order
            }
        })
        svc_order += 1


# Write the final extracted data to a JSON file
output_json_path = Path("/home/arif/leafloat/extracted_content.json")
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(all_extracted_data, f, indent=2, ensure_ascii=False)

print(f"Content extracted and saved to {output_json_path}")
