import os

import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import pandas as pd


def filter_common_sentences_from_towards_data_science(sentence: str) -> str:
    """
    It takes a sentence as input and returns a sentence with the common sentences removed

    :param sentence: The sentence that we want to filter out the common sentences from
    :type sentence: str
    """
    return sentence.replace("A Medium publication sharing concepts, ideas and codes.", "") \
        .replace("Help Status Writers Blog Careers Privacy Terms About Text to speech", "") \
        .replace("Your home for data science.", "") \
        .replace("Towards Data Science Save", "")


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

    df = pd.read_csv("../crawler/crawled_data/" + f_name, header=None, sep='\0', low_memory=True)

    # Selecting the contents from the dataframe.
    contents = np.squeeze(df.values[df.index % 3 == 2])
    preprocessed_contents = np.zeros_like(contents, dtype=list)

    for index, i in enumerate(contents):
        preprocessed_contents[index] = \
            preprocess_one_piece_of_text(filter_common_sentences_from_towards_data_science(i))
