from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from .models import Question, Choice


class QuestionResource(ModelResource):
    pass


class ChoiceResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, 'question')

    class Meta:
        queryset = Choice.objects.all()
        resource_name = 'choice'
        filtering = {
            'question': ALL_WITH_RELATIONS
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_schema'), name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/set/(?P<pk_list>\w[\w/;-]*)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_multiple'), name="api_get_multiple"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def determine_format(self, request):
        """
        Used to determine the desired format from the request.format
        attribute.
        """
        if (hasattr(request, 'format') and
                request.format in self._meta.serializer.formats):
            return self._meta.serializer.get_mime_for_format(request.format)
        return super(ChoiceResource, self).determine_format(request)

    def wrap_view(self, view):
        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            request.format = kwargs.pop('format', None)
            wrapped_view = super(ChoiceResource, self).wrap_view(view)
            return wrapped_view(request, *args, **kwargs)
        return wrapper


class QuestionResource(ModelResource):
    class Meta:
        queryset = Question.objects.all()
        resource_name = 'question'

    choices = fields.ToManyField(ChoiceResource, 'choices')

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/choices\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_choices'), name="api_get_choices"),
            url(r"^(?P<resource_name>%s)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_schema'), name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/set/(?P<pk_list>\w[\w/;-]*)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_multiple'), name="api_get_multiple"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def determine_format(self, request):
        if (hasattr(request, 'format') and
                request.format in self._meta.serializer.formats):
            return self._meta.serializer.get_mime_for_format(request.format)
        return super(QuestionResource, self).determine_format(request)

    def wrap_view(self, view):
        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            request.format = kwargs.pop('format', None)
            wrapped_view = super(QuestionResource, self).wrap_view(view)
            return wrapped_view(request, *args, **kwargs)
        return wrapper

    def get_choices(self, request, **kwargs):
        try:
            bundle = self.build_bundle(data={'pk': kwargs['pk']}, request=request)
            obj = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        choice_resource = ChoiceResource()
        return choice_resource.get_list(request, question_id=obj.pk)
