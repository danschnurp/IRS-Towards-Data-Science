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
            # todo print user that it failed
            print(sanitized[0], "failed")
        # The code is performing some preprocessing on the `text_content` and `title` variables before they are added to
        # the index.
        text_content = [i.replace("\n", " ") for i in text_content]
        title = [i.replace("\n", " ") for i in title]
        text_content = [sanitize_for_html_tags(i) for i in text_content]
        title = [sanitize_for_html_tags(i) for i in title]

        url_path = sanitized[0].replace("\n", "")
        title_author = ' '.join(title).split("|")
        title_hash = str(hash(title_author[0]))
        today_date = now().today().date()
        title = preprocessor.filter_common_title_parts_from_towards_data_science(title_author[0])
        author = title_author[1]
        if len(author) > 3:
            author = author[4:-1]
        else:
            author = "ANONYMOUS_AUTHOR"
        text_content = preprocessor. \
            filter_common_sentences_from_towards_data_science(' '.join(text_content))

        original_data = pd.read_csv("preprocessed_data/" + INPUT_DATA,
                                    sep=";", header=0,
                                    low_memory=True)
        preprocessed_data = pd.read_csv("preprocessed_data/preprocessed_" + INPUT_DATA,
                                        sep=";", header=0,
                                        low_memory=True)
        preprocessed_data = preprocessed_data.to_dict()
        original_data = original_data.to_dict()

        del original_data["Unnamed: 0"]

        original_data["hash"][len(original_data) - 1] = title_hash
        original_data["Date"][len(original_data) - 1] = today_date
        original_data["Author"][len(original_data) - 1] = author
        original_data["Link"][len(original_data) - 1] = url_path
        original_data["Title"][len(original_data) - 1] = title
        original_data["Content"][len(original_data) - 1] = text_content

        # pd.DataFrame(data=original_data

        title = preprocessor.preprocess_one_piece_of_text(title)
        text_content = preprocessor.preprocess_one_piece_of_text(text_content)

        del preprocessed_data["Unnamed: 0"]

        preprocessed_data["hash"][len(original_data) - 1] = title_hash
        preprocessed_data["Date"][len(original_data) - 1] = today_date
        preprocessed_data["Author"][len(original_data) - 1] = author
        preprocessed_data["Link"][len(original_data) - 1] = url_path
        preprocessed_data["Title"][len(original_data) - 1] = title
        preprocessed_data["Content"][len(original_data) - 1] = text_content

        original_data = pd.DataFrame(original_data)
        preprocessed_data = pd.DataFrame(preprocessed_data)

        save_original_data(original_data)
        save_preprocessed_data(preprocessed_data)

        save_titles(index_data(preprocessed_data["Title"]))
        save_contents(index_data(preprocessed_data["Content"]))
