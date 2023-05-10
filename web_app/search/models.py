#  date: 20. 4. 2023
#  author: Daniel Schnurpfeil

import json
import os.path

from django.db.models.functions import Cast
from django.forms import DurationField
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.utils.dateparse import parse_date

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from re import findall

import pandas as pd

from indexers.kiv_ir_indexer import index_data
from preprocessors.html_sanitizer import sanitize_for_html_tags

from indexers.similarity_ranking import count_cosine_similarity, search_bool
from indexers.kiv_ir_indexer import save_to_json

from crawlers.crawler import Crawler
from preprocessors.nltk_preprocessor import NltkPreprocessor

contents_filename = "content2023_04_01_17_10.csv"


def search_by_query(query, search_by="Title", search_by_bool=False, start_date="", end_date=""):
    """
    searches for data based on a specific search criteria.

    :param search_by_bool:
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
    original_data = pd.read_csv("./preprocessed_data/" + contents_filename,
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


def index_url(url_to_index: str):
    """
    adds url to indexed sites
    :param url_to_index: The parameter `url_to_index` is a string that represents the URL of a webpage that needs to be
    indexed
    """

    sanitized = findall(r"https://towardsdatascience\.com/[a-z\-\d]+", url_to_index)

    #  crawls websites and extract data from them.
    crawler = Crawler(output_dir="")

    # Creating a list of stop words and a stemmer.
    stop_words = stopwords.words('english')
    ps = PorterStemmer()

    # Creating an instance of the NltkPreprocessor class.
    preprocessor = NltkPreprocessor("", stop_words, ps, make_csv_only=False)
    
    if len(sanitized) == 1:
        title, text_content = crawler.crawl_one_site(sanitized[0])
        if title == "failed":
            return
        # The code is performing some preprocessing on the `text_content` and `title` variables before they are added to
        # the index.
        text_content = [i.replace("\n", " ") for i in text_content]
        title = [i.replace("\n", " ") for i in title]
        text_content = [sanitize_for_html_tags(i) for i in text_content]
        title = [sanitize_for_html_tags(i) for i in title]
        # preprocessing freshly crawled data
        url_path = sanitized[0].replace("\n", "")
        title_author = ' '.join(title).split("|")
        title_hash = int(hash(' '.join(title)))
        today_date = now().today().date()
        title = preprocessor.filter_common_title_parts_from_towards_data_science(title_author[0])
        author = title_author[1]
        if len(author) > 3:
            author = author[4:-1]
        else:
            author = "ANONYMOUS_AUTHOR"
        text_content = preprocessor. \
            filter_common_sentences_from_towards_data_science(' '.join(text_content))

        # reading indexed dataset
        original_data = pd.read_csv("./preprocessed_data/" + contents_filename,
                                    sep=";", header=0,
                                    low_memory=True)
        preprocessed_data = pd.read_csv("./preprocessed_data/preprocessed_" + contents_filename,
                                        sep=";", header=0,
                                        low_memory=True)
        # converting to dict <- pandas sucks
        preprocessed_data = preprocessed_data.to_dict()
        original_data = original_data.to_dict()
        # dropping index value to avoid reproduction of this column
        del original_data["Unnamed: 0"]

        if title_hash in list(preprocessed_data["hash"].values()):
            return 1

        # inserting data to dataset the "+ 1" adds new entry, and it is quite hack
        original_data["hash"][len(original_data["hash"]) + 1] = title_hash
        original_data["Date"][len(original_data["hash"])] = today_date
        original_data["Author"][len(original_data["hash"])] = author
        original_data["Link"][len(original_data["hash"])] = url_path
        original_data["Title"][len(original_data["hash"])] = title
        original_data["Content"][len(original_data["hash"])] = text_content

        title = preprocessor.preprocess_one_piece_of_text(title)
        text_content = preprocessor.preprocess_one_piece_of_text(text_content)
        # dropping index value to avoid reproduction of this column
        del preprocessed_data["Unnamed: 0"]
        # inserting freshly preprocessed data to dataset
        preprocessed_data["hash"][len(original_data["hash"])] = title_hash
        preprocessed_data["Date"][len(original_data["hash"])] = today_date
        preprocessed_data["Author"][len(original_data["hash"])] = author
        preprocessed_data["Link"][len(original_data["hash"])] = url_path
        preprocessed_data["Title"][len(original_data["hash"])] = title
        preprocessed_data["Content"][len(original_data["hash"])] = text_content

        original_data = pd.DataFrame(original_data)
        preprocessed_data = pd.DataFrame(preprocessed_data)

        save_original_data(original_data)
        save_preprocessed_data(preprocessed_data)
        # update file based index
        save_titles(index_data(preprocessed_data["Title"]))
        save_contents(index_data(preprocessed_data["Content"]))
        return 1


def save_titles(indexed_title):
    save_to_json(indexed_title, "titles.JSON", "./indexed_data")


def save_contents(indexed_content):
    save_to_json(indexed_content, "contents.JSON", "./indexed_data")


def load_titles():
    with open("./indexed_data/titles.JSON") as f:
        return json.load(f)


def load_contents():
    with open("./indexed_data/contents.JSON") as f:
        return json.load(f)


def save_preprocessed_data(result):
    result.to_csv(os.path.abspath("./preprocessed_data/preprocessed_" + contents_filename),
                  sep=';', encoding='utf-8')


def save_original_data(result):
    result.to_csv(os.path.abspath("./preprocessed_data/" + contents_filename),
                  sep=';', encoding='utf-8')
