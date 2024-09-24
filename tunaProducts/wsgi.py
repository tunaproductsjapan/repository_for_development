"""
WSGI config for tunaProducts project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys #add for local

from django.core.wsgi import get_wsgi_application

sys.path.append(r'C:\Users\hiroa\Documents\tunaProducts') #add for local
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tunaProducts.settings')

application = get_wsgi_application()
