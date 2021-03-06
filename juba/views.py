# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from future.builtins import super

from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.messages import info, error

from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, DetailView, TemplateView

from mezzanine.conf import settings
from mezzanine.generic.models import ThreadedComment, Keyword
from mezzanine.utils.views import paginate

from .forms import JubaForm
from .models import Juba
from .utils import order_by_score
from mezzanine.accounts import get_profile_model

USER_PROFILE_RELATED_NAME = get_profile_model().user.field.related_query_name()

class UserFilterView(ListView):
    """
    List view that puts a ``profile_user`` variable into the context,
    which is optionally retrieved by a ``username`` urlpattern var.
    If a user is loaded, ``object_list`` is filtered by the loaded
    user. Used for showing lists of links and comments.
    """

    def get_context_data(self, **kwargs):
        context = super(UserFilterView, self).get_context_data(**kwargs)
        try:
            username = self.kwargs["username"]
        except KeyError:
            profile_user = None
        else:
            users = User.objects.select_related("profile")
            lookup = {"username__iexact": username, "is_active": True}
            profile_user = get_object_or_404(users, **lookup)
            qs = context["object_list"].filter(user=profile_user)
            context["object_list"] = qs
        context["profile_user"] = profile_user
        context["no_data"] = ("终于等到你了")
        return context


class ScoreOrderingView(UserFilterView):
    """
    List view that optionally orders ``object_list`` by calculated
    score. Subclasses must defined a ``date_field`` attribute for the
    related model, that's used to determine time-scaled scoring.
    Ordering by score is the default behaviour, but can be
    overridden by passing ``False`` to the ``by_score`` arg in
    urlpatterns, in which case ``object_list`` is sorted by most
    recent, using the ``date_field`` attribute. Used for showing lists
    of links and comments.
    """

    def get_context_data(self, **kwargs):
        context = super(ScoreOrderingView, self).get_context_data(**kwargs)
        qs = context["object_list"]
        context["by_score"] = self.kwargs.get("by_score", True)
        if context["by_score"]:
            qs = order_by_score(qs, self.score_fields, self.date_field)
        else:
            qs = qs.order_by("-" + self.date_field)
        context["object_list"] = paginate(qs, self.request.GET.get("page", 1),
            settings.ITEMS_PER_PAGE, settings.MAX_PAGING_LINKS)
        context["title"] = self.get_title(context)
        return context


class JubaView(object):
    """
    List and detail view mixin for links - just defines the correct
    queryset.
    """
    def get_queryset(self):
        return Juba.objects.published().select_related("user", "user__profile")


class JubaList(JubaView, ScoreOrderingView):
    """
    List view for links, which can be for all users (homepage) or
    a single user (links from user's profile page). Links can be
    order by score (homepage, profile links) or by most recently
    created ("newest" main nav item).
    """

    date_field = "publish_date"
    score_fields = ["rating_sum", "comments_count"]

    def get_queryset(self):
        queryset = super(JubaList, self).get_queryset()
        tag = self.kwargs.get("tag")
        if tag:
            queryset = queryset.filter(keywords__keyword__slug=tag)
        return queryset.prefetch_related("keywords__keyword")

    def get_title(self, context):
        tag = self.kwargs.get("tag")
        if tag:
            return get_object_or_404(Keyword, slug=tag).title
        if context["by_score"]:
            return ""  # Homepage
        if context["profile_user"]:
            return "由 %s 发布的" % getattr(
                context["profile_user"],
                USER_PROFILE_RELATED_NAME
            )
        else:
            return "聚吧"


class JubaCreate(CreateView):
    """
    Link creation view - assigns the user to the new link, as well
    as setting Mezzanine's ``gen_description`` attribute to ``False``,
    so that we can provide our own descriptions.
    """

    form_class = JubaForm
    model = Juba

    def form_valid(self, form):
        hours = getattr(settings, "ALLOWED_DUPLICATE_JUBA_HOURS", None)
        if hours and form.instance.juba:
            lookup = {
                "juba": form.instance.juba,
                "publish_date__gt": now() - timedelta(hours=hours),
            }
            try:
                juba = Juba.objects.get(**lookup)
            except Juba.DoesNotExist:
                pass
            else:
                error(self.request, "Juba exists")
                return redirect(juba)
        form.instance.user = self.request.user
        form.instance.gen_description = False
        info(self.request, "Juba created")
        return super(JubaCreate, self).form_valid(form)


class JubaDetail(JubaView, DetailView):
    """
    Link detail view - threaded comments and rating are implemented
    in its template.
    """
    pass


class CommentList(ScoreOrderingView):
    """
    List view for comments, which can be for all users ("comments" and
    "best" main nav items) or a single user (comments from user's
    profile page). Comments can be order by score ("best" main nav item)
    or by most recently created ("comments" main nav item, profile
    comments).
    """

    date_field = "submit_date"
    score_fields = ["rating_sum"]

    def get_queryset(self):
        qs = ThreadedComment.objects.filter(is_removed=False, is_public=True)
        select = ["user", "user__profile"]
        prefetch = ["content_object"]
        return qs.select_related(*select).prefetch_related(*prefetch)

    def get_title(self, context):
        if context["profile_user"]:
            return "Comments by %s" % context["profile_user"].profile
        elif context["by_score"]:
            return "Best comments"
        else:
            return "Latest comments"


class TagList(TemplateView):
    template_name = "juba/tag_list.html"
