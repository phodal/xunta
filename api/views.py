import itertools

from mezzanine.blog.models import BlogPost
from rest_framework import serializers, viewsets
from rest_framework.response import Response

from juba.models import Juba
from links.models import Link


class TimelineSerializer(serializers.Serializer):
    model = serializers.SerializerMethodField('get_model_name')
    title = serializers.CharField()
    pk = serializers.CharField()
    slug = serializers.CharField()

    @staticmethod
    def get_model_name(model):
        model = str(model.__class__.__name__).lower()
        if model == 'blogpost':
            model = 'blog'
        return model


class AllListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TimelineSerializer

    def get_paginate_by(self):
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 10

    def list(self, request):
        queryset = list(itertools.chain(Link.objects.all(), Juba.objects.all(), BlogPost.objects.all()))[:10]
        search_param = self.request.query_params.get('search', None)
        if search_param is not None:
            link_queryset = Link.objects.filter(title__contains=search_param)
            juba_queryset = Juba.objects.filter(title__contains=search_param)
            blog_queryset = BlogPost.objects.filter(title__contains=search_param)
            queryset = list(itertools.chain(link_queryset, juba_queryset, blog_queryset))[:10]

        homepage = self.request.query_params.get('homepage', None)
        if homepage is not None:
            link_queryset = Link.objects.all()[:5]
            juba_queryset = Juba.objects.all()[:5]
            blog_queryset = BlogPost.objects.all()[:5]
            queryset = list(itertools.chain(link_queryset, juba_queryset, blog_queryset))

        serializer = TimelineSerializer(queryset, many=True)
        return Response(serializer.data)