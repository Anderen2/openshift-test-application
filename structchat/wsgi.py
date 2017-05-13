"""
WSGI config for structchat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "structchat.settings")

import newrelic.agent
newrelic.agent.initialize()
print("Newrelic init #2")

from django.core.wsgi import get_wsgi_application
application = newrelic.agent.WSGIApplicationWrapper(get_wsgi_application())
