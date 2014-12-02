"""
WSGI config for azdkj532 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "azdkj532.settings")

import sys
sys.path.append('/var/www/python/dmhy-catcher/')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
