from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from .search import search

import datetime
import json

POST_PER_PAGE = 15


# Create your views here.
def index(request):
    """
    Index view controller

    :param request: http request object
    :return: rendered page
    """
    return render(request, "search/index.html", None)


def question_search_pagination(request, page):
    """
    Question search with pagination view controller

    :param request: http request object
    :param page: currently selected page
    :return: rendered page
    """
    form = {}
    url_params = request.GET.copy().urlencode()

    # get GET parameters
    search_type = request.GET.get("search_type", None)
    search_text = request.GET.get("search_text", None)

    # define the required search type
    if search_type is None:
        if "search_type" in request.COOKIES:
            search_type = request.COOKIES["search_type"]
        else:
            search_type = "fulltext"

    if search_text is None:
        search_text = ""

    page = page if page > 0 else 1

    # determine filters
    if request.GET.getlist("pages") and request.GET.get("pages", "all") != "all":
        pages = request.GET.getlist("pages")
        form["pages"] = pages

    if request.GET.get("with_answer", None) is not None:
        form["with_answer"] = True

    if request.GET.get("date_range_start", None) and request.GET.get("date_range_end", None):
        date_start_string = request.GET["date_range_start"]
        date_end_string = request.GET["date_range_end"]
        date_start = datetime.datetime.strptime(date_start_string, "%Y-%m-%d")
        date_end = datetime.datetime.strptime(date_end_string, "%Y-%m-%d")
    else:
        date_start = datetime.datetime.now() - datetime.timedelta(days=730)
        date_end = datetime.datetime.now()

    form["date_range_start"] = str(date_start.date())
    form["date_range_end"] = str(date_end.date())

    # pagination settings and feed dict
    pagination_info = {"page_nr": page,
                       "next_page_nr": page + 1,
                       "previous_page_nr": page - 1,
                       "url_params": url_params}

    # render the template
    response = render(request, "search/question_search.html",
                      context={"pagination_info": pagination_info, "display_search": True,
                               "search_text": search_text, "form": form})

    response.set_cookie("search_type", search_type)
    return response


def question_search(request):
    """
    Question search without pagination view controller

    :param request: http request object
    :return: rendered page
    """
    return question_search_pagination(request, 1)


def explore_questions_pagination(request, page):
    """
    Explore question with pagination view controller

    :param request: http request
    :param page: currently selected page
    :return: rendered page
    """
    form = {}
    url_params = request.GET.copy().urlencode()

    # determine which posts should be shown according to selected page
    page = page if page > 0 else 1
    post_start = (page - 1) * POST_PER_PAGE
    post_end = (page * POST_PER_PAGE) + 1

    # determine filters
    if request.GET.getlist("pages") and request.GET.get("pages", "all") != "all":
        pages = request.GET.getlist("pages")
        form["pages"] = pages

    if request.GET.get("with_answer", None) is not None:
        form["with_answer"] = True

    if request.GET.get("date_range_start", None) and request.GET.get("date_range_end", None):
        date_start_string = request.GET["date_range_start"]
        date_end_string = request.GET["date_range_end"]
        date_start = datetime.datetime.strptime(date_start_string, "%Y-%m-%d")
        date_end = datetime.datetime.strptime(date_end_string, "%Y-%m-%d")
    else:
        date_start = datetime.datetime.now() - datetime.timedelta(days=730)
        date_end = datetime.datetime.now()

    form["date_range_start"] = str(date_start.date())
    form["date_range_end"] = str(date_end.date())

    # pagination settings and feed dict
    has_previous = True if page > 1 else False
    has_next = True
    pagination_info = {"has_previous": has_previous, "has_next": has_next, "page_nr": page, "next_page_nr": page + 1,
                       "previous_page_nr": page - 1, "url_params": url_params}

    # render the template
    return render(request, "search/explore_questions.html",
                  context={"pagination_info": pagination_info, "display_search": True, "form": form})


def explore_questions(request):
    """
    Explore question without pagination view controller

    :param request: http request object
    :return: rendered page
    """
    return explore_questions_pagination(request, 1)


def detail(request, post_id, page):
    pass


def question_search_content_loader(request, page=1):

    pass


def explore_questions_content_loader(request, page=1):
    pass
