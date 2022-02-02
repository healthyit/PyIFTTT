import logging
from datetime import datetime
from dateutil import tz


class AuthError(Exception):
    pass


class App(object):
    def __init__(self, config, context):
        self.config = config
        self.context = context
        self.check_auth()
        self.auth = self.config['auth'].get(type(self).__name__, {})
        # search auth for object

    def check_auth_example(self):
        logging.info('Example should be defined at a class level : {}'.format(type(self).__name__))

    def check_auth_location(self):
        if not self.config['auth'].get(type(self).__name__, False):
            self.context.log('The {} App requires a location. '
                             'Please define [location] in your auth.yml file.'.format(type(self).__name__))
            self.check_auth_example()
            raise AuthError
        auth = self.config['auth'].get(type(self).__name__, {})
        if not auth.get('location', False):
            self.context.log('The {} App requires a location. '
                             'Please define [location] in your auth.yml file.'.format(type(self).__name__))
            self.check_auth_example()
            raise AuthError
        return True

    def check_auth_username_password(self):
        if not self.config['auth'].get(type(self).__name__, False):
            self.context.log(
                'The {} App requires authorisation. '
                'Please define [username] and [password] in your auth.yml file.'.format(type(self).__name__))
            self.check_auth_example()
            raise AuthError
        auth = self.config['auth'].get(type(self).__name__, {})
        if not auth.get('username', False):
            self.context.log('The {} App requires authorisation. '
                             'Please define [username] in your auth.yml file.'.format(type(self).__name__))
            self.check_auth_example()
            raise AuthError
        if not auth.get('password', False):
            self.context.log('The {} App requires authorisation. '
                             'Please define [password] in your auth.yml file.'.format(type(self).__name__))
            self.check_auth_example()
            raise AuthError
        return True

    @staticmethod
    def futs(uts):
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = datetime.utcfromtimestamp(uts)
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)
        return local.strftime('%Y/%m/%d %H:%M:%S %Z')

    def check_auth(self):
        self.context.log('No authorisation defined for {}.'.format(type(self).__name__))
        return True

    def __call__(self, func, context, **kwargs):
        logging.info('[+] Call {}: {}({})'.format(type(self).__name__, func, kwargs))
        if not hasattr(self, func):
            raise AttributeError('Specified fn [{}] does not exist in Class [{}]'.format(func, type(self).__name__))
        result = getattr(self, func)(**kwargs)
        logging.info('    [-] Result: {}'.format(result))
        return result
