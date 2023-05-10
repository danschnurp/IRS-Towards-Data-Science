from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = 'search'
    indexer_runs = False
    INPUT_DATA = "content2023_04_01_17_10.csv"
