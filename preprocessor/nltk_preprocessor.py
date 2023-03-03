#  date: 3. 3. 2023
#  author: Daniel Schnurpfeil
#
import os
import sys

import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import pandas as pd

from crawler.utils import make_output_dir


def filter_common_sentences_from_towards_data_science(sentence: str) -> str:
    """
    It takes a sentence as input and returns a sentence with the common sentences removed

    :param sentence: The sentence that we want to filter out the common sentences from
    :type sentence: str
    """
    return sentence.replace("A Medium publication sharing concepts, ideas and codes.", "") \
        .replace("Help Status Writers Blog Careers Privacy Terms About Text to speech", "") \
        .replace("Your home for data science.", "") \
        .replace("Towards Data Science Save", "")\
        .replace("Towards Data Science Member-only", "")


def filter_common_title_parts_from_towards_data_science(sentence: str) -> str:
    """
    It takes a sentence as input and returns a sentence with common title parts removed

    :param sentence: the sentence to be filtered
    :type sentence: str
    """
    return sentence.replace("| Towards Data Science", "")


def preprocess_one_piece_of_text(sentence: str):
    # Checking if the venv folder is in the parent directory.
    if "venv" not in os.listdir("../"):
        raise "NO venv dir found!"
    # Checking if the nltk_data folder is in the venv folder.
    if "nltk_data" not in os.listdir("../venv/"):
        import nltk
        import ssl

        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        # Downloading the stopwords and punkt packages from nltk.
        nltk.download("stopwords", download_dir="../venv/nltk_data")
        nltk.download("punkt", download_dir="../venv/nltk_data")

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)

    # A list comprehension that is removing the stop words from the sentence.
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    # print(filtered_sentence)

    # Creating an object of the PorterStemmer class.
    ps = PorterStemmer()

    # Splitting the sentence into words and then stemming each word.
    preprocessed = []
    for word in sentence.split():
        preprocessed.append(ps.stem(word))
    return preprocessed


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='preprocessor using NLTK lib')
    parser.add_argument('-i', '--input_file_name',
                        help="filename from ../crawler/crawled_data/", required=True)

    f_name = parser.parse_args().input_file_name

    # Reading the csv file and storing it in a dataframe.
    df = pd.read_csv("../crawler/crawled_data/" + f_name, header=None, sep='\0', low_memory=True)

    preprocessed_contents = np.zeros(int(len(df) / 3), dtype=list)
    preprocessed_titles = np.zeros(int(len(df) / 3), dtype=list)
    preprocessed_authors = np.zeros(int(len(df) / 3), dtype=list)
    ids = np.zeros(int(len(df) / 3), dtype=int)
    print()
    print("preprocessing:" + " " * 14 + "\\/")

    # The number of steps that the progress bar will have.
    toolbar_width = 25
    use_progressbar = True
    if len(preprocessed_authors) < toolbar_width:
        use_progressbar = False

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))
    counter = 0
    # Iterating over the titles and contents array and preprocessing each element.
    for i in range(0, len(df), 3):
        if use_progressbar:
            if counter % int((len(preprocessed_authors) / toolbar_width)) == 0:
                sys.stdout.write("-")
                sys.stdout.flush()
        if counter == len(preprocessed_authors):
            break

        content = df.values[i+2][0]
        title_author = df.values[i+1][0]
        one_id = df.values[i][0].split(")")
        ids[counter] = one_id[1]
        # Preprocessing the content of the article.
        preprocessed_contents[counter] = preprocess_one_piece_of_text(
                filter_common_sentences_from_towards_data_science(content))

        title_author = filter_common_title_parts_from_towards_data_science(title_author)
        split = title_author.split("|")
        # Removing the "by " and the " " from the author name.
        if len(split) > 1:
            preprocessed_authors[counter] = split[1][4:-1]
        else:
            preprocessed_authors[counter] = "ANONYMOUS_AUTHOR"
            # Preprocessing the title of the article.
        preprocessed_titles[counter] = preprocess_one_piece_of_text(split[0])
        counter += 1

    sys.stdout.write("]")
    sys.stdout.flush()

    make_output_dir(output_filename="preprocessed_data")
    # Finding the minimum length of the arrays.
    size = np.min(np.array([len(ids), len(preprocessed_titles), len(preprocessed_contents), len(preprocessed_authors)]))
    result = pd.DataFrame(data=np.array([ids[:size],
                                         preprocessed_titles[:size],
                                         preprocessed_contents[:size],
                                         preprocessed_authors[:size]
                                         ]).T,
                          columns=["ID", "Title", "Content", "Author"])
    result.to_csv("./preprocessed_data/preprocessed_" + f_name[7:-3] + "csv", sep=';', encoding='utf-8')
