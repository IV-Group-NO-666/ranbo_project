import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ranbo_project.settings')

import django
django.setup()
from ranbo.models import User, Post, Like

def populate():
    user1_post = [
        {'Post_id':741,
         'View_times':35,
         'Like_times':24,
         'Content':"China's 34th gold! China women's table tennis team defeated Japan 3-0 in the Olympic women's team final",
         }
    ]

    user2_post = [
        {'Post_id':852,
         'View_times':266,
         'Like_times':36,
         'Content':"Today, the Tokyo Olympic Diving women's 10m platform singles final, Tokyo Olympic Team has nine gold and silver sweep! Quan Hongchan gold, Chen Yuxi silver!",
         }
    ]

    user3_post = [
        {'Post_id':963,
         'View_times':489,
         'Like_times':152,
         'Content':"It's a beautiful day!",
         }
    ]

    user = {'789':{'post':user1_post,'Username':'memeda'},
            '456':{'post':user2_post,'Username':'yingyingying'},
            '123':{'post':user3_post,'Username':'jijizha'}}


    for user, user_data in user.items():
        u = add_user(user,Username=user_data['Username'])
        for p in user_data['post']:
            add_post(u, Post_id=p['Post_id'],View_times=p['View_times'], Like_times=p['Like_times'], Content=p['Content'])


def add_post(User_id,Post_id,View_times=0,Like_times=0,Content=any):
    p = Post.objects.get_or_create(User_id=User_id, Post_id=Post_id,Content=Content)[0]
    p.view_times=View_times
    p.Like_tiles=Like_times
    p.save()
    return p

def add_user(User_id,Username):
    u = User.objects.get_or_create(User_id=User_id,Username=Username)[0]
    u.save()
    return u

if __name__ == '__main__':
    print('Starting Ranbo population script...')
    populate()