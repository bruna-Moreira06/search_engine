import torch
from django.test import TestCase
from sentence_transformers import util

from ..models import ArtHelp, Rubrique


class ArtHelpTestCase(TestCase):
    def setUp(self):
        self.article = ArtHelp(
            article_id=1,
            title="Test Article",
            text="This is a test article",
            language="en",
            date_update="2020-01-01",
            product="classic",
            title_embedding=[0.4, 0.5, 0.6],
            text_embedding=[0.7, 0.8, 0.9]
        )

    def test_calculate_cosine_similarity(self):
        search_embeddings = torch.tensor([[0.2, 0.3, 0.4]])
        expected_title_similarity = util.pytorch_cos_sim(
            torch.tensor(self.article.title_embedding), search_embeddings).item()
        expected_text_similarity = util.pytorch_cos_sim(
            torch.tensor(self.article.text_embedding), search_embeddings).item()

        title_similarity, text_similarity = self.article.calculate_cosine_similarity(
            search_embeddings)

        self.assertEqual(title_similarity, expected_title_similarity)
        self.assertEqual(text_similarity, expected_text_similarity)


class RubriqueTestCase(TestCase):
    def setUp(self):
        self.rubrique = Rubrique(
            rubrique_id=1,
            slug="test-rubrique",
            libelle="Test Rubrique"
        )

    def test_rubrique_representation(self):
        expected_representation = "test-rubrique"
        representation = repr(self.rubrique)

        self.assertEqual(representation, expected_representation)
