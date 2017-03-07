from __future__ import unicode_literals

from django.contrib.messages import info
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from mezzanine.accounts import get_profile_model

from show.forms import ShowForm
from show.models import Show

USER_PROFILE_RELATED_NAME = get_profile_model().user.field.related_query_name()


def index(request):
    shows = Show.objects.all()

    return render(request, 'show/show_list.html', {
        'shows': shows
    })


class ShowCreate(CreateView):
    """
    Link creation view - assigns the user to the new link, as well
    as setting Mezzanine's ``gen_description`` attribute to ``False``,
    so that we can provide our own descriptions.
    """

    form_class = ShowForm
    model = Show

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.gen_description = False
        info(self.request, "Link created")
        print(self.request)
        return super(ShowCreate, self).form_valid(form)


class ShowDetail(DetailView):
    pass
