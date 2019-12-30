import os


def make_dir(dir_):
    # Make file if doesn't exists
    if not os.path.exists(dir_):
        os.makedirs(dir_)


def make_dir_for_file(file):
    """
    Makes directory for file if doesn't exist
    """

    dir_ = os.path.dirname(file)

    # Make file if doesn't exists
    if not os.path.exists(dir_):
        os.makedirs(dir_)
