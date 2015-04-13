from django.forms.models import modelform_factory
from django.forms import ValidationError

from .models import Juba


BaseJubaForm = modelform_factory(Juba, fields=["title", "content", "description", "slug"])


class JubaForm(BaseJubaForm):

    def clean(self):
        content = self.cleaned_data.get("content", None)
        description = self.cleaned_data.get("description", None)
        if not content and not description:
            raise ValidationError("Either a link or description is required")
        return self.cleaned_data
