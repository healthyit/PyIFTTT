import logging
import requests
import json
from .app import *

class Slack(App):
    # https://api.slack.com/tutorials/tracks/getting-a-token


    def auth_usage(self):
        # TODO
        if not self.config['auth'].get(type(self).__name__, False):
            logging.error('The {} App requires authorisation. Please define [token] in your auth.yml file.'.format(type(self).__name__))
            logging.error('Try here to get a Slack App Token: https://api.slack.com/tutorials/tracks/getting-a-token')
            logging.info('Example usage in Auth.yml:\n{}:\n  token: my_tocken\n  password: my_password'.format(type(self).__name__))
            raise AuthError
        auth = self.config['auth'].get(type(self).__name__, {})
        if not auth.get('username', False):
            logging.error('The {} App requires authorisation. Please define [token] in your auth.yml file.'.format(type(self).__name__))
            logging.error('Try here to get a Slack App Token: https://api.slack.com/tutorials/tracks/getting-a-token')
            logging.info('Example usage in Auth.yml:\n{}:\n  token: my_tocken\n  password: my_password'.format(type(self).__name__))
            raise AuthError

    def post_message_to_slack(self, text, slack_channel, slack_user_name, icon_emoji=None, blocks=None):
        return requests.post('https://slack.com/api/chat.postMessage', {
            'token': self.auth['token'],
            'channel': slack_channel,
            'text': text,
            'icon_emoji': icon_emoji,
            'username': slack_user_name,
            'blocks': json.dumps(blocks) if blocks else None
        }).json()

    def report_log(self, username, channel):
        self.post_message_to_slack(self.context.log_msg, 'PyIFTTT')
