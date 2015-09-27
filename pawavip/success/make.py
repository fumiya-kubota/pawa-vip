import yaml
import os

DIR_PATH = os.path.join('game', 'success')


def flat_dict(k1, v1):
    if not isinstance(v1, dict):
        return {k1: v1}
    if not v1:
        return {k1: ''}
    result = {}
    for k2, v2 in v1.items():
        key = k1 + '.' + k2
        result.update(flat_dict(key, v2))
    return result


def flatten(dictionary):
    result = {}
    for k, v in dictionary.iteritems():
        result.update(flat_dict(k, v))
    return result


def init_parameters(success_name):
    file_path = os.path.join(DIR_PATH, success_name, 'parameters.yaml')
    with open(file_path) as fp:
        print fp
        data = yaml.load(fp)

    file_path = os.path.join('pawavip', 'success', 'parameters.yaml')
    with open(file_path) as fp:
        data.update(yaml.load(fp))

    return flatten(data)
