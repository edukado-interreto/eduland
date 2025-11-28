#!/bin/bash
./manage.py shell -c 'from wagtail_localize.models import TranslationSource; [ts.update_from_db() for ts in TranslationSource.objects.all().iterator()]'
