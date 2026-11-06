import logging

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

logger = logging.getLogger(__name__)


def vite_prefix() -> str:
    """Static directory of the Vite build, already hashed with its own manifest."""
    return settings.DJANGO_VITE["default"]["static_url_prefix"].strip("/") + "/"


class StaticFilesStorage(ManifestStaticFilesStorage):
    """
    Hashed file names, so browsers never keep a stale CSS or JS after a deploy.

    A missing file (unnoticed with DEBUG, which ignores the manifest) gives a
    404 for that file instead of a 500 for the whole page.
    """

    manifest_strict = False

    def post_process(self, paths, dry_run=False, **options):
        prefix = vite_prefix()
        paths = {path: v for path, v in paths.items() if not path.startswith(prefix)}
        yield from super().post_process(paths, dry_run, **options)

    def stored_name(self, name):
        if name.startswith(vite_prefix()):
            return name
        try:
            return super().stored_name(name)
        except ValueError:
            logger.warning("Static file not found: %s", name)
            return name
