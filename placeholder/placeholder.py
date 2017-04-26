#!/usr/bin/env python
from __future__ import unicode_literals

import os
import hashlib
import sys

# Imports for django
from django import forms
from django.conf.urls import url
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import etag

# Imports for pillow
from io import BytesIO
from PIL import Image, ImageDraw

# Settings constants
DEBUG=os.environ.get('DEBUG', 'on')=='on'
SECRET_KEY=os.environ.get('SECRET_KEY', 'nk0@o!w)2#l$=!a&*dg9u0qo!w!b!%thk=3rdf$e$rqh&x*d0_')
ALLOWED_HOSTS=os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

BASE_DIR=os.path.dirname(__file__)
TEMPLATES_DIR=os.path.join(BASE_DIR, 'templates')
# Settings configurations
settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
    ),
    
   TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,],
    },
],
    STATICFILES_DIRS=(
        os.path.join(BASE_DIR, 'static'),
    ),
    STATIC_URL='/static/',
)

# Classes
# ImageForm, foms.py
class ImageForm(forms.Form):
	""" Form to validate requested image placeholder """
	width=forms.IntegerField(min_value=1, max_value=2000)
	heigth=forms.IntegerField(min_value=1, max_value=2000)
	def generate(self, image_format='PNG'):
		""" Generate an image of the given type """
		heigth=self.cleaned_data(['heigth'])
		width=form.cleaned_data(['width'])
		key='{}.{}.{}'.format(width, heigth, image_format)
		
		content=cache.get(key)

		if content is None:		
			image=Image.new('RGB', (width, heigth))
			draw=ImageDraw.Draw(image)
		
			text='{}x{}'.format(width, heigth)
			textwidth, textheigth=draw.textsize(text)
			if textwidth<width and textheigth<heigth:
				texttop=(heigth-textheigth)//2
				textleft=(width-textwidth)//2
				draw.text((textleft, texttop), text, fill(255, 255, 255))
			content=BytesIO()
			image.save()
			content.seek(0)
			cache.set(key, content, 60*60)
		return content

				
# Views, views.py
def generate_etag(request, width, heigth):
	content = 'Placeholder: {0} x {1}'.format(width, height)
	return hashlib.sha1(content.encode('utf-8')).hexdigest()

# Placeholder
@etag(generate_etag) 
def placeholder(request, width, heigth):
	form=ImageForm({'heigth': heigth, 'width': width})
	if form.is_valid():
		image=form.generate()
		return HttpResponse(image, content_type='image/png')
	else:
		return HttpResponseBadRequest('Invalid image request')
	
# Index	
def index(request):
	example = reverse('placeholder', kwargs={'width': 50, 'height':50})
	context = {'example': request.build_absolute_uri(example)}
	return render(request, 'home.html', context)
        

# Urls, urls.py
urlpatterns=[
	url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder,
        name='placeholder'),
	url(r'^$', index, name='homepage')
	]
	
applicstion=get_wsgi_application()
if __name__=='__main__':
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)
	
