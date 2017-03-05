from __future__ import unicode_literals

from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView
from mezzanine.accounts import get_profile_model

from show.forms import ShowForm
from show.models import Show

USER_PROFILE_RELATED_NAME = get_profile_model().user.field.related_query_name()


def index(request):
    if not request.user.is_authenticated():
        return redirect('login')

    if not hasattr(request.user, 'profile'):
        return redirect('/')

    # Only return posts from users that are being followed, test this later
    # for performance / improvement
    users_followed = request.user.profile.follows.all()
    shows = Show.objects.filter(
        user_profile__in=users_followed).order_by('-posted_on')

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
