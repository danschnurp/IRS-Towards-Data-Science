from time import mktime

from django.db.models.functions import Cast
from django.forms import DurationField

from indexers.similarity_ranking import count_cosine_similarity
from preprocessors.html_sanitizer import sanitize_for_html_tags
from web_app.search.apps import SearchConfig

from django.utils.timezone import now
from django.utils.dateparse import parse_date


def __search(query, search_by=SearchConfig.indexed_titles, start_date="", end_date=""):
    """
    The function takes a query as input and performs a search operation.

    :param query: The query parameter is a string that represents the search query
    """

    if len(start_date) > 0:
        start_date = parse_date(start_date)
    else:
        start_date = parse_date('1972-01-01')
    if len(end_date) > 0:
        end_date = parse_date(end_date)
    else:
        end_date = now().today().date()
    if Cast(start_date - end_date, output_field=DurationField()).identity[1][1].days > 0:
        start_date = parse_date('1900-01-01')
        end_date = now().today().date()

    query = sanitize_for_html_tags(query)
    docs_ids, _ = count_cosine_similarity(query, search_by, stem_query=True)
    results = []
    date_range = range(int(mktime(start_date.timetuple()) / 21600.),
                       int(mktime(end_date.timetuple()) / 21600.))
    for i in docs_ids:
        row = SearchConfig.original_data.iloc[i]

        if int(mktime(parse_date(row["Date"]).timetuple()) / 21600.) in date_range:
            results.append({"date": row["Date"], "title": row["Title"], "hash": row["hash"],
                            "content": row["Content"][:300] + "...",
                            "author": row["Author"], "link": row["Link"]})
    return results if len(results) > 0 else ["not found"]
