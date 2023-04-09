from django.apps import AppConfig

from crawlers.crawler import Crawler


class SearchConfig(AppConfig):
    name = 'search'
    crawler = Crawler(output_dir="")
