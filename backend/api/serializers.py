from rest_framework import serializers

from recipes.models import Tag


class TaggSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
