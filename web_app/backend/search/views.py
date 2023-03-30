from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse

from .models import ExampleModel
from .serializers import ExampleModelSerializer

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_data(request):
    data = ExampleModel.objects.all()
    if request.method == 'GET':
        serializer = ExampleModelSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)


def index(request):
    """
    Index view controller

    :param request: http request object
    :return: rendered page
    """
    return render(request, "search/index.html", None)


def indexer(request):
    """
    Index view controller

    :param request: http request object
    :return: rendered page
    """
    return render(request, "search/indexer.html", context={"display_search": True})
