import sys

import yaycl

from test_task.lib.yaml_parse import load_jinja_yaml
from test_task.utils.path import conf_dir


yaycl.load_yaml = load_jinja_yaml


class ConfigWrapper(object):
    def __init__(self, dir):
        self.yaycl_config = yaycl.Config(config_dir=dir, extension='.yaml')

    def __getattr__(self, key):
        return getattr(self.yaycl_config, key)

    def __getitem__(self, key):
        return getattr(self.yaycl_config, key)


sys.modules[__name__] = ConfigWrapper(dir=conf_dir)
