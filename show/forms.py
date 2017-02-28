from django.forms import ModelForm

from show.models import Show, Comment


class PostPictureForm(ModelForm):
    class Meta:
        model = Show
        fields = ['title', 'image']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']