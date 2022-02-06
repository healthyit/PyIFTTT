import requests
import json
import time
import datetime
from .app import *


class OpenWeather(App):

    def check_auth_example(self):
        self.context.log(
            'Example usage in Auth.yml:\n{}:\n  location: '
            'Sydney, AU-NSW, AU\n  app_id: 1234567890\n  units: metric (optional)'.format(
                type(self).__name__))

    def check_auth(self):
        try:
            self.check_auth_location()
        except AuthError:
            self.context.log('OpenWeather prefers the location as "City, State Code, Country Code" in ISO 3166 format.')
            self.context.log('ISO 3166: https://en.wikipedia.org/wiki/ISO_3166-1')
            self.context.log('Try your address here: https://openweathermap.org/find?')
            raise AuthError
        auth = self.config['auth'].get(type(self).__name__, {})
        if not auth.get('app_id', False):
            self.context.log('OpenWeather needs an app_id for it''s APIs. '
                             'Please add it to you auth.yml. '
                             'You can sign up for a free one here: https://home.openweathermap.org/users/sign_up')
            self.check_auth_example()
            raise AuthError
        return True

    def get_current_weather(self):
        resp = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units={}'.format(self.auth['location'],
                                                                                            self.auth['app_id'],
                                                                                            self.auth.get('units',
                                                                                                          'metric')))
        if resp.status_code == 200:
            return json.loads(resp.text)
        else:
            return {}

    def is_nighttime(self):
        data = self.get_current_weather()
        sunrise_utc_ts = data['sys']['sunrise']
        sunset_utc_ts = data['sys']['sunset']
        now_utc_ts = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        if now_utc_ts < sunrise_utc_ts or now_utc_ts > sunset_utc_ts:
            result = True
        else:
            result = False
        self.context.log(
            'If [OpenWeather: is Nighttime - SunRise({}) < Now({}) < SunSet({})] = {}'.format(App.futs(sunrise_utc_ts),
                                                                                              App.futs(now_utc_ts),
                                                                                              App.futs(sunset_utc_ts),
                                                                                              result))
        return result

    def is_before_nighttime(self, minutes):
        data = self.get_current_weather()
        sunset_utc_ts = data['sys']['sunset']
        now_utc_ts = int(time.mktime(datetime.now().timetuple()))
        x_before_sunset = (sunset_utc_ts - (minutes * 60))
        if now_utc_ts < x_before_sunset:
            result = True
        else:
            result = False
        self.context.log(
            'If [OpenWeather: is Before Nighttime - '
            'Now({}), {} Mins Before SunSet({}), SunSet({})] = {}'.format(App.futs(now_utc_ts),
                                                                   minutes,
                                                                   App.futs(x_before_sunset),
                                                                   App.futs(sunset_utc_ts),
                                                                   result))
        return result

    def is_after_nighttime(self, minutes):
        data = self.get_current_weather()
        sunset_utc_ts = data['sys']['sunset']
        now_utc_ts = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        x_after_sunset = (sunset_utc_ts + (minutes * 60))
        if x_after_sunset < now_utc_ts:
            result = True
        else:
            result = False
        self.context.log(
            'If [OpenWeather: is After Nighttime - '
            'Now({}), {} Mins After({}), SunSet({})] = {}'.format(App.futs(now_utc_ts),
                                                                  minutes,
                                                                  App.futs(x_after_sunset),
                                                                  App.futs(sunset_utc_ts),
                                                                  result))
        return result

    def is_daytime(self):
        data = self.get_current_weather()
        sunrise_utc_ts = data['sys']['sunrise']
        sunset_utc_ts = data['sys']['sunset']
        now_utc_ts = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        if sunrise_utc_ts < now_utc_ts < sunset_utc_ts:
            result = True
        else:
            result = False
        self.context.log(
            'If [OpenWeather: is Daytime - Sunrise({}), Now({}), Sunset({})] = {}'.format(App.futs(sunrise_utc_ts),
                                                                                          App.futs(now_utc_ts),
                                                                                          App.futs(sunset_utc_ts),
                                                                                          result))
        return result

    def is_before_daytime(self, minutes):
        data = self.get_current_weather()
        sunrise_utc_ts = data['sys']['sunrise']
        now_utc_ts = int(time.mktime(datetime.datetime.now().timetuple()))
        sunrise_utc_ts_minus_x = sunrise_utc_ts - (minutes * 60)
        if now_utc_ts < sunrise_utc_ts_minus_x:
            result = True
        else:
            result = False
        self.context.log(
            'If [OpenWeather: is Before Daytime - '
            'Now({}), {} before Sunrise({}), Sunrise({})] = {}'.format(App.futs(now_utc_ts),
                                                                       minutes,
                                                                       App.futs(sunrise_utc_ts_minus_x),
                                                                       App.futs(sunrise_utc_ts),
                                                                       result))
        return result

    def is_after_daytime(self, minutes):
        data = self.get_current_weather()
        sunrise_utc_ts = data['sys']['sunrise']
        now_utc_ts = int(time.mktime(datetime.datetime.now().timetuple()))
        x_after_sunrise_utc_ts = sunrise_utc_ts + (minutes * 60)
        if now_utc_ts > x_after_sunrise_utc_ts:
            result = True
        else:
            result = False
        self.context.log('If [OpenWeather: is after daytime sunrise({}), '
                         '{} after sunrise({}), now({})] = {}'.format(App.futs(sunrise_utc_ts),
                                                                      minutes,
                                                                      App.futs(x_after_sunrise_utc_ts),
                                                                      App.futs(now_utc_ts),
                                                                      result))
        return result

    def is_clear(self, percentage):
        data = self.get_current_weather()
        if data['weather'][0]['id'] == 800 and percentage < 10:
            result = True
        elif data['weather'][0]['id'] == 801 and percentage < 25:
            result = True
        elif data['weather'][0]['id'] == 802 and percentage < 50:
            result = True
        elif data['weather'][0]['id'] == 803 and percentage < 90:
            result = True
        elif percentage < 95:
            result = True
        else:
            result = False
        self.context.log('If [OpenWeather: is_clear by {}% ({})] = {}'.format(percentage, data['weather'][0]['id'],
                                                                              result))
        return result

    def is_overcast(self, percentage):
        data = self.get_current_weather()
        if data['weather'][0]['id'] == 800 and percentage > 90:
            result = True
        elif data['weather'][0]['id'] == 801 and percentage > 75:
            result = True
        elif data['weather'][0]['id'] == 802 and percentage > 50:
            result = True
        elif data['weather'][0]['id'] == 803 and percentage > 10:
            result = True
        elif percentage > 5:
            result = True
        else:
            result = False
        self.context.log('If [OpenWeather: is overcast by {}% ({})] = {}'.format(percentage, data['weather'][0]['id'],
                                                                                 result))
        return result
    
    def is_min_temperature_below_c(self, celsius):
        data = self.get_current_weather()
        if data['main']['temp_min'] < celsius:
            result = True
        else:
            result = False
        self.context.log('If [OpenWeather: Min Temp below {}c ({}c)] = {}'.format(celsius,
                                                                                  data['main']['temp_min'],
                                                                                  result))
        return result
