
import pickle

import torch
from django.db import models
from sentence_transformers import util


class Rubrique(models.Model):
    # Identifiant unique de la rubrique
    rubrique_id = models.IntegerField(primary_key=True)
    slug = models.TextField()  # Champ pour le slug de la rubrique
    libelle = models.TextField()  # Champ pour le libellé de la rubrique

    def save(self, *args, **kwargs):
        # Appelle la méthode save() de la classe parent pour enregistrer l'objet
        super(Rubrique, self).save(*args, **kwargs)

    def __repr__(self) -> str:
        # Représentation sous forme de chaîne de caractères de la rubrique
        return f"{self.slug}"


class ArtHelp(models.Model):
    # Identifiant unique de l'article
    article_id = models.IntegerField(primary_key=True)
    # Clé étrangère vers le modèle Rubrique
    rubrique = models.ForeignKey(Rubrique, on_delete=models.CASCADE)
    slug = models.TextField()  # Slug de l'article
    title = models.TextField()  # Titre de l'article
    text = models.TextField()  # Texte de l'article
    language = models.CharField(max_length=5)  # Langue de l'article
    product = models.CharField(max_length=10)  # Catégorie de l'article
    date_update = models.DateField()  # Date de mise à jour de l'article
    # Données binaires pour l'embedding du titre
    title_embedding = models.BinaryField()
    # Similarité du titre (calculée)
    title_similarity = models.FloatField(null=True)
    # Données binaires pour l'embedding du texte
    text_embedding = models.BinaryField()
    # Similarité du texte (calculée)
    text_similarity = models.FloatField(null=True)
    # Similarité calculée (combinaison de la similarité du titre et du texte)
    computed_similarity = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        # Convertir les embeddings du titre en bytes
        self.title_embedding = pickle.dumps(self.title_embedding)
        # Convertir les embeddings du texte en bytes
        self.text_embedding = pickle.dumps(self.text_embedding)
        super(ArtHelp, self).save(*args, **kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__} - {self.pk} - {self.title} - {self.title_similarity} - {self.text_similarity}>"
        # Méthode spéciale qui renvoie une représentation en chaîne de caractères de l'objet.
        # Elle affiche le nom de la classe, l'identifiant, le titre et les similarités du titre et du texte.

    def calculate_cosine_similarity(self, search_embeddings):
        # Charger les embeddings à partir des données binaires avec pickle
        # Charger les embeddings du titre
        title_embeddings = pickle.loads(self.title_embedding)
        # Charger les embeddings du texte
        text_embeddings = pickle.loads(self.text_embedding)

        # Convertir les embeddings en tenseurs
        # Convertir les embeddings du titre en tenseur
        title_tensor = torch.tensor(title_embeddings)
        # Convertir les embeddings du texte en tenseur
        text_tensor = torch.tensor(text_embeddings)

        # Calculer les similarités cosinus
        cosine_similarities_title = util.pytorch_cos_sim(
            title_tensor, search_embeddings)  # Calculer la similarité cosinus du titre
        cosine_similarities_text = util.pytorch_cos_sim(
            text_tensor, search_embeddings)  # Calculer la similarité cosinus du texte

        # Stocker la similarité du titre dans l'objet
        self.title_similarity = cosine_similarities_title.item()
        # Stocker la similarité du texte dans l'objet
        self.text_similarity = cosine_similarities_text.item()
        # Renvoyer les similarités du titre et du texte calculées
        return self.title_similarity, self.text_similarity
