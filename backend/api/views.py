from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import TagSerializer
from recipes.models import Tag


class TagViewSet(ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None
