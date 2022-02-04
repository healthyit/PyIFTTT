import logging
from .app import *
from meross_iot.api import MerossHttpClient, UnauthorizedException

# Uses https://github.com/albertogeniola/MerossIot


class Meross(App):

    def check_auth_example(self):
        logging.info('Example usage in Auth.yml:\n{}:\n  username: my_login\n  password: my_password'.format(
            type(self).__name__))

    def check_auth(self):
        self.check_auth_username_password()

    def is_on(self, device_uuid):
        try:
            http_handler = MerossHttpClient(email=self.config['auth']['Meross']['username'],
                                            password=self.config['auth']['Meross']['password'])
            devices = http_handler.list_supported_devices()
            for device in devices:
                if device._uuid == device_uuid:
                    data = device.get_sys_data()
                    if data['all']['digest']['togglex'][0]['onoff'] == 1:
                        self.context.log('If [Meross: Is Device On] [{}]: True'.format(data['all']['digest']['togglex'][0]['onoff']))
                        return True
                    else:
                        self.context.log('If [Meross: Is Device On] [{}]: False'.format(data['all']['digest']['togglex'][0]['onoff']))
                        return False
        except UnauthorizedException as e:
            self.context.log('Error Meross UnauthorizedException: {}'.format(e))
        return False

    def is_off(self, device_uuid):
        try:
            http_handler = MerossHttpClient(email=self.config['auth']['Meross']['username'],
                                            password=self.config['auth']['Meross']['password'])
            devices = http_handler.list_supported_devices()
            for device in devices:
                if device._uuid == device_uuid:
                    data = device.get_sys_data()
                    if data['all']['digest']['togglex'][0]['onoff'] == 1:
                        self.context.log('If [Meross: Is Device Off] [{}]: True'.format(data['all']['digest']['togglex'][0]['onoff']))
                        return False
                    else:
                        self.context.log('If [Meross: Is Device Off] [{}]: False'.format(data['all']['digest']['togglex'][0]['onoff']))
                        return True
        except UnauthorizedException as e:
            self.context.log('Error Meross UnauthorizedException: {}'.format(e))
        return False

    def action_on(self, device_uuid):
        try:
            http_handler = MerossHttpClient(email=self.config['auth']['Meross']['username'],
                                            password=self.config['auth']['Meross']['password'])
            devices = http_handler.list_supported_devices()
            for device in devices:
                if device._uuid == device_uuid:
                    # If the device supports multiple channels, let's play with each one.
                    n_channels = len(device.get_channels())
                    for channel in range(0, n_channels):
                        # Turns the power-plug on
                        print("\nTurning channel %d on..." % channel)
                        device.turn_on_channel(channel)
                    self.context.log('Action [Meross: Action Turn Device On]: Success')
                    return True
            self.context.log('Action [Meross: Action Turn Device On]: Unsuccessful')
        except UnauthorizedException as e:
            self.context.log('Error Meross UnauthorizedException: {}'.format(e))
        return False

    def action_off(self, device_uuid):
        try:
            http_handler = MerossHttpClient(email=self.config['auth']['Meross']['username'],
                                            password=self.config['auth']['Meross']['password'])
            devices = http_handler.list_supported_devices()
            for device in devices:
                if device._uuid == device_uuid:
                    # If the device supports multiple channels, let's play with each one.
                    n_channels = len(device.get_channels())
                    for channel in range(0, n_channels):
                        # Turns the power-plug on
                        print("\nTurning channel %d on..." % channel)
                        device.turn_off_channel(channel)
                    self.context.log('Action [Meross: Action Turn Device Off]: Success')
                    return True
            self.context.log('Action [Meross: Action Turn Device Off]: Unsuccessful')
        except UnauthorizedException as e:
            self.context.log('Error Meross UnauthorizedException: {}'.format(e))
        return False
