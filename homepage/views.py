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


def get_blog_posts(category, month, request, tag, template, username, year):
    templates = []
    blog_posts = BlogPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        blog_posts = blog_posts.filter(keywords__keyword=tag)
    if year is not None:
        blog_posts = blog_posts.filter(publish_date__year=year)
        if month is not None:
            blog_posts = blog_posts.filter(publish_date__month=month)
            try:
                month = month_name[int(month)]
            except IndexError:
                raise Http404()
    if category is not None:
        category = get_object_or_404(BlogCategory, slug=category)
        blog_posts = blog_posts.filter(categories=category)
        templates.append(u"blog/blog_post_list_%s.html" %
                         str(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        blog_posts = blog_posts.filter(user=author)
        templates.append(u"blog/blog_post_list_%s.html" % username)
    prefetch = ("categories", "keywords__keyword")
    blog_posts = blog_posts.select_related("user").prefetch_related(*prefetch)
    blog_posts = paginate(blog_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"blog_posts": blog_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    templates.append(template)
    return context, templates


def homepage(request, tag=None, year=None, month=None, username=None,
             category=None, template="blog/blog_post_list.html"):
    settings.use_editable()
    context, templates = get_blog_posts(category, month, request, tag, template, username, year)
    return render(request, templates, context)