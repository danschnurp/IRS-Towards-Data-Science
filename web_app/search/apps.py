import pandas as pd
from django.apps import AppConfig

from crawlers.crawler import Crawler

import json


class SearchConfig(AppConfig):
    name = 'search'
    crawler = Crawler(output_dir="")

    original_data = pd.read_csv("preprocessed_data/content2023_04_01_17_10.csv",
                                sep=";", header=0,
                                low_memory=True)
    indexed_contents = json.loads("indexed_data/contents.JSON")
    indexed_titles = json.loads("indexed_data/titles.JSON")

