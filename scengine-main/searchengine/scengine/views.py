import glob
import json
import os

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from rest_framework.views import APIView

from .forms import SearchForm
from .serializers import ArtHelpSerializer
from .utils.data_extraction import load_help_data
from .utils.search import search_articles


class HomeView(View):
    def get(self, request):
        return render(request, 'scengine/pages/home.html')


class SearchArticleView(APIView):
    def get(self, request):
        form = SearchForm()
        return render(request, 'scengine/pages/search_form.html', {'form': form})

    def post(self, request):
        query = request.data.get('query')
        language = request.data.get('language')
        product = request.data.get('product')
        results_articles, slugs, time_articles = search_articles(
            query, language, product)
        serializer = ArtHelpSerializer(results_articles, many=True)
        data = {
            'results_articles': serializer.data,
            'slugs': slugs,
            'query': query,
            'language': language,
            'product': product,
            'time': time_articles
        }
        return JsonResponse(data)


class SearchArticleHTMLView(SearchArticleView):
    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, *kwargs)
        data = json.loads(data.content)
        # Combine results_articles and slugs into a single list of tuples
        results_with_slugs = zip(data['results_articles'], data['slugs'])
        data['results_with_slugs'] = results_with_slugs
        return render(request, 'scengine/pages/search_articles_results.html', data)


def load_data(request):
    # Exécuter la fonction de chargement des données
    load_help_data()
    # Afficher un message de chargement
    messages.info(request, 'Données chargées')
    return redirect('home')


def benchmark_view(request):
    json_folder = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../scengine/', 'benchmarks')
    json_files = glob.glob(os.path.join(json_folder, '*.json'))

    benchmark_data = []
    for file_path in json_files:
        with open(file_path, 'r') as f:
            data = json.load(f)

            # Obtenir le nom de la fonction à partir du nom du fichier
            function_name = os.path.splitext(os.path.basename(file_path))[0]
            execution_times = [entry['execution_time'] for entry in data]
            num_entries = len(execution_times)
            avg_execution_time = sum(execution_times) / num_entries

            benchmark_data.append({
                'function_name': function_name,
                'num_entries': num_entries,
                'avg_execution_time': avg_execution_time
            })

    context = {'benchmark_data': benchmark_data}
    return render(request, 'scengine/pages/benchmark.html', context)
