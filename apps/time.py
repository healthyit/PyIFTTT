from datetime import datetime
from dateutil import tz
from .app import *


class Time(App):

    def check_auth(self):
        return True

    def is_time_after(self, time):
        now_utc_ts = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = datetime.utcfromtimestamp(now_utc_ts)
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)
        local_time = local.strftime('%H:%M:%S')
        if local_time > time:
            result = True
        else:
            result = False
        self.context.log('If [Time: is time after - now({}), time({})] = {}'.format(local_time, time, result))
        return result

    def is_time_before(self, time):
        now_utc_ts = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = datetime.utcfromtimestamp(now_utc_ts)
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)
        local_time = local.strftime('%H:%M:%S')
        if local_time < time:
            result = True
        else:
            result = False
        self.context.log('If [Time: is time before - now({}), time({})] = {}'.format(local_time, time, result))
        return result
