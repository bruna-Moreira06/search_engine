from django.test import SimpleTestCase
from scengine.forms import SearchForm


class SearchFormTestCase(SimpleTestCase):
    def test_search_form_valid_data(self):
        form = SearchForm(data={
            'query': 'example',  # Exemple de requête valide
            'language': 'en',  # Langue valide (anglais)
            'product': 'classic'  # Produit valide (classique)
        })
        self.assertTrue(form.is_valid())  # Vérifie si le formulaire est valide

    def test_search_form_missing_data(self):
        form = SearchForm(data={})  # Données manquantes dans le formulaire
        # Vérifie si le formulaire n'est pas valide
        self.assertFalse(form.is_valid())
        # Vérifie le nombre d'erreurs (3 erreurs attendues)
        self.assertEqual(len(form.errors), 3)

    def test_search_form_invalid_language(self):
        form = SearchForm(data={
            'query': 'example',  # Exemple de requête valide
            'language': 'de',  # Langue invalide (allemand)
            'product': 'classic'  # Produit valide (classique)
        })
        # Vérifie si le formulaire n'est pas valide
        self.assertFalse(form.is_valid())
        # Vérifie le nombre d'erreurs (1 erreur attendue)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(
            form.errors['language'][0], 'Select a valid choice. de is not one of the available choices.'
        )  # Vérifie le message d'erreur spécifique pour le champ 'language'

    def test_search_form_invalid_product(self):
        form = SearchForm(data={
            'query': 'example',  # Exemple de requête valide
            'language': 'en',  # Langue valide (anglais)
            'product': 'invalid'  # Produit invalide
        })
        # Vérifie si le formulaire n'est pas valide
        self.assertFalse(form.is_valid())
        # Vérifie le nombre d'erreurs (1 erreur attendue)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(
            form.errors['product'][0], 'Select a valid choice. invalid is not one of the available choices.'
        )  # Vérifie le message d'erreur spécifique pour le champ 'product'
