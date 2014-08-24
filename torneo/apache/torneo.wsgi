import os
import sys
sys.path = ['/var/www/html/torneo'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'torneo.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

