#!/usr/bin/env python
from __future__ import unicode_literals

# Imports for django
import sys
from django.conf.urls import url
from django.conf import settings
from django.http import HttpResponse

# Settings
settings.configure(
    DEBUG=True,
    SECRET_KEY='thisisthesecretkey',
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
	
if __name__=='__main__':
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)
	
