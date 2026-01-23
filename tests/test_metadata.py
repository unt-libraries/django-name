import pathlib
import re
import tomli


def test_versions_match():
    pyproject_path = pathlib.Path(__file__).resolve().parents[1] / "pyproject.toml"
    init_path = pathlib.Path(__file__).resolve().parents[1] / 'name' / '__init__.py'

    with open(pyproject_path, "rb") as f:
        pyproject = tomli.load(f)
    with open(init_path, 'r') as f:
        app_version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                                f.read(), re.MULTILINE).group(1)

    pyproject_version = pyproject["project"]["version"]
    assert pyproject_version == app_version
