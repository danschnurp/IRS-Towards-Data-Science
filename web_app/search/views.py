from django.http import HttpResponse
from django.shortcuts import render


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
