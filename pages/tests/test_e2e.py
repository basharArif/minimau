import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from django.test import LiveServerTestCase
from django.urls import reverse

from django.core.management import call_command

class E2ETests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.selenium = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        cls.selenium.implicitly_wait(10) # seconds

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        # Create a dummy extracted_content.json file
        json_content = '''
    {
        "page_contents": [
            {
                "model": "cms_content.PageContent",
                "fields": {
                    "page_name": "about",
                    "section_identifier": "hero_section",
                    "title": "About Leafloat Robotics",
                    "order": 1
                }
            },
            {
                "model": "cms_content.PageContent",
                "fields": {
                    "page_name": "service",
                    "section_identifier": "hero_section",
                    "title": "Our Services",
                    "order": 1
                }
            }
        ],
        "products": [
            {
                "model": "cms_content.Product",
                "fields": {
                    "name": "Robodogs",
                    "short_description": "A short description.",
                    "hero_image": "test_hero.jpg",
                    "hero_image_alt_text": "Test Hero Image",
                    "main_description": "Main description of the test product.",
                    "conclusion_text": "Conclusion of the test product.",
                    "url_slug": "robodogs",
                    "order": 1
                }
            }
        ],
        "services": [],
        "features": [],
        "timeline_events": [],
        "capabilities": [],
        "call_to_actions": []
    }
    '''
        self.json_file_path = os.path.join(os.getcwd(), "extracted_content.json")
        with open(self.json_file_path, "w") as f:
            f.write(json_content)
        call_command('populate_cms_data')

    def tearDown(self):
        super().tearDown()
        os.remove(self.json_file_path)

    def test_homepage_title(self):
        self.selenium.get(self.live_server_url + reverse('pages:home'))
        self.assertIn('Leafloat Robotics', self.selenium.title)

    def test_about_page_content(self):
        self.selenium.get(self.live_server_url + reverse('pages:about'))
        self.assertIn('About Leafloat Robotics', self.selenium.find_element('css selector', 'h2').text)

    def test_service_page_content(self):
        self.selenium.get(self.live_server_url + reverse('pages:service'))
        self.assertIn('Our Services', self.selenium.find_element('css selector', 'h2').text)

    def test_product_detail_page_content(self):
        # Assuming 'robodogs' is a valid slug for a product
        self.selenium.get(self.live_server_url + reverse('pages:product_detail', kwargs={'url_slug': 'robodogs'}))
        self.assertIn('Robodogs'.upper(), self.selenium.find_element('css selector', 'h1.product-name').text)
