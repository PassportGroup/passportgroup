from pusher import Pusher as P
import os
from apps.core.exceptions import GeneralException


class Pusher:
    def __init__(self):
        self.set_credentials()
        self.pusher = P(
            app_id=self.app_id,
            key=self.key,
            secret=self.secret,
            cluster=self.cluster
        )

    def authenticate(self, channel, socket_id):
        auth = self.pusher.authenticate(
            channel=channel,
            socket_id=socket_id
        )

        return auth

    def trigger_notifications(self, username, data):
        channel = f'PassportGroup.web.notifications.{username}'
        self.pusher.trigger(channel, 'notification', data)

    def trigger_new_message(self, receiver_username):
        channel = f'PassportGroup.new.message.{receiver_username}'
        self.pusher.trigger(channel, 'message', True)

    def set_credentials(self):
        try:
            assert os.getenv('PUSHER_APP_ID'), 'Invalid pusher app id'
            assert os.getenv('PUSHER_KEY'), 'Invalid pusher key'
            assert os.getenv('PUSHER_SECRET'), 'Invalid pusher secret'
            assert os.getenv('PUSHER_CLUSTER'), 'Invalid pusher cluster'

            self.pusher.app_id = os.getenv('PUSHER_APP_ID')
            self.pusher.key = os.getenv('PUSHER_KEY')
            self.pusher.secret = os.getenv('PUSHER_SECRET')
            self.pusher.cluster = os.getenv('PUSHER_CLUSTER')

        except AssertionError as e:
            raise GeneralException(e.args[0])

