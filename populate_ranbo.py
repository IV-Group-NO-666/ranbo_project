import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ranbo_project.settings')

import django

django.setup()
from ranbo.models import User, Post, Like


def populate():
    user1_post = [
        {'post_id': 741,
         'view_times': 35,
         'like_times': 24,
         'content': "China's 34th gold! China women's table tennis team defeated Japan 3-0 in the Olympic women's team final",
         }
    ]

    user2_post = [
        {'post_id': 852,
         'view_times': 266,
         'like_times': 36,
         'content': "Today, the Tokyo Olympic Diving women's 10m platform singles final, Tokyo Olympic Team has nine gold and silver sweep! Quan Hongchan gold, Chen Yuxi silver!",
         }
    ]

    user3_post = [
        {'post_id': 963,
         'view_times': 489,
         'like_times': 152,
         'content': "It's a beautiful day!",
         }
    ]

    user = {'789': {'post': user1_post, 'username': 'memeda'},
            '456': {'post': user2_post, 'username': 'yingyingying'},
            '123': {'post': user3_post, 'username': 'jijizha'}}

    for user, user_data in user.items():
        u = add_user(user, username=user_data['username'])
        for p in user_data['post']:
            add_post(u, post_id=p['post_id'], view_times=p['view_times'], like_times=p['like_times'],
                     content=p['content'])


def add_post(user_id, post_id, view_times=0, like_times=0, content=any):
    p = Post.objects.get_or_create(user_id=user_id, post_id=post_id, content=content)[0]
    p.view_times = view_times
    p.like_times = like_times
    p.save()
    return p


def add_user(user_id, username):
    u = User.objects.get_or_create(user_id=user_id, username=username)[0]
    u.save()
    return u


if __name__ == '__main__':
    print('Starting Ranbo population script...')
    populate()
