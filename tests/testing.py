import os


def project_path(*parts):
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), *parts)
