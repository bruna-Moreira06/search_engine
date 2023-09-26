import numpy as np
from django.conf import settings
from django.test import TestCase

from ..utils.tools import date_converter, embeddings, save_execution_time


class UtilsTestCase(TestCase):
    def setUp(self):
        self.model = settings.MODEL

    def test_embeddings_returns_valid_embedding(self):
        text = "This is a test sentence."
        embedding = embeddings(text)
        self.assertIsInstance(
            embedding, np.ndarray, "The embedding should be an instance of numpy.ndarray.")
        self.assertEqual(embedding.shape, (512,),
                         "The shape of the embedding should be (512,).")

    def test_save_execution_time_saves_execution_time(self):
        function_name = "embeddings"
        execution_time = 1.2345678
        save_execution_time(function_name, execution_time)
        # Add assertions to verify that the execution time is saved correctly

    def test_date_converter(self):
        # Test avec une date valide
        date_string = "2023-06-15T12:30:00+00:00"
        expected_result = (2023, 6, 15)
        result = date_converter(date_string)
        self.assertEqual(result, expected_result)

        # Test avec une autre date valide
        date_string = "2022-01-01T00:00:00+00:00"
        expected_result = (2022, 1, 1)
        result = date_converter(date_string)
        self.assertEqual(result, expected_result)

        # Test avec une date invalide
        date_string = "2023-06-15"  # Format incorrect
        with self.assertRaises(ValueError):
            date_converter(date_string)

        # Test avec une autre date invalide
        date_string = "2023-06-15T12:30:00"  # Format incorrect
        with self.assertRaises(ValueError):
            date_converter(date_string)
