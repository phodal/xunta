from django.shortcuts import render, redirect

from show.models import Show


def index(request):
    if not request.user.is_authenticated():
        return redirect('login')

    # Only return posts from users that are being followed, test this later
    # for performance / improvement
    users_followed = request.user.profile.follows.all()
    shows = Show.objects.filter(
                user_profile__in=users_followed).order_by('-posted_on')

    return render(request, 'show/show_list.html', {
        'shows': shows
    })