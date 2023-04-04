import numpy as np

from preprocessors.html_sanitizer import sanitize_for_html_tags


def count_cosine_similarity(query: str, indexed_data):
    query = sanitize_for_html_tags(query)
    words = query.split(" ")
    postings = []
    scores = {}
    for word in words:
        if word in indexed_data:
            postings.append(indexed_data[word])
        else:
            postings.append(0)
    for posting in postings:
        for doc_id, tf_idf in zip(posting["doc_id"], posting["tf-idf"]):
            if doc_id not in scores.keys():
                scores[doc_id] = [tf_idf]
            else:
                scores[doc_id].append(tf_idf)
    for i in scores:
        # print(i, np.sum(scores[i]) / len(scores[i]), np.sum(scores[i]) / np.sum(np.square(scores[i])))
        scores[i] = np.sum(scores[i]) / np.sum(np.square(scores[i]))
    scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}
    print(scores)

