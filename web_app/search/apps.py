import pandas as pd
from django.apps import AppConfig

from crawlers.crawler import Crawler

import json


class SearchConfig(AppConfig):
    name = 'search'
    crawler = Crawler(output_dir="")
    print("READING content data")
    original_data = pd.read_csv("preprocessed_data/content2023_04_01_17_10.csv",
                                sep=";", header=0,
                                low_memory=True)
    print("READING indexed contents")
    with open("indexed_data/contents.JSON") as f:
        indexed_contents = json.loads(f.read())
    print("READING indexed titles")
    with open("indexed_data/titles.JSON") as f:
        indexed_titles = json.loads(f.read())

