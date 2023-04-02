from unittest import TestCase

from indexers.kiv_ir_indexer import index_data


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
        print()
