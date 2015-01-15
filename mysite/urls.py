from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from polls.api import QuestionResource, ChoiceResource


v1_api = Api(api_name='v1')
v1_api.register(QuestionResource())
v1_api.register(ChoiceResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^banking/', include('banking.urls', namespace="banking")),
    url(r'^notafiscal/', include('notafiscal.urls', namespace="notafiscal")),
    url(r'^admin/', include(admin.site.urls)),

    (r'^api/', include(v1_api.urls)),
)
