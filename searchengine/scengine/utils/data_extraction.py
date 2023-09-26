import datetime
import json
import os
import pickle
import time

from bs4 import BeautifulSoup
from django.conf import settings

from ..models import ArtHelp, Rubrique
from .tools import date_converter, embeddings, save_execution_time


def parse_articles_list(article_list):
    """
    Recursively iterate over articles by section and store their slugs in ARTICLES_LIST.

    Args:
        article_list (dict): Dictionary containing article information.

    Returns:
        list: List of article slugs.
    """
    start_time = time.time()

    for k, article in article_list.items():
        settings.ARTICLES_LIST.append(
            (article.get("slug").rstrip('/')))

    end_time = time.time()
    execution_time = end_time - start_time
    save_execution_time('parse_articles_list', execution_time)
    return settings.ARTICLES_LIST


def load_help_data():
    """
    Charge les données d'aide dans la base de données en récupérant l'arborescence et les informations des articles depuis l'API.

    Cette fonction itère sur les IDs des webzines et les paramètres de langue pour récupérer les données JSON de l'arborescence,
    charger les rubriques dans la base de données, récupérer les slugs des articles, récupérer les données JSON des articles, et
    stocker les informations des articles dans la base de données.
    """
    start_time = time.time()
    dossier_cache = settings.CACHE_DIR

    for nom_fichier in os.listdir(dossier_cache):
        if nom_fichier.startswith("article"):
            chemin_fichier = os.path.join(dossier_cache, nom_fichier)
            with open(chemin_fichier) as fichier:
                article = json.load(fichier)

            # Récupérer la langue du premier paragraphe de l'article
            prodlang = next(iter(article["paragraphs"].values())).get("lg")
            # Récupérer le produit à partir de la langue
            product = prodlang[3:-3]
            # Récupérer la langue à partir de la langue
            language = prodlang[-2:]

            rubrique_id = article.get("rubrique_info").get("id_rubrique")
            try:
                # Vérifier si la rubrique existe déjà dans la base de données
                rubrique_object = Rubrique.objects.get(rubrique_id=rubrique_id)
            except Rubrique.DoesNotExist:
                # Créer une nouvelle rubrique si elle n'existe pas déjà
                rub_slug = article.get("rubrique_info").get("slug")
                libelle = article.get("rubrique_info").get("libelle")
                rubrique_object = Rubrique(
                    rubrique_id=rubrique_id, slug=rub_slug, libelle=libelle)
                rubrique_object.save()

            id_article = article.get("id_article")
            y, m, d = date_converter(article.get("date_modif"))
            date_update = datetime.date(y, m, d)
            title, text = clean_content(article)
            slug = article.get("slug")

            # Vérifier si l'article existe déjà
            try:
                article_object = ArtHelp.objects.get(article_id=id_article)
                if article_object.date_update != date_update:
                    # Encoder les phrases pour obtenir leurs embeddings
                    title_embedding = embeddings(title)
                    text_embedding = embeddings(text)
                    # Mettre à jour l'article s'il existe déjà
                    article_object.title = title
                    article_object.text = text
                    article_object.slug = slug
                    article_object.language = language
                    article_object.product = product
                    article_object.rubrique = rubrique_object
                    article_object.title_embedding = title_embedding
                    article_object.text_embedding = text_embedding
                    article_object.date_update = date_update
                    article_object.save()
                    print(f"Mise à jour de {title}")
                else:
                    print(f"L'article {title} existe déjà")

            except ArtHelp.DoesNotExist:
                # Encoder les phrases pour obtenir leurs embeddings
                title_embedding = embeddings(title)
                text_embedding = embeddings(text)
                # Créer un nouvel article s'il n'existe pas déjà
                article_object = ArtHelp(article_id=id_article, title=title,
                                         text=text, date_update=date_update,
                                         language=language, product=product,
                                         slug=slug, rubrique=rubrique_object,
                                         title_embedding=title_embedding,
                                         text_embedding=text_embedding)
                article_object.save()
                print(f"Création de {title}")

    print("Chargement des données d'aide terminé")
    end_time = time.time()
    execution_time = end_time - start_time
    save_execution_time('load_help_data', execution_time)


def parse_rub_slugs(rubdict):
    """
    Recursively iterate over the rubrics and store their slugs in RUB_SLUGS.
    """
    for k, rub in rubdict.items():
        settings.RUB_SLUGS.append(rub.get("slug"))
        if rub.get("children_rub", {}):
            parse_rub_slugs(rub.get("children_rub"))


def clean_content(article):
    """
    Fonction pour nettoyer le titre et le texte d'un article.
    Elle supprime les balises HTML, les URL, la ponctuation et les espaces superflus.
    Elle effectue également une correction orthographique et met à jour le corpus global avec les mots corrigés.

    Args:
        article (dict): Les données JSON de l'article.

    Returns:
        tuple: Le titre nettoyé et le texte.
    """
    start_time = time.time()  # Démarrer le chronomètre
    titre = article.get("titre")
    # Générer le contenu textuel
    text_content = ""
    for paragraphe in article["paragraphs"].values():
        inter_titre = paragraphe.get("inter_titre")
        texte = paragraphe.get("texte")
        if inter_titre:
            text_content += inter_titre + " "
        if texte:
            texte = BeautifulSoup(texte, "html.parser").get_text()
            text_content += texte + " "
    end_time = time.time()
    execution_time = end_time - start_time
    save_execution_time('clean_content', execution_time)
    # Retourner le titre et le texte nettoyés
    return titre, text_content
