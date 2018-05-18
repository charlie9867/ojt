"""
WSGI config for hco_test project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
import os, sys
import site

site.addsitedir('/usr/lib64/python3.6/site-packages')

#path = os.path.abspath(__file__+'/../../..')
path = '/opt/hco_test'
#if path not in sys.path
sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hco_test.settings")

application = get_wsgi_application()
