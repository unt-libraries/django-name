import importlib

import name


def test_versions_match():
    assert name.__version__ == importlib.metadata.version('django-name')
