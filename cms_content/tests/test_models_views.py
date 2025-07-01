from django.test import TestCase, Client
from django.urls import reverse
from cms_content.models import CaseStudy, WhitePaper, Blog
from datetime import date

class CMSContentTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.case_study = CaseStudy.objects.create(
            title='Test Case Study',
            short_description='Short description for test case study.',
            image='case_studies/test_case_study.jpg',
            image_alt_text='Test Case Study Image',
            url_slug='test-case-study',
            order=1
        )
        self.white_paper = WhitePaper.objects.create(
            title='Test White Paper',
            short_description='Short description for test white paper.',
            file='white_papers/test_white_paper.pdf',
            url_slug='test-white-paper',
            order=1
        )
        self.blog_post = Blog.objects.create(
            title='Test Blog Post',
            author='Test Author',
            publish_date=date(2025, 7, 1),
            image='blog_images/test_blog_post.jpg',
            image_alt_text='Test Blog Post Image',
            content='<p>This is the content of the test blog post.</p>',
            url_slug='test-blog-post',
            order=1
        )

    def test_case_study_model(self):
        self.assertEqual(self.case_study.title, 'Test Case Study')
        self.assertEqual(self.case_study.url_slug, 'test-case-study')

    def test_white_paper_model(self):
        self.assertEqual(self.white_paper.title, 'Test White Paper')
        self.assertEqual(self.white_paper.url_slug, 'test-white-paper')

    def test_blog_model(self):
        self.assertEqual(self.blog_post.title, 'Test Blog Post')
        self.assertEqual(self.blog_post.author, 'Test Author')
        self.assertEqual(self.blog_post.url_slug, 'test-blog-post')

    def test_case_studies_view(self):
        response = self.client.get(reverse('cms_content:case_studies'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Case Study')
        self.assertTemplateUsed(response, 'pages/case_studies.html')

    def test_white_papers_view(self):
        response = self.client.get(reverse('cms_content:white_papers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test White Paper')
        self.assertTemplateUsed(response, 'pages/white_papers.html')

    def test_blog_detail_view(self):
        response = self.client.get(reverse('cms_content:blog_detail', args=['test-blog-post']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Blog Post')
        self.assertContains(response, 'Test Author')
        self.assertContains(response, 'This is the content of the test blog post.')
        self.assertTemplateUsed(response, 'pages/blog-details-left-sidebar.html')

    def test_contact_page_map_integration(self):
        response = self.client.get(reverse('pages:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<iframe width="100%" height="450" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://www.openstreetmap.org/export/embed.html?bbox=101.68037%2C3.13900%2C101.70037%2C3.15900&amp;layer=mapnik" style="border: 1px solid black"></iframe>')
