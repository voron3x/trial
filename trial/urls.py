# coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin

from trial.views import CompareView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', CompareView.as_view(), name='compare_view'),
    url(r'^admin/', include(admin.site.urls)),
)
