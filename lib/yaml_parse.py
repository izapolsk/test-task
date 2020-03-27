import os

from warnings import warn

import ruamel.yaml as yaml
import yaycl
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.yaml.objects import AnsibleUnicode
from ansible.template import Templar
from lya import AttrDict

EXCLUDE_VARS = ('TERMCAP', )


def load_jinja_yaml(filename, **kwargs):
    loaded_yaml = AttrDict()

    # Find the requested yaml in the yaml dir
    if os.path.exists(filename):
        try:
            dl = DataLoader()
            env_vars = kwargs.get('env', {})
            env_vars.update(os.environ)
            for var in EXCLUDE_VARS:
                if var in env_vars:
                    env_vars.pop(var)
            vars = dict(env=env_vars)
            vars.update(dl.load_from_file(filename))
            loaded_yaml.update(Templar(loader=dl, variables=vars).template(vars, fail_on_undefined=False))
            loaded_yaml.pop('env')
        except Exception as e:
            warn('Unable to parse configuration file at {}'.format(filename), yaycl.ConfigInvalid)
            warn('exception: {}'.format(e))
    return loaded_yaml


def dump_jinja_yaml(filename, data):
    yaml.Dumper.add_representer(AttrDict, lambda dumper, cont: dumper.represent_dict(cont.items()))
    yaml.Dumper.add_representer(AnsibleUnicode, yaml.SafeRepresenter.represent_str)
    yaml.Dumper.add_representer(tuple, yaml.SafeRepresenter.represent_list)
    with open(filename, 'w') as f:
        return yaml.dump(data, f, encoding='utf-8', allow_unicode=True, default_flow_style=False)
