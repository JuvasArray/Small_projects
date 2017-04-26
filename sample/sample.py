#!/usr/bin/env python
from __future__ import unicode_literals

# Imports for django
import sys
import os
from django.conf.urls import url
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

DEBUG=os.environ.get('DEBUG', 'on')=='on'
SECRET_KEY=os.environ.get('SECRET_KEY', '{{ secret_key }}')
ALLOWED_HOSTS=os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Settings
settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

# Views
def index(request):
	return HttpResponse('Hello Django')

# Urls
urlpatterns=[
	url(r'^$', index, name='index')
	]
	
applicstion=get_wsgi_application()

if __name__=='__main__':
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)
	