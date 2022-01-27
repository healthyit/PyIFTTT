import logging


class AuthError(Exception):
    pass


class App(object):
    def __init__(self, config, context):
        self.config = config
        self.context = context
        self.check_auth()
        self.auth = self.config['auth'].get(type(self).__name__, {})
        # search auth for object

    def check_auth_location(self):
        if not self.config['auth'].get(type(self).__name__, False):
            logging.error('The {} App requires a location. Please define [location] in your auth.yml file.'.format(type(self).__name__))
            logging.info('Example usage in Auth.yml:\n{}:\n  location: Sydney, AU-NSW, AU \n '.format(type(self).__name__))
            raise AuthError
        auth = self.config['auth'].get(type(self).__name__, {})
        if not auth.get('location', False):
            logging.error('The {} App requires a location. Please define [location] in your auth.yml file.'.format(type(self).__name__))
            logging.info('Example usage in Auth.yml:\n{}:\n  location: Sydney, AU-NSW, AU \n '.format(type(self).__name__))
            raise AuthError
        return True

    def check_auth_username_password(self):
        if not self.config['auth'].get(type(self).__name__, False):
            logging.error('The {} App requires authorisation. Please define [username] and [password] in your auth.yml file.'.format(type(self).__name__))
            logging.info('Example usage in Auth.yml:\n{}:\n  username: my_login\n  password: my_password'.format(type(self).__name__))
            raise AuthError
        auth = self.config['auth'].get(type(self).__name__, {})
        if not auth.get('username', False):
            logging.error('The {} App requires authorisation. Please define [username] in your auth.yml file.'.format(type(self).__name__))
            logging.info('Example usage in Auth.yml:\n{}:\n  username: my_login\n  password: my_password'.format(type(self).__name__))
            raise AuthError
        if not auth.get('password', False):
            logging.error('The {} App requires authorisation. Please define [password] in your auth.yml file.'.format(type(self).__name__))
            logging.info('Example usage in Auth.yml:\n{}:\n  username: my_login\n  password: my_password'.format(type(self).__name__))
            raise AuthError
        return True

    def check_auth(self):
        logging.warning('No authorisation defined for {}.'.format(type(self).__name__))
        return True

    def __call__(self, func, context, **kwargs):
        logging.info('[+] Call {}: {}({})'.format(type(self).__name__, func, kwargs))
        if not hasattr(self, func):
            raise AttributeError('Specified fn [{}] does not exist in Class [{}]'.format(func, type(self).__name__))
        result = getattr(self, func)(**kwargs)
        logging.info('    [-] Result: {}'.format(result))
        return result

