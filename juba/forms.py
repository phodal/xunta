
from django.conf import settings
from django.forms.models import modelform_factory
from django.forms import ValidationError

from .models import Juba


BaseLinkForm = modelform_factory(Juba, fields=["title", "juba", "description"])


class JubaForm(BaseLinkForm):

    def clean(self):
        juba = self.cleaned_data.get("juba", None)
        description = self.cleaned_data.get("description", None)
        if not juba and not description:
            raise ValidationError("Either a link or description is required")
        return self.cleaned_data
