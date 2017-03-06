from django.views.generic import ListView

from stack.models import Stack


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
