from rest_framework import serializers

from .models import ArtHelp, Rubrique


class RubriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubrique
        fields = ('slug',)


class ArtHelpSerializer(serializers.ModelSerializer):
    rubrique = RubriqueSerializer()

    class Meta:
        model = ArtHelp
        fields = ('article_id', 'rubrique', 'slug', 'title', 'text',
                  'date_update', 'title_similarity', 'text_similarity','computed_similarity')
