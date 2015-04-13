from __future__ import unicode_literals
from calendar import month_name
from django.http import Http404
from future.builtins import super

from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from mezzanine.blog.models import BlogPost, BlogCategory

from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.models import get_user_model
from mezzanine.utils.views import paginate

from drum.links.models import Link
from drum.links.utils import order_by_score
from juba.models import Juba


User = get_user_model()


class UserFilterView(ListView):
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
        context["no_data"] = ("Whoa, there's like, literally no data here, "
                              "like seriously, I totally got nothin.")
        return context


class ScoreOrderingView(UserFilterView):
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


class LinkView(object):
    def get_queryset(self):
        return Link.objects.published().select_related("user", "user__profile")


class HomepageList(LinkView, ScoreOrderingView):
    """
    List view for links, which can be for all users (homepage) or
    a single user (links from user's profile page). Links can be
    order by score (homepage, profile links) or by most recently
    created ("newest" main nav item).
    """

    date_field = "publish_date"
    score_fields = ["rating_sum", "comments_count"]

    def get_queryset(self):
        queryset = super(HomepageList, self).get_queryset()
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
            return "Links by %s" % context["profile_user"].profile
        else:
            return "Newest"


def homepage(request, tag=None, year=None, month=None, username=None,
             category=None, template="index.html"):
    settings.use_editable()
    templates = []
    blog_posts = BlogPost.objects.published(for_user=request.user)
    author = None

    prefetch = ("categories", "keywords__keyword")
    blog_posts = blog_posts.select_related("user").prefetch_related(*prefetch)
    links = Link.objects.published().select_related("user", "user__profile").prefetch_related()
    jubas = Juba.objects.published().select_related("user", "user__profile").prefetch_related()

    blog_posts = paginate(blog_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"blog_posts": blog_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author, "links": links, "jubas": jubas}
    templates.append(template)
    return render(request, templates, context)