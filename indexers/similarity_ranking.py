#  date: 4. 4. 2023
#  author: Daniel Schnurpfeil

import numpy as np

from preprocessors.html_sanitizer import sanitize_for_html_tags
from preprocessors.nltk_preprocessor import preprocess_query


def search_bool(query: str, indexed_data: dict):
    """
    This function takes a query string and a dictionary of indexed data as input and returns a doc ids containing all words

    :param query: A string representing the search query that the user wants to perform
    :type query: str
    :param indexed_data: indexed_data is a dictionary that contains the indexed data that we want to search through
    :type indexed_data: dict
    """
    # safety input check
    query = sanitize_for_html_tags(query)
    query = preprocess_query(query)
    words = query.split(" ")
    postings = []
    results = []
    # gets relevant postings
    for word in words:
        if word in indexed_data:
            postings.append(indexed_data[word])
    for posting in postings:
        results += posting["doc_id"]
    results = np.array(results)
    unique, counts = np.unique(np.squeeze(results), return_counts=True)
    results = unique[counts > 1]
    return results


def count_cosine_similarity(query: str, indexed_data: dict, stem_query=False):
    """
    This function takes a query string and a dictionary of indexed data, and calculates the cosine similarity between the
    query and each indexed data.

    :param query: A string representing the query for which cosine similarity needs to be calculated
    :type query: str
    :param indexed_data: The indexed_data parameter is a dictionary that contains the preprocessed and indexed data that we
    want to search through
    :type indexed_data: dict
    :param stem_query: A boolean flag indicating whether to stem the query before calculating cosine similarity
    defaults to False (optional)
    """
    # safety input check
    query = sanitize_for_html_tags(query)
    if stem_query:
        query = preprocess_query(query)
    words = query.split(" ")
    postings = []
    scores = {}
    # gets relevant postings
    for word in words:
        if word in indexed_data:
            postings.append(indexed_data[word])
    # grouping by documents and extracts tf-idf
    for posting in postings:
        for doc_id, tf_idf in zip(posting["doc_id"], posting["tf-idf"]):
            if doc_id not in scores.keys():
                scores[doc_id] = [tf_idf]
            else:
                scores[doc_id].append(tf_idf)
    # counts cosine similarity
    for i in scores:
        # debug printing
        # print(i, np.sum(scores[i]) / len(scores[i]), np.sum(scores[i]) / np.sum(np.square(scores[i])))
        scores[i] = np.sum(scores[i]) / np.sum(np.square(scores[i]))
    # sorting
    sorted_docs = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}
    return list(sorted_docs.keys())[:100], list(sorted_docs.values())[:100]
