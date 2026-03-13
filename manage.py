#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    os.environ.setdefault("DJANGO_RUNSERVER_HIDE_WARNING", "true")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn’t import Django. Is it installed and available?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
