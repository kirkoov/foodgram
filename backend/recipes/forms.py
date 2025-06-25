from django.forms import ModelForm
from django.forms.widgets import TextInput

from recipes.models import Tag


class TagForm(ModelForm):
    """This way the tag hex codes will be in the respective colour for better visibility in the admin zone."""

    class Meta:
        model = Tag
        fields = "__all__"

        widgets = {
            "color": TextInput(attrs={"type": "color"}),
        }
