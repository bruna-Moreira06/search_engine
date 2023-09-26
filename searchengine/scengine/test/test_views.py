from django.test import Client, TestCase
from django.urls import reverse

from ..forms import SearchForm


class SearchArticleViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('search_html'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SearchForm)
        self.assertTemplateUsed(response, 'scengine/pages/search_form.html')

    def test_post(self):
        data = {
            'query': 'test',
            'language': 'en',
            'product': 'abc'
        }
        response = self.client.post(reverse('search_html'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'scengine/pages/search_articles_results.html')


class BenchmarkViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_benchmark_view(self):
        response = self.client.get(reverse('benchmark'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scengine/pages/benchmark.html')
