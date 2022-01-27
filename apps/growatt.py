from .app import *
import growattServer

class Growatt(App):

    def __init__(self, config, context):
        super(Growatt, self).__init__(config, context)
        self.api = None
        self.user_id = None

    def init_api(self):
        self.api = growattServer.GrowattApi()
        login_response = self.api.login(self.auth['username'], self.auth['password'])
        self.user_id = login_response['user']['id']

    def auth_usage(self):
        self.check_auth_username_password()

    def is_battery_full(self):
        if self.api is None:
            self.init_api()
        plants = self.api.plant_list(self.user_id)
        plant_data = self.api.plant_info(plants['data'][0]['plantId'])
        if plant_data['deviceList'][0]['capacity'] in ('100%', '99%', '98%','97%'):
            return True
        else:
            return False
        # self.api.plant_list(1041214)
        # self.api.plant_info('795598')

    def is_input_above(self, kw):
        if self.api is None:
            self.init_api()
        plants = self.api.plant_list(self.user_id)
        plant_data = self.api.plant_info(plants['data'][0]['plantId'])
        result = self.api.mix_system_status(plant_data['deviceList'][0]['deviceAilas'], plants['data'][0]['plantId'])
        if float(result['ppv']) > kw:
            return True
        else:
            return False

    def is_input_below(self, kw):
        if self.api is None:
            self.init_api()
        plants = self.api.plant_list(self.user_id)
        plant_data = self.api.plant_info(plants['data'][0]['plantId'])
        result = self.api.mix_system_status(plant_data['deviceList'][0]['deviceAilas'], plants['data'][0]['plantId'])
        if float(result['ppv']) < kw:
            return True
        else:
            return False
