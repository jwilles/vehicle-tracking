import os


def root_dir():
    return os.path.dirname(os.path.realpath(__file__))


def top_dir():
    return os.sep.join(root_dir().split(os.sep)[:-2])


def data_dir():
    return top_dir() + '/data'