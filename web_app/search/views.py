import re

from django.shortcuts import render
from django.utils.timezone import now

from preprocessors.html_sanitizer import sanitize_for_html_tags
from web_app.search.apps import SearchConfig


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
    if "index_url" in request.GET.keys():
        index_url(request.GET["index_url"])

    return render(request, "search/indexer.html", context={"display_search": True})


def index_url(url_to_index):

    sanitized = re.findall(r"https://towardsdatascience\.com/[a-z\-\d]+", url_to_index)

    if len(sanitized) == 1:

        title, text_content = SearchConfig.crawler.crawl_one_site(sanitized[0])
        if title == "failed":
            print(sanitized[0], "failed")
        text_content = [i.replace("\n", " ") for i in text_content]
        title = [i.replace("\n", " ") for i in title]
        text_content = [sanitize_for_html_tags(i) for i in text_content]
        title = [sanitize_for_html_tags(i) for i in title]
        title = now().today().date() + "|" + sanitized[0].replace("\n", "") + "|" + ' '.join(title) + "\n"
#         todo preprocess and add to index



