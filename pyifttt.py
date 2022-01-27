"""PyIFTTT

Usage:
  itf.py -c config_file
  itf.py (-h | --help)
  itf.py --version

Options:
  -h --help                                 Show this screen.
  -c config_file --config_file=config_gile  Optional Config File that runs through migration, default is import.yml
  --version                                 Show version.

"""
from docopt import docopt
import logging
import os
import yaml
from context import *
from pipeline import *


def main(arguments):
    context = None
    config = {}

    if not os.path.isfile('configs/{}.yml'.format(arguments.get('config_file'))):
        logging.info('[!] Config "{}" not found.'.format(arguments.get('config_file')))

    try:
        with open('configs/{}.yml'.format(arguments.get('config_file')), 'r') as f:
            load_config = yaml.safe_load(f)
        config = {}
        # Load Conditions`
        conditons = []
        for condition in load_config.get('if',{}):
            conditons.append(condition)
        config['conditions'] = conditons
        # actions`
        actions = []
        for action in load_config.get('then', {}):
            actions.append(action)
        config['actions'] = actions
        # else action
        actions_else = []
        for action in load_config.get('else', {}):
            actions_else.append(action)
        config['actions_else'] = actions_else

        if load_config.get('name'):
            config['name'] = load_config.get('name')
        else:
            config['name'] = 'Unnamed'
        context = Context(config)
        with open('auth.yml', 'r') as f:
            config['auth'] = yaml.safe_load(f)
        Pipeline(config, context)

    except Exception as e:
        msg = '[X] - {}'.format(e)
        logging.error(msg, exc_info=True)
        exit(1)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(levelname)s - %(message)s',
        level=logging.INFO,
    )

    logging.getLogger("gnupg").setLevel(logging.WARNING)
    arguments = docopt(__doc__, version='PyIFTTT')
    arguments = {k.replace('-', ''): v for k, v in arguments.items()}
    main(arguments)
