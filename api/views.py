import itertools
from mezzanine.blog.models import BlogPost

from rest_framework import serializers, viewsets
from rest_framework import filters
from rest_framework.response import Response

from juba.models import Juba

from links.models import Link


class TimelineSerializer(serializers.Serializer):
    model = serializers.SerializerMethodField('get_model_name')
    title = serializers.CharField()
    slug = serializers.CharField()

    @staticmethod
    def get_model_name(model):
        model = str(model.__class__.__name__).lower()
        if model is 'blogpost':
            model = 'blog'
        return model


class AllListView(viewsets.ModelViewSet):
    serializer_class = TimelineSerializer

    def list(self, request):
        queryset = list(itertools.chain(Link.objects.all(), Juba.objects.all(), BlogPost.objects.all()))
        search_param = self.request.QUERY_PARAMS.get('search', None)
        serializer = TimelineSerializer(queryset, many=True)
        return Response(serializer.data)