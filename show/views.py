from __future__ import unicode_literals

from django.contrib.messages import info
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView
from mezzanine.accounts import get_profile_model

from show.forms import ShowForm
from show.models import Show

USER_PROFILE_RELATED_NAME = get_profile_model().user.field.related_query_name()

class ShowView(object):
    def get_queryset(self):
        return Show.objects.all()

class ShowList(ShowView, ListView):
    def get_queryset(self):
        queryset = super(ShowList, self).get_queryset()
        return queryset.prefetch_related()

    def get_context_data(self, **kwargs):
        context = super(ShowList, self).get_context_data(**kwargs)
        context["shows"] = context["object_list"]
        return context


class ShowCreate(CreateView):
    form_class = ShowForm
    model = Show

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.gen_description = False
        info(self.request, "又秀了一次恩爱")
        return super(ShowCreate, self).form_valid(form)


class ShowDetail(DetailView):
    pass
