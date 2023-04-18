import pandas as pd
from django.apps import AppConfig

from crawlers.crawler import Crawler

import json

from main_preprocessor import download_nltk
from preprocessors.nltk_preprocessor import NltkPreprocessor


class SearchConfig(AppConfig):
    name = 'search'
    crawler = Crawler(output_dir="")
    print("READING content data")
    original_data = pd.read_csv("preprocessed_data/content2023_04_01_17_10.csv",
                                sep=";", header=0,
                                low_memory=True)
    preprocessed_data = pd.read_csv("preprocessed_data/preprocessed_content2023_04_01_17_10.csv",
                                    sep=";", header=0,
                                    low_memory=True)
    print("READING indexed contents")
    with open("indexed_data/contents.JSON") as f:
        indexed_contents = json.loads(f.read())
    print("READING indexed titles")
    with open("indexed_data/titles.JSON") as f:
        indexed_titles = json.loads(f.read())

    # Checking if the venv folder is in the parent directory, and if the nltk_data folder is in the venv folder. If not,
    # it downloads the stopwords and punkt packages from nltk.
    download_nltk()
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer

    # Creating a list of stop words and a stemmer.
    stop_words = stopwords.words('english')
    ps = PorterStemmer()

    # Creating an instance of the NltkPreprocessor class.
    preprocessor = NltkPreprocessor("", stop_words, ps, make_csv_only=False)
