"""
RSGI config for config project.

It exposes the RSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://github.com/emmett-framework/granian
"""

import os

from django_rsgi import get_rsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_rsgi_application()
