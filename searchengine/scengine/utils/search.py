
import time

from ..models import ArtHelp
from .tools import embeddings, save_execution_time


def search_articles(search_term, language, product, n=10):
    """
    Fonction pour rechercher des articles en fonction d'un terme de recherche et récupérer les articles les plus pertinents.

    Args:
        search_term (str): Le terme de recherche.
        language (str): La langue des articles.
        product (str): Le nom du produit.
        n (int, optionnel): Le nombre d'articles les plus pertinents à récupérer. Par défaut, 10.

    Returns:
        tuple: Les articles les plus pertinents et le temps d'exécution.
    """
    start_time = time.time()  # Démarrer le chronomètre
    embedding = embeddings(search_term)

    # Définir les poids pour la similarité du titre et du texte
    weight_text = 0.9  # Poids pour la similarité du texte
    weight_title = 0.3  # Poids pour la similarité du titre
    weight_similarity = weight_text + weight_title  # Poids total pour la similarité

    # Définir le seuil de similarité minimale pour filtrer les articles
    similarity_threshold = 0.30
    # Récupérer les articles en fonction de la langue et du produit
    queryset_art = ArtHelp.objects.filter(language=language, product=product)
    # Calculer la similarité cosinus pour les articles
    for article in queryset_art:
        article.calculate_cosine_similarity(search_embeddings=embedding)

        # Calculer la similarité calculée en utilisant la similarité pondérée du titre et du texte
        article.computed_similarity = (
            article.title_similarity * weight_title + article.text_similarity * weight_text
        ) / weight_similarity

    # Trier les articles par similarité calculée dans l'ordre décroissant et retourner les n premiers articles
    top_articles = sorted(
        (
            {
                'article': article,
                'slug': article.rubrique.slug
            }
            for article in queryset_art
            if article.computed_similarity > similarity_threshold
        ),
        key=lambda x: x['article'].computed_similarity,
        reverse=True,
    )[:n]

    # Extraire les articles et les slugs des résultats
    articles = [article['article'] for article in top_articles]
    slugs = [article['slug'] for article in top_articles]

    end_time = time.time()
    execution_time = end_time - start_time
    save_execution_time('search_articles', execution_time)
    return articles, slugs, execution_time
