from django.contrib.auth.models import User
from django.shortcuts import render

from user_profile.models import Profile


def followers(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    profiles = user_profile.followers.all

    context = {
        'header': 'Followers',
        'profiles': profiles,
    }

    return render(request, 'templates/follow_list.html', context)


def following(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    profiles = user_profile.following.all

    context = {
        'header': 'Following',
        'profiles': profiles
    }
    return render(request, 'templates/follow_list.html', context)

