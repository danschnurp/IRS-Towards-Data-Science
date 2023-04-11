
from django.shortcuts import render

from search.add_index import _index_another_url
from search.apps import SearchConfig
from search.search import __search


def index(request):
    results = _search_text(request)
    if results is not None and len(results) > 0:
        return render(request, "search/results.html", context={"display_search": True,
                                                               "query": request.GET["search_text"],
                                                               "results": results})
    return render(request, "search/index.html", None)


def indexer(request):
    results = _search_text(request)
    if len(results) > 0:
        return render(request, "search/results.html", context={"display_search": True,
                                                               "query": request.GET["search_text"],
                                                               "results": results})
    _index_another_url(request)
    return render(request, "search/indexer.html", context={"display_search": True})


def _search_text(request):
    if "search_text" in request.GET.keys():
        if len(request.GET["search_text"]) > 0:
            if "search_by" not in request.GET and "start_date" not in request.GET and "end_date" not in request.GET:
                return __search(request.GET["search_text"])
            elif request.GET["search_by"] == "Contents":
                return __search(request.GET["search_text"], search_by=SearchConfig.indexed_contents,
                                start_date=request.GET["start_date"],
                                end_date=request.GET["end_date"])
            else:
                return __search(request.GET["search_text"])

        else:
            return []
    else:
        return []
