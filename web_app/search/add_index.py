#  date: 20. 4. 2023
#  author: Daniel Schnurpfeil

from re import findall

import pandas as pd
from django.utils.timezone import now

from indexers.kiv_ir_indexer import index_data
from preprocessors.html_sanitizer import sanitize_for_html_tags
from web_app.search.models import save_titles, save_contents, save_original_data, save_preprocessed_data
from web_app.towards_data_science.settings import preprocessor, crawler, INPUT_DATA


def _index_url(url_to_index: str):
    """
    adds url to indexed sites
    :param url_to_index: The parameter `url_to_index` is a string that represents the URL of a webpage that needs to be
    indexed
    """

    sanitized = findall(r"https://towardsdatascience\.com/[a-z\-\d]+", url_to_index)
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
        original_data = pd.read_csv("preprocessed_data/" + INPUT_DATA,
                                    sep=";", header=0,
                                    low_memory=True)
        preprocessed_data = pd.read_csv("preprocessed_data/preprocessed_" + INPUT_DATA,
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
