from sys import maxsize
import pytest
from rest_framework.test import APIRequestFactory

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.test import TestCase

from .models import Tag
from .validators import validate_hex_color, validate_slug_field
from api.views import TagViewSet


class TagTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.test_tags = []
        cls.request_detail = cls.factory.get("/api/tags/0/")
        for index in range(3):
            tag = Tag(
                name=f"Tag {index}",
                color=f"#E26C{index}D",
                slug=f"-{index}_",
            )
            cls.test_tags.append(tag)
        Tag.objects.bulk_create(cls.test_tags)

    def test_create_tag_name(self):
        with pytest.raises(DataError):
            Tag.objects.create(
                name=settings.NUM_CHARS_MEALTIME_NAME * "s" + "more",
                color=None,
                slug=None,
            )

    def test_create_tag_color(self):
        with pytest.raises(ValidationError):
            Tag.objects.create(
                name=settings.NUM_CHARS_MEALTIME_NAME * "s",
                color=validate_hex_color("E26C2D"),
                slug=None,
            )

    def test_create_tag_slug(self):
        Tag.objects.create(
            name=settings.NUM_CHARS_MEALTIME_NAME * "s",
            color=None,
            slug=validate_slug_field("a-proper-slug"),
        )

    def test_get_taglist(self):
        request = self.factory.get("/api/tags/")
        view = TagViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.__dict__.get("data")
        if data is not None:
            for new, default in zip(data, self.test_tags):
                assert new["name"] == default.name
                assert new["color"] == default.color
                assert new["slug"] == default.slug
        else:
            raise DataError(
                "Empty data in the test_get_taglist() ordered dicts."
            )

    def test_get_tagdetail(self):
        view = TagViewSet.as_view({"get": "retrieve"})
        response = view(self.request_detail, pk=1)
        data = response.__dict__.get("data")
        if data is not None:
            assert data["name"] == self.test_tags[0].name
            assert data["color"] == self.test_tags[0].color
            assert data["slug"] == self.test_tags[0].slug
        else:
            raise DataError(
                "Empty data in the test_get_tagdetail() ordered dicts."
            )

    def test_get_tagdetail_status200(self):
        view = TagViewSet.as_view({"get": "retrieve"})
        response = view(self.request_detail, pk=1)
        assert response.status_code == 200

    def test_get_tagdetail_status404(self):
        view = TagViewSet.as_view({"get": "retrieve"})
        response = view(self.request_detail, pk=maxsize)
        assert response.status_code == 404
