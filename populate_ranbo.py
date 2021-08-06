import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ranbo_project.settings')

import django

django.setup()
from ranbo.models import User, Post, Like


def populate():
    user1_post = [
        {
         'view_times': 35,
         'like_times': 24,
         'content': "China's 34th gold! China women's table tennis team defeated Japan 3-0 in the Olympic women's team final",
         }
    ]

    user2_post = [
        {
         'view_times': 266,
         'like_times': 36,
         'content': "Today, the Tokyo Olympic Diving women's 10m platform singles final, Tokyo Olympic Team has nine gold and silver sweep! Quan Hongchan gold, Chen Yuxi silver!",
         },
         {'view_times':654,
          'like_times':459,
          'content':"lkasfd laksd naksldn  aoi nak n lak na lk"},
          {'view_times':789,
          'like_times':62,
          'content':"adsajs o iaja oij aok aoksnd saoid j"}
    ]

    user3_post = [
        {
         'view_times': 489,
         'like_times': 152,
         'content': "It's a beautiful day!",
         },
         {'view_times':94,
          'like_times':6,
          'content':"asjd ias dbiasj bdiasj dbqwkej bwqk e"}
    ]

    user = {'memeda': {'post': user1_post},
            'yingyingying': {'post': user2_post},
            'jijizha': {'post': user3_post}}

    for user, user_data in user.items():
        u = add_user(user)
        for p in user_data['post']:
            add_post(u, view_times=p['view_times'], like_times=p['like_times'],
                     content=p['content'])


def add_post(user, view_times=0, like_times=0, content=any):
    p = Post.objects.get_or_create(user=user,  content=content)[0]
    p.view_times = view_times
    p.like_times = like_times
    p.save()
    return p


def add_user(username):
    u = User.objects.get_or_create( username=username)[0]
    u.save()
    return u


if __name__ == '__main__':
    print('Starting Ranbo population script...')
    populate()
