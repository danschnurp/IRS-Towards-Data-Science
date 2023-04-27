#  date: 20. 4. 2023
#  author: Daniel Schnurpfeil

from django.shortcuts import render

from search.add_index import _index_url
from search.search import _search_by_query


def index(request):
    results = _search_text(request)
    # displaying the results
    if results is not None and len(results) > 0:
        return render(request, "search/results.html", context={"display_search": True,
                                                               "query": request.GET["search_text"],
                                                               "results": results})
    return render(request, "search/index.html", None)


def indexer(request):
    """
    The function "indexer" is defined and takes a request object as an argument.

    :param request: The `request` parameter in a Django view function is an object that contains information about the
    current HTTP request, such as the user agent, the requested URL, any submitted data, and the user session. It is an
    instance of the `HttpRequest` class. The `request` object is passed as
    """
    #  adds url to indexed sites
    if "index_url" in request.GET.keys():
        indexed = 0
        if len(request.GET["index_url"]) > 0:
            indexed = _index_url(request.GET["index_url"])
        if indexed == 1:
            return render(request, "search/index.html", None)

    results = _search_text(request)
    if len(results) > 0:
        return render(request, "search/results.html", context={"display_search": True,
                                                               "query": request.GET["search_text"],
                                                               "results": results})
    return render(request, "search/indexer.html", context={"display_search": True})


def _search_text(request):
    """
    set parameters such as date range and ty of the search
    :param request: The `request` parameter is an object that represents the HTTP request made by a client to a server. It
    contains information such as the HTTP method used (e.g. GET, POST), the URL requested, any query parameters, headers,
    and the body of the request (if applicable).
    """
    if "search_text" in request.GET.keys():
        if len(request.GET["search_text"]) > 0:
            if "search_by" in request.GET:
                start_date = ""
                end_date = ""
                if "start_date" in request.GET:
                    start_date = request.GET["start_date"]
                if "end_date" in request.GET:
                    end_date = request.GET["end_date"]
                # searches by contents
                if request.GET["search_by"] == "Contents":
                    return _search_by_query(request.GET["search_text"], search_by="Content",
                                            start_date=start_date,
                                            end_date=end_date)
                # searches by titles
                elif request.GET["search_by"] == "Titles":
                    return _search_by_query(request.GET["search_text"],
                                            start_date=start_date,
                                            end_date=end_date)
                # searches by bools (AND)
                elif request.GET["search_by"] == "Bools":
                    return _search_by_query(request.GET["search_text"], search_by_bool=True, start_date=start_date,
                                            end_date=end_date)
                else:
                    return _search_by_query(request.GET["search_text"])

        else:
            return []
    else:
        return []
