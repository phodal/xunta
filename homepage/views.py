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