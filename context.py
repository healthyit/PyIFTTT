import logging


class Context(object):
    def __init__(self, config):
        self.config = config
        self.log_msg = 'PyIFTTT Log'

    def log(self, msg):
        logging.info(msg)
        self.log_msg = '{}{}  {}'.format(self.log_msg, "\n", msg)
