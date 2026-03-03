from django.conf import settings
from django.http import HttpRequest
from django.views.decorators.cache import cache_page
from django_rsgi.serve import serve_file


def _get_public_files_re():
    """
    Format public files as "favicon\.ico|robots\.txt"
    """
    public_files = (f.name for f in settings.PUBLIC_ROOT.glob("*.*"))
    return r"|".join(f.replace(".", r"\.") for f in public_files)


PUBLIC_FILES_URL = rf"^(?P<filename>{_get_public_files_re()})$"


@cache_page(60 * 60 * 24 * 30)
def public(request: HttpRequest, filename: str):
    return serve_file(request, path=filename, document_root=settings.PUBLIC_ROOT)
