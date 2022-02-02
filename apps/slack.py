import requests
import json
from .app import *


class Slack(App):

    def check_auth_example(self):
        self.context.log(
            'Example usage in Auth.yml:\n{}:\n'
            '  webhook: https://hooks.slack.com/services/123/456/789/'.format(type(self).__name__))

    def auth_usage(self):
        if not self.config['auth'].get(type(self).__name__, False):
            self.context.log('The {} App requires authorisation. '
                             'Please define [webhook] in your auth.yml file.'.format(type(self).__name__))
            self.check_auth_example()
            raise AuthError
        auth = self.config['auth'].get(type(self).__name__, {})
        if not auth.get('username', False):
            self.context.log('The {} App requires authorisation. '
                             'Please define [webhook] in your auth.yml file.'.format(type(self).__name__))
            self.check_auth_example()
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
