from time import mktime

import pandas as pd
from django.db.models.functions import Cast
from django.forms import DurationField

from indexers.similarity_ranking import count_cosine_similarity
from preprocessors.html_sanitizer import sanitize_for_html_tags

from django.utils.timezone import now
from django.utils.dateparse import parse_date

from web_app.search.models import load_contents, load_titles
from web_app.towards_data_science.settings import INPUT_DATA


def _search_by_query(query, search_by="Title", start_date="", end_date=""):
    """
    The function takes a query as input and performs a search operation.

    :param query: The query parameter is a string that represents the search query
    """
    if search_by == "Content":
        search_by = load_contents()
    else:
        search_by = load_titles()

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
                       int(mktime(end_date.timetuple()) / 21600. + 1))

    original_data = pd.read_csv("preprocessed_data/" + INPUT_DATA,
                                sep=";", header=0,
                                low_memory=True)

    for i in docs_ids:
        row = original_data.iloc[i]

        if int(mktime(parse_date(row["Date"]).timetuple()) / 21600.) in date_range:
            results.append({"date": row["Date"], "title": row["Title"], "hash": row["hash"],
                            "content": row["Content"][:300] + "...",
                            "author": row["Author"], "link": row["Link"]})
    return results if len(results) > 0 else ["not found"]
