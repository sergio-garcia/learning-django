from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^import/$', views.import_nfse, name='import_nfse'),
)
