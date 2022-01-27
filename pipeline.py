import logging
import apps


class Pipeline(object):
    def __init__(self, config, context):
        self.config = config
        self.context = context
        if len(self.config['conditions']) < 1:
            logging.info('[+] Conditions not defined, ''if'' dictionary in config required (list of conditions)')
            return
        if len(self.config['actions']) < 1:
            logging.info('[+] Actions not defined, ''then'' dictionary in config required (list of actions)')
            return
        self.context = context

        logging.info('[>] Initializing Pipeline: {}'.format(config.get('name')))

        initialized_objects = {}
        for item in (self.config['conditions'] + self.config['actions'] + self.config['actions_else']):
            if item['app'] not in initialized_objects:
                logging.info('[>] Initializing Step: {}'.format(item['app']))
                cls = getattr(apps, item['app'])
                obj = cls(self.config, self.context)
                initialized_objects[item['app']] = obj

        do_action = False
        for condition in self.config['conditions']:
            do_action = initialized_objects[condition['app']](condition['condition'], self.context, **condition.get('args', {}))
            if not do_action:
                break

        if do_action:
            for action in self.config['actions']:
                result = initialized_objects[action['app']](action['action'], self.context, **action.get('args', {}))
        else:
            for action in self.config['actions_else']:
                result = initialized_objects[action['app']](action['action'], self.context, **action.get('args', {}))

