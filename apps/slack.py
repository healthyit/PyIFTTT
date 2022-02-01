import logging
import requests
import json
from .app import *

class Slack(App):
    # https://api.slack.com/tutorials/tracks/getting-a-token


    def auth_usage(self):
        # TODO
        if not self.config['auth'].get(type(self).__name__, False):
            logging.error('The {} App requires authorisation. Please define [webhook] in your auth.yml file.'.format(type(self).__name__))
            logging.info('Example usage in Auth.yml:\n{}:\n  webhook: https://hooks.slack.com/services/123/456/789/'.format(type(self).__name__))
            raise AuthError
        auth = self.config['auth'].get(type(self).__name__, {})
        if not auth.get('username', False):
            logging.error('The {} App requires authorisation. Please define [webhook] in your auth.yml file.'.format(type(self).__name__))
            logging.info('Example usage in Auth.yml:\n{}:\n  webhook: https://hooks.slack.com/services/123/456/789/'.format(type(self).__name__))
            raise AuthError

    def post_message_to_slack(self, text):
        blob = {'text': text}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        result = requests.post(self.auth['webhook'], data=json.dumps(blob), headers=headers)
        if result.status_code != 200:
            return False
        else:
            return True

    def action_report_log(self):
        return self.post_message_to_slack(self.context.log_msg)


