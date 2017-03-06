from django.views.generic import ListView, DetailView

from stack.models import Stack, Company


class StackView(object):
    def get_queryset(self):
        return Stack.objects.all()


class StackList(StackView, ListView):
    def get_queryset(self):
        queryset = super(StackList, self).get_queryset()
        return queryset.prefetch_related()

    def get_context_data(self, **kwargs):
        context = super(StackList, self).get_context_data(**kwargs)
        context["stacks"] = context["object_list"]
        return context


class StackDetail(StackView, DetailView):
    """
    Link detail view - threaded comments and rating are implemented
    in its template.
    """

    def get_context_data(self, **kwargs):
        context = super(StackDetail, self).get_context_data(**kwargs)
        context["companies"] = Company.objects.filter(stacks__id=context["stack"].id)
        return context
