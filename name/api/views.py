from django import http
from django.shortcuts import get_object_or_404

from rest_framework.renderers import JSONRenderer
from . import serializers, stats as statistics
from ..decorators import jsonp
from ..models import Name, Location
from ..utils import filter_names


class JSONResponse(http.HttpResponse):
    """HTTP Response object for returning JSON data."""

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data, renderer_context={'indent': 4})
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def name_json(request, name_id):
    """Returns result of name query in json format."""
    name = get_object_or_404(Name, name_id=name_id)
    data = serializers.NameSerializer(name, context={'request': request})

    return JSONResponse(data.data)


def stats_json(request):
    stats = statistics.NameStatistics()
    data = serializers.NameStatisticsSerializer(stats)
    return JSONResponse(data.data)


@jsonp
def search_json(request):
    """Gets the JSON encoded version of the Names matching
    the query parameters.

    This also provides the endpoint used for autocompletion
    during search.
    """
    names = filter_names(request)

    # If the request is AJAX, then it is most likely for autocompletion,
    # so we will only return first 10 names.
    if request.is_ajax():
        names = names[:10]

    data = serializers.NameSearchSerializer(
        names, many=True, context={'request': request})

    response = JSONResponse(data.data)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'X-Requested-With'

    return response


def locations_json(request):
    """Presents the Locations and related Names serialized into JSON."""
    if request.is_ajax():
        locations = Location.objects.filter(status=0)

        data = serializers.LocationSerializer(
            locations, many=True, context={'request': request})

        return JSONResponse(data.data)
    return http.HttpResponseNotFound()
