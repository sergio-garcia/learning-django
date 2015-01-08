from threading import local
from django.contrib.sites.models import Site

_locals = local()

def get_current_request():
    return getattr(_locals, 'request', None)

def get_current_site():
    request = get_current_request()
    host = request.get_host()
    return Site.objects.get(domain__iexact=host)

class GlobalRequestMiddleware(object):
    def process_request(self, request):
        _locals.request = request
