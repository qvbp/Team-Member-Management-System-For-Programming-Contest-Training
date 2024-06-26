"""
WSGI config for Management_System project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import schedule
import time
from app01.catch_data.cf_catch import cf_crawl_data

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Management_System.settings')

application = get_wsgi_application()


