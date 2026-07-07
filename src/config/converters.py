from collections.abc import Iterable

from django.conf import settings
from django.urls.converters import StringConverter


def _or(values: Iterable[str]) -> str:
    return "|".join(values)


def _get_public_files_re() -> str:
    r"""
    Format public files as "favicon\.ico|dir/(blank\.svg|choice\.svg)"
    """
    ROOT = settings.PUBLIC_ROOT
    DIRECTORIES = ROOT.walk()  # (0: current_path, 1: directories, 2: files)

    # ['favicon.ico', 'robots.txt']
    root_files = (f for f in next(DIRECTORIES)[2])

    #
    others = (f"{d.relative_to(ROOT)}/({_or(files)})" for d, _, files in DIRECTORIES)
    return rf"^{_or(root_files)}|{_or(others)}$".replace(".", r"\.")


class PublicFilesConverter(StringConverter):
    regex = _get_public_files_re()
