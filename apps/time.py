from .app import *

class Time(App):

    def check_auth(self):
        return True

    def is_after(self, time):
        return True

    def is_before(self, time):
        return True
