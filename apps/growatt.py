from .app import *
import growattServer


class Growatt(App):

    def __init__(self, config, context):
        super(Growatt, self).__init__(config, context)
        self.api = None
        self.user_id = None

    def init_api(self):
        if self.api is None:
            self.api = growattServer.GrowattApi()
            login_response = self.api.login(self.auth['username'], self.auth['password'])
            self.user_id = login_response['user']['id']

    def check_auth_example(self):
        self.context.log('Example usage in Auth.yml:\n{}:\n  username: my_login\n  password: my_password'.format(
            type(self).__name__))

    def check_auth(self):
        self.check_auth_username_password()

    def is_battery_full(self):
        self.init_api()
        plants = self.api.plant_list(self.user_id)
        plant_data = self.api.plant_info(plants['data'][0]['plantId'])
        if plant_data['deviceList'][0]['capacity'] in ('100%', '99%', '98%', '97%'):
            result = True
        else:
            result = False
        self.context.log(
            'If [Growatt: Battery Full - Battery Capacity({}%)] = {}'.format(plant_data['deviceList'][0]['capacity'],
                                                                             result))
        return result

    def is_input_above(self, kw):
        self.init_api()
        plants = self.api.plant_list(self.user_id)
        plant_data = self.api.plant_info(plants['data'][0]['plantId'])
        api_result = self.api.mix_system_status(plant_data['deviceList'][0]['deviceAilas'], plants['data'][0]['plantId'])
        if float(api_result['ppv']) > kw:
            result = True
        else:
            result = False
        self.context.log('If [Growatt: Input Above {}kw ({}kw)] = {}'.format(kw, api_result['ppv'], result))
        return result

    def is_input_below(self, kw):
        self.init_api()
        plants = self.api.plant_list(self.user_id)
        plant_data = self.api.plant_info(plants['data'][0]['plantId'])
        api_result = self.api.mix_system_status(plant_data['deviceList'][0]['deviceAilas'], plants['data'][0]['plantId'])
        if float(api_result['ppv']) < kw:
            result = True
        else:
            result = False
        self.context.log('If [Growatt: Input Below {}kw ({}kw)] = {}'.format(kw, api_result['ppv'], result))
        return result
