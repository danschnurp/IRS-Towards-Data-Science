from unittest import TestCase

import pandas as pd

from indexers.kiv_ir_indexer import index_data
from indexers.similarity_ranking import count_cosine_similarity


class Test(TestCase):

    def setUp(self) -> None:
        """
        This function sets up data for testing by reading preprocessed and original data files and storing relevant
        columns in variables.
        """
        super().setUp()
        self.df = pd.read_csv("../preprocessed_data/preprocessed_content2023_04_01_17_10.csv",
                              sep=";", header=0,
                              low_memory=True)
        self.original = pd.read_csv("../preprocessed_data/content2023_04_01_17_10.csv",
                                    sep=";", header=0,
                                    low_memory=True)
        self.titles = self.original["Title"]
        self.contents = self.original["Content"]

    def tearDown(self) -> None:
        """
        This function prints information about documents, titles, and content.
        """
        super().tearDown()
        print(self.docs)
        print("QUERY:", self.queries["q1"])
        for i in range(len(self.docs)):
            print("TITLE:\t", self.titles[self.docs[i]])
            print("content:\t\t", self.contents[self.docs[i]][:150], "\n")

    def test_index_data(self):
        """
        The function tests the cosine similarity calculation of indexed data for given queries.
        """
        data = ["tropical fish include fish found in tropical environments",
                "fish live in a sea",
                "tropical fish are popular aquarium fish",
                "fish also live in Czechia",
                "Czechia is a country"]

        indexed_data = index_data(data)

        queries = {"q1": "tropical fish sea",
                   "q2": "tropical fish"}
        print(count_cosine_similarity(queries["q1"], indexed_data))
        print(count_cosine_similarity(queries["q2"], indexed_data))

    def test_performance_titles(self):
        """
        This function tests the performance of a cosine similarity algorithm on a given query and a dataset of titles.
        """
        self.queries = {"q1": "best programming language for Machine Learning"}
        self.docs, self.scores = count_cosine_similarity(self.queries["q1"], index_data(self.df["Title"]))

    def test_performance_contents(self):
        """
        The function tests the performance of counting cosine similarity between a query and a set of documents.
        """
        self.queries = {"q1": "cosine similarity"}
        self.docs, self.scores = count_cosine_similarity(self.queries["q1"],
                                                         index_data(self.df["Content"]),
                                                         stem_query=True)
