# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from board.urls import router
from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    url(r'^api/token/', obtain_auth_token, name='api-token'),
    url(r'^api/', include(router.urls)),
]
