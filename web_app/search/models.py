#  date: 20. 4. 2023
#  author: Daniel Schnurpfeil

import json
import os.path

from django.db import models

# Create your models here.
from indexers.kiv_ir_indexer import save_to_json
from search.apps import SearchConfig


def save_titles(indexed_title):
    save_to_json(indexed_title, "titles.JSON", "indexed_data")


def save_contents(indexed_content):
    save_to_json(indexed_content, "contents.JSON", "indexed_data")


def load_titles():
    with open("indexed_data/titles.JSON") as f:
        return json.loads(f.read())


def load_contents():
    with open("indexed_data/contents.JSON") as f:
        return json.loads(f.read())


def save_preprocessed_data(result):
    result.to_csv(os.path.abspath("preprocessed_data/preprocessed_" + SearchConfig.INPUT_DATA),
                  sep=';', encoding='utf-8')


def save_original_data(result):
    result.to_csv(os.path.abspath("preprocessed_data/" + SearchConfig.INPUT_DATA),
                  sep=';', encoding='utf-8')
