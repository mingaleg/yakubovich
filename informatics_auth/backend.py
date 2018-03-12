from django.conf import settings
from django.contrib.auth.models import User

from game.models import Player
from .api import InformaticsApiException, InformaticsApiInvalidPassword
from .api import login

ADMINS = ['shhdup']


class InformaticsBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            info = login(username, password)
        except InformaticsApiInvalidPassword:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(
                username=username,
                password=password,
                first_name=info['firstname'],
                last_name=info['lastname'],
                is_superuser=(username in ADMINS),
                is_staff=(username in ADMINS),
            )
            user.save()
            player = Player(
                user=user,
                ejudge_id=info['ejudge_id'],
            )
            player.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None