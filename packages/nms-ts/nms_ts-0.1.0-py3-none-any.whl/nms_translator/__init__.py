import pytoml
from pathlib import Path


def get_version():
    path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    pyproject = pytoml.loads(open(str(path)).read())
    return pyproject["tool"]["poetry"]["version"]


__version__ = get_version()
