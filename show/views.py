from __future__ import unicode_literals

from datetime import timedelta

from django.contrib.messages import info, error
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic import CreateView
from future.builtins import super
from mezzanine.accounts import get_profile_model
from mezzanine.conf import settings

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

    def form_valid(self, form):
        hours = getattr(settings, "ALLOWED_DUPLICATE_JUBA_HOURS", None)
        if hours and form.instance.juba:
            lookup = {
                "juba": form.instance.juba,
                "publish_date__gt": now() - timedelta(hours=hours),
            }
            try:
                show = Show.objects.get(**lookup)
            except Show.DoesNotExist:
                pass
            else:
                error(self.request, "Juba exists")
                return redirect(show)
        form.instance.user = self.request.user
        form.instance.gen_description = False
        info(self.request, "Juba created")
        return super(ShowCreate, self).form_valid(form)
