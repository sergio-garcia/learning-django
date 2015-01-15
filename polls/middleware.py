from threading import local
from django.contrib.sites.models import Site
import os

_locals = local()

def get_current_request():
    return getattr(_locals, 'request', None)

def get_current_site():
    request = get_current_request()
    host = request.get_host()

    try:
        return Site.objects.get(domain__iexact=host)
    except:
        return Site.objects.all()[0]

class GlobalRequestMiddleware(object):
    def process_request(self, request):
        _locals.request = request
