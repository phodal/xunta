import itertools
from mezzanine.blog.models import BlogPost

from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from juba.models import Juba

from links.models import Link


class TimelineSerializer(serializers.Serializer):
    model = serializers.SerializerMethodField('is_named_bar')
    title = serializers.CharField()
    slug = serializers.CharField()

    @staticmethod
    def is_named_bar(model):
        return str(model.__class__.__name__ )


class AllListView(viewsets.ModelViewSet):
    serializer_class = TimelineSerializer

    def list(self, request):
        queryset = list(itertools.chain(Link.objects.all(), Juba.objects.all(), BlogPost.objects.all()))
        serializer = TimelineSerializer(queryset, many=True)
        return Response(serializer.data)