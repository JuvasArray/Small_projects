#!/usr/bin/env python
from __future__ import unicode_literals


import sys
import os
# Imports for django
from django import forms
from django.conf.urls import url
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest
# Imports for pillow
from io import BytesIO
from PIL import Image, ImageDraw

# Settings constants
DEBUG=os.environ.get('DEBUG', 'on')=='on'
SECRET_KEY=os.environ.get('SECRET_KEY', 'nk0@o!w)2#l$=!a&*dg9u0qo!w!b!%thk=3rdf$e$rqh&x*d0_')
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

# Classes
class ImageForm(forms.Form):
	""" Form to validate requested image placeholder """
	width=forms.IntegerField(min_value=1, max_value=2000)
	heigth=forms.IntegerField(min_value=1, max_value=2000)
	def generate(self, image_format='PNG'):
		""" Generate an image of the given type """
		heigth=self.cleaned_data(['heigth'])
		width=form.cleaned_data(['width'])
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
		return content
		

# Views
def placeholder(request, width, heigth):
	form=ImageForm({'heigth': heigth, 'width': width})
	if form.is_valid():
		image=form.generate()
		return HttpResponse(image, content_type='image/png')
	else:
		return HttpResponseBadRequest('Invalid image request')
		

def index(request):
	return HttpResponse('Hello world')

# Urls
urlpatterns=[
	url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder,
        name='placeholder'),
	url(r'^$', index, name='homepage')
	]
	
applicstion=get_wsgi_application()

if __name__=='__main__':
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)
	