from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelform_factory

from show.models import Show, Comment

BaseShowForm = modelform_factory(Show, fields=["title", "image"])


class PostPictureForm(ModelForm):
    class Meta:
        model = Show
        fields = ['title', 'image']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class ShowForm(BaseShowForm):
    def clean(self):
        title = self.cleaned_data.get("title", None)
        image = self.cleaned_data.get("image", None)

        if not title and not image:
            raise ValidationError("Either a link or description is required")
        return self.cleaned_data
