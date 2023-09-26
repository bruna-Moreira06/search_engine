from django.test import SimpleTestCase
from django.urls import resolve, reverse
from scengine.views import (SearchArticleHTMLView, SearchArticleView,
                            benchmark_view)


class UrlsTestCase(SimpleTestCase):
    def test_search_article_HTML_url(self):
        url = reverse('search_html')
        self.assertEqual(resolve(url).func.view_class, SearchArticleHTMLView)

    def test_search_article_API_url(self):
        url = reverse('api_search')
        self.assertEqual(resolve(url).func.view_class, SearchArticleView)

    def test_benchmark_url(self):
        url = reverse('benchmark')
        self.assertEqual(resolve(url).func, benchmark_view)
