from rest_framework import filters
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from stack.models import Stack, Company, Job


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('title',)


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('name', 'salary_start', 'salary_end')


class StackSerializer(serializers.HyperlinkedModelSerializer):
    company_stacks = CompanySerializer(many=True, required=False, read_only=True)
    job_stacks = JobSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Stack
        fields = ('title', 'content', 'featured_image', "description", "company_stacks", "job_stacks")


class StackSet(viewsets.ModelViewSet):
    queryset = Stack.objects.filter()
    serializer_class = StackSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
