import logging
import requests
import json
import time
import datetime

from .app import *

class OpenWeather(App):

    def check_auth(self):
        try:
            self.check_auth_location()
        except AuthError:
            logging.info('OpenWeather prefers the location as "City, State Code, Country Code" in ISO 3166 format.')
            logging.info('ISO 3166: https://en.wikipedia.org/wiki/ISO_3166-1')
            logging.info('Try your address here: https://openweathermap.org/find?')
            raise AuthError
        auth = self.config['auth'].get(type(self).__name__, {})
        if not auth.get('app_id', False):
            logging.info('OpenWeather needs an app_id for it''s APIs. Please add it to you auth.yml. You can sign up for a free one here: https://home.openweathermap.org/users/sign_up')
            logging.info('Example usage in Auth.yml:\n{}:\n  location: Sydney, AU-NSW, AU\n  app_id: 1234567890\n '.format(type(self).__name__))
            raise AuthError
        return True

    def getCurrent(self):
        resp = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(self.auth['location'],self.auth['app_id']))
        if resp.status_code == 200:
            return json.loads(resp.text)
        else:
            return {}

    def is_nighttime(self):
        data = self.getCurrent()
        sunrise_utc_ts = data['sys']['sunrise']
        sunset_utc_ts = data['sys']['sunset']
        now_utc_ts = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        if now_utc_ts < sunrise_utc_ts or now_utc_ts > sunset_utc_ts:
            return True
        else:
            return False

    def is_before_nighttime(self, minutes):
        data = self.getCurrent()
        sunset_utc_ts = data['sys']['sunset']
        now_utc_ts = int(time.mktime(datetime.datetime.now().timetuple()))
        if now_utc_ts < (sunset_utc_ts  - (minutes * 60)):
            return True
        else:
            return False

    def is_after_nighttime(self, minutes):
        data = self.getCurrent()
        sunset_utc_ts = data['sys']['sunset']
        now_utc_ts = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        if (sunset_utc_ts + (minutes * 60)) < now_utc_ts:
            return True
        else:
            return False

    def is_daytime(self):
        data = self.getCurrent()
        sunrise_utc_ts = data['sys']['sunrise']
        sunset_utc_ts = data['sys']['sunset']
        now_utc_ts = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        if sunrise_utc_ts < now_utc_ts < sunset_utc_ts:
            return True
        else:
            return False

    def is_before_daytime(self, minutes):
        data = self.getCurrent()
        sunrise_utc_ts = data['sys']['sunrise']
        now_utc_ts = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        if (now_utc_ts - (minutes * 60)) < sunrise_utc_ts:
            return True
        else:
            return False

    def is_after_daytime(self, minutes):
        data = self.getCurrent()
        sunrise_utc_ts = data['sys']['sunrise']
        now_utc_ts = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        if sunrise_utc_ts < (now_utc_ts + (minutes * 60)):
            return True
        else:
            return False

    def is_clear(self, percentage):
        data = self.getCurrent()
        if data['weather'][0]['id'] == 800 and percentage < 10:
            return True
        elif data['weather'][0]['id'] == 801 and percentage < 25:
            return True
        elif data['weather'][0]['id'] == 802 and percentage < 50:
            return True
        elif data['weather'][0]['id'] == 803 and percentage < 95:
            return True
        elif percentage > 90:
            return True
        else:
            return False

    def is_overcast(self, percentage):
        return not self.is_clear(100-percentage)

