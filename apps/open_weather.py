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
            logging.info('Example usage in Auth.yml:\n{}:\n  location: Sydney, AU-NSW, AU\n  app_id: 1234567890\n  units: metric (optional)'.format(type(self).__name__))
            raise AuthError
        return True

    def getCurrent(self):
        resp = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units={}'.format(self.auth['location'],
                                                                                            self.auth['app_id'],
                                                                                            self.auth.get('units',
                                                                                                          'metric')))
        # {"coord":{"lon":151.2073,"lat":-33.8679},
        # "weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],
        # "base":"stations",
        # "main":{"temp":297.33,"feels_like":298.02,"temp_min":296.52,"temp_max":298.32,"pressure":1014,"humidity":85},
        # "visibility":10000,
        # "wind":{"speed":0.89,"deg":32,"gust":2.68},
        # "rain":{"1h":0.11},
        # "clouds":{"all":36},
        # "dt":1643453131,
        # "sys":{"type":2,"id":2018875,"country":"AU","sunrise":1643397193,"sunset":1643446978},
        # "timezone":39600,"id":2147714,"name":"Sydney","cod":200}
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
            result = True
        else:
            result = False
        self.context.log(
            'If [OpenWeather: is Nighttime - SunRise({}) < Now({}) < SunSet({})] = {}'.format(sunrise_utc_ts,
                                                                                            now_utc_ts,
                                                                                            sunset_utc_ts,
                                                                                            result))
        return result

    def is_before_nighttime(self, minutes):
        data = self.getCurrent()
        sunset_utc_ts = data['sys']['sunset']
        now_utc_ts = int(time.mktime(datetime.datetime.now().timetuple()))
        x_before_sunset = (sunset_utc_ts - (minutes * 60))
        if now_utc_ts < x_before_sunset:
            result = True
        else:
            result = False
        self.context.log(
            'If [OpenWeather: is Before Nighttime - Now({}), {} Mins Before({}), SunSet({})] = {}'.format(now_utc_ts,
                                                                                                        minutes,
                                                                                                        x_before_sunset,
                                                                                                        sunset_utc_ts,
                                                                                                        result))
        return result

    def is_after_nighttime(self, minutes):
        data = self.getCurrent()
        sunset_utc_ts = data['sys']['sunset']
        now_utc_ts = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        x_after_sunset = (sunset_utc_ts + (minutes * 60))
        if x_after_sunset < now_utc_ts:
            result = True
        else:
            result = False
        self.context.log(
            'If [OpenWeather: is After Nighttime - Now({}), {} Mins After({}), SunSet({})] = {}'.format(now_utc_ts,
                                                                                                      minutes,
                                                                                                      x_after_sunset,
                                                                                                      sunset_utc_ts,
                                                                                                      result))
        return result

    def is_daytime(self):
        data = self.getCurrent()
        sunrise_utc_ts = data['sys']['sunrise']
        sunset_utc_ts = data['sys']['sunset']
        now_utc_ts = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        if sunrise_utc_ts < now_utc_ts < sunset_utc_ts:
            result = True
        else:
            result = False
        self.context.log(
            'If [OpenWeather: is Daytime - Sunrise({}), Now({}), Sunset({})] = {}'.format(sunrise_utc_ts, now_utc_ts,
                                                                                          sunset_utc_ts, result))
        return result

    def is_before_daytime(self, minutes):
        data = self.getCurrent()
        sunrise_utc_ts = data['sys']['sunrise']
        now_utc_ts = int(time.mktime(datetime.datetime.now().timetuple()))
        sunrise_utc_ts_minus_x = sunrise_utc_ts - (minutes * 60)
        if now_utc_ts < sunrise_utc_ts_minus_x:
            result = True
        else:
            result = False
        self.context.log(
            'If [OpenWeather: is Before Daytime - Now({}), {} before Sunrise({}), Sunrise({})] = {}'.format(now_utc_ts,
                                                                                                            minutes,
                                                                                                            sunrise_utc_ts_minus_x,
                                                                                                            sunrise_utc_ts))
        return result

    def is_after_daytime(self, minutes):
        data = self.getCurrent()
        sunrise_utc_ts = data['sys']['sunrise']
        now_utc_ts = int(time.mktime(datetime.datetime.now().timetuple()))
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
    
    def is_min_temperature_below_c(self, celsius):
        data = self.getCurrent()
        try:
            if data['main']['temp_min'] < celsius:
                self.context.log('If [OpenWeather: Min Temp Above {}c] [{}]: True'.format(celsius, data['main']['temp_min']))
                return True
            else:
                self.context.log('If [OpenWeather: Min Temp Above {}c] [{}]: False'.format(celsius, data['main']['temp_min']))
                return False
        except Exception as e:
            logging.info(' OpenWeather API Response: {}'.format(data))
            return False


