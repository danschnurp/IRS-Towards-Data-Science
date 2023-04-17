from re import findall
from django.utils.timezone import now

from kiv_ir_indexer import index_data
from preprocessors.html_sanitizer import sanitize_for_html_tags
from web_app.search.apps import SearchConfig


def _index_url(url_to_index: str):
    """
    adds url to indexed sites
    :param url_to_index: The parameter `url_to_index` is a string that represents the URL of a webpage that needs to be
    indexed
    """

    sanitized = findall(r"https://towardsdatascience\.com/[a-z\-\d]+", url_to_index)
    if len(sanitized) == 1:
        title, text_content = SearchConfig.crawler.crawl_one_site(sanitized[0])
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
        title = SearchConfig.preprocessor.filter_common_title_parts_from_towards_data_science(title_author[0])
        author = title_author[1]
        if len(author) > 3:
            author = author[4:-1]
        else:
            author = "ANONYMOUS_AUTHOR"
        text_content = SearchConfig.preprocessor. \
            filter_common_sentences_from_towards_data_science(' '.join(text_content))
        l = SearchConfig.original_data
        l.index  = l.index + 1
        l.loc[-1] = [l.index,
            title_hash,
                  today_date,
                  author,
                  url_path,
                  title,
                  text_content]

        SearchConfig.original_data = l

        title = SearchConfig.preprocessor.preprocess_one_piece_of_text(title)
        text_content = SearchConfig.preprocessor.preprocess_one_piece_of_text(text_content)

        index_data(text_content, SearchConfig.indexed_contents)
        index_data(title, SearchConfig.indexed_titles)
