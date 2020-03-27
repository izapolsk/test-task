import os

# todo: replace with getting path of installed module and entry points
repo_dir = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
proj_dir = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
conf_dir = os.path.join(proj_dir, 'conf')
log_dir = os.path.join(proj_dir, 'log')
tmp_dir = os.path.join(proj_dir, 'tmp')
data_dir = os.path.join(proj_dir, 'data')
