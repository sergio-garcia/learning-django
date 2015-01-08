from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^import/$', views.import_ofx, name='import_ofx'),
)
