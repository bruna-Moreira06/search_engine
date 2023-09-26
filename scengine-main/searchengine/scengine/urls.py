from django.urls import path

from .views import (HomeView, SearchArticleHTMLView, SearchArticleView,
                    benchmark_view, load_data)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('HTML_search/', SearchArticleHTMLView.as_view(), name='search_html'),
    path('API_search/', SearchArticleView.as_view(), name='api_search'),
    path('benchmark/', benchmark_view, name='benchmark'),
    path('load_data/', load_data, name='load_data')

]
