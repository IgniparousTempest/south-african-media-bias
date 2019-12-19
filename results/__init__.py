import os


def absolute_path(file_name: str) -> str:
    dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir, file_name)
