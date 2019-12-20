import os


def absolute_path(file_name: str) -> str:
    """
    Gets a file path in the results folder, regardless of the working directory.
    i.e. 'iol.json' -> '/projects/project/results/iol.json'
    :param file_name: A file name in the results folder.
    :return: The absolute path.
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir, file_name)
