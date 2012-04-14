import logging
from random import choice
from string import letters
from django.contrib.auth.models import User

from gatekeeper.mail import send_moderation_notices


logger = logging.getLogger(__name__)

def create_user(userdata):
    """
    """
    userdata['username'] = get_username(userdata['first_name'], userdata['last_name'], 0)
    
    new_user = User.objects.create_user(userdata['username'], 
                                        userdata['email'], 
                                        userdata['password1'])
    new_user.first_name = userdata['first_name']
    new_user.last_name = userdata['last_name']
    new_user.is_active = False
    new_user.save()

    user_profile = new_user.get_profile()
    user_profile.focus = userdata['focus']
    user_profile.blog_url = userdata['blog_url']
    user_profile.twitter_name = userdata['twitter_name']
    user_profile.location = userdata['location']
    user_profile.profession = userdata['profession']
    user_profile.notify_recent_changes = userdata['notify_recent_changes']
    user_profile.save()
    
    send_moderation_notices(new_user)
    return new_user


def user_in_group(user, groupname):
    if not user:
        logger.warn("Can't test if empty user is in group %s" % groupname)
        return False
    return filter(lambda grp: grp.name == groupname, user.groups.all())


def get_username(firstname, lastname, index):
    """
    """
    username = u''.join([firstname.capitalize(), lastname.capitalize()])
    if index > 0:
        username += str(index)
    try:
        user = User.objects.get(username=username)
        return get_username(firstname, lastname, index+1)
    except User.DoesNotExist:
        return username

    