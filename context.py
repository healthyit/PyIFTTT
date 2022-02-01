class Context(object):
    def __init__(self, config):
        self.config = config
        self.log_msg = 'PyIFTTT Log on {}'.format()

    def log(self, msg):
        self.log_msg = '{}{}  {}'.format(self.log_msg, "\n", msg)
