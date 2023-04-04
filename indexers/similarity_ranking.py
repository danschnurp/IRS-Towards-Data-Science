#  date: 4. 4. 2023
#  author: Daniel Schnurpfeil

import numpy as np

from preprocessors.html_sanitizer import sanitize_for_html_tags
from preprocessors.nltk_preprocessor import preprocess_query


def count_cosine_similarity(query: str, indexed_data: dict, stem_query=False):
    """
    counts cosine similarity between query and indexed data
    :param stem_query: T/F
    :param query: string query
    :param indexed_data: advanced dictionary where each term has its tf-idf
    :return: max top 5 best scored documents
    """
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
    return list(sorted_docs.keys())[:5], list(sorted_docs.values())[:5]


