from ._version import __version__


def __getattr__(name):
    # Resolve `main` (the console-script entry point, panoptes:main) lazily:
    # importing it pulls in panoptes.app, which binds the DB engine to
    # PANOPTES_DB_URL. Doing that eagerly here meant a bare `import panoptes`
    # (e.g. pytest importing the package to reach tests/conftest.py) bound the
    # engine before anyone had a chance to set the env var.
    if name == "main":
        from .panoptes import main
        return main
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
