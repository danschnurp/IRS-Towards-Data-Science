from unittest import TestCase

from indexers.kiv_ir_indexer import index_data
from indexers.similarity_ranking import count_cosine_similarity


class Test(TestCase):

    def test_index_data(self):
        data = ["tropical fish include fish found in tropical enviroments",
                "fish live in a sea",
                "tropical fish are popular aquarium fish",
                "fish also live in Czechia",
                "Czechia is a country"]

        indexed_data = index_data(data)

        queries = {"q1": "tropical fish sea",
                   "q2": "tropical fish"}
        count_cosine_similarity(queries["q1"], indexed_data)
        count_cosine_similarity(queries["q2"], indexed_data)
