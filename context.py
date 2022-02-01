class Context(object):
    def __init__(self, config):
        self.config = config
        self.log_msg = 'PyIFTTT Log'

    def log(self, msg):
        self.log_msg = '{}/n  {}'.format(self.log_msg, msg)
