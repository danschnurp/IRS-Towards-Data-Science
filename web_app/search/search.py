#  date: 20. 4. 2023
#  author: Daniel Schnurpfeil

import pandas as pd
from django.db.models.functions import Cast
from django.forms import DurationField
from django.utils.safestring import mark_safe

from indexers.similarity_ranking import count_cosine_similarity, search_bool

from django.utils.timezone import now
from django.utils.dateparse import parse_date

from web_app.search.models import load_contents, load_titles
from web_app.towards_data_science.settings import INPUT_DATA


def _search_by_query(query, search_by="Title", search_by_bool=False, start_date="", end_date=""):
    """
    searches for data based on a specific search criteria.

    :param query: The search query that the user wants to search for
    :param search_by: This parameter specifies the field to search for the query. The default value
     is "Title", which means the search will be performed on the title of the items.
    :param start_date: start_date is a parameter that specifies the earliest date for the search results
    :param end_date: The end date parameter is used to specify the latest date for which the search results should be
    returned. It is an optional parameter and if not provided, the search results will not be limited by end date
    """

    if search_by == "Content":
        search_by = load_contents()
    else:
        search_by = load_titles()

    if len(start_date) > 0:
        start_date = parse_date(start_date)
    else:
        # sets start-date as 1972 year
        start_date = parse_date('1972-01-01')
    if len(end_date) > 0:
        end_date = parse_date(end_date)
    else:
        end_date = now().today().date()
    # checks validity of range input dates, if it fails set default params
    if Cast(end_date - start_date, output_field=DurationField()).identity[1][1].days < 0:
        start_date = parse_date('1972-01-01')
        end_date = now().today().date()
    if search_by_bool:
        docs_ids = search_bool(query, search_by)
    else:
        docs_ids, _ = count_cosine_similarity(query, search_by, stem_query=True)
    results = []
    # loads the original data to get view results
    original_data = pd.read_csv("preprocessed_data/" + INPUT_DATA,
                                sep=";", header=0,
                                low_memory=True)
    for i in docs_ids:
        row = original_data.iloc[i]
        # checks validity of ranges input dates and result date
        if Cast(parse_date(row["Date"]) - start_date, output_field=DurationField()).identity[1][1].days > 0 > \
                Cast(parse_date(row["Date"]) - end_date, output_field=DurationField()).identity[1][1].days - 1:
            words = query.split(" ")
            words = [word.lower() for word in words if len(word) > 0]
            highlighted_content = ['<mark>' + word_content + '</mark>'
                                   if word_content in words
                                   else word_content
                                   for word_content in row["Content"][:500].split(" ")]
            highlighted_title = ['<mark>' + word_title + '</mark>'
                                 if word_title.lower() in words
                                 else word_title
                                 for word_title in row["Title"].split(" ")]

            results.append({"date": row["Date"], "title": mark_safe(" ".join(highlighted_title) + ""),
                            "hash": row["hash"],
                            # adds first 300 chars of content
                            "content": mark_safe(" ".join(highlighted_content) + "..."),
                            "author": row["Author"], "link": row["Link"]})
    return results[:5] if len(results) > 0 else ["not found"]
