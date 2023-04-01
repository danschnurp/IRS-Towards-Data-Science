#  date: 3. 3. 2023
#  author: Daniel Schnurpfeil
#
import sys
from copy import copy

import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize


class NltkPreprocessor:

    def __init__(self, f_name, stop_words, ps, make_csv_only=False):

        self.f_name, self.stop_words, self.ps = f_name, stop_words, ps
        self.make_csv_only = make_csv_only

        # Reading the csv file and storing it in a dataframe.
        df = pd.read_csv(self.f_name, header=None, sep='\0', low_memory=True)

        # Taking the values from the dataframe and storing them in arrays.
        self.non_preprocessed_contents = np.squeeze(df.values[2:len(df.values):3])
        self.non_preprocessed_authors = np.squeeze(df.values[1:len(df.values):3])
        self.preprocessed_contents = np.zeros(int(len(df) / 3), dtype=list)
        self.preprocessed_authors = np.zeros(int(len(df) / 3), dtype=list)
        self.preprocessed_titles = np.zeros(int(len(df) / 3), dtype=list)
        self.preprocessed_dates = np.zeros(int(len(df) / 3), dtype=list)

        # Taking the first element of each row and storing it in the self.ids array.
        self.ids = df.values[:len(df.values):3]
        self.ids = np.squeeze(self.ids)

        # The number of steps that the progress bar will have.
        self.toolbar_width = 25
        self.use_progressbar = True
        self.counter = 0
        if len(self.preprocessed_authors) < self.toolbar_width:
            self.use_progressbar = False

    @staticmethod
    def filter_common_sentences_from_towards_data_science(sentence: str) -> str:
        """
        It takes a sentence as input and returns a sentence with the common sentences removed
    
        :param sentence: The sentence that we want to filter out the common sentences from
        :type sentence: str
        """
        return sentence.replace("A Medium publication sharing concepts, ideas and codes.", "") \
            .replace("Help Status Writers Blog Careers Privacy Terms About Text to speech", "") \
            .replace("Your home for data science.", "") \
            .replace("Towards Data Science Save", "") \
            .replace("Towards Data Science Member-only", "")

    @staticmethod
    def filter_common_title_parts_from_towards_data_science(sentence: str) -> str:
        """
        It takes a sentence as input and returns a sentence with common title parts removed

        :param sentence: the sentence to be filtered
        :type sentence: str
        """
        return sentence.replace("| Towards Data Science", "")

    def preprocess_one_piece_of_text(self, sentence: str):
        """
        1. Tokenize the sentence into words
        2. Remove stop words
        3. Stem the words
        4. Join the words back into a sentence

        and it is extremely SLOW 😑
    
        :param sentence: the text you want to preprocess
        :type sentence: str
        """

        if self.use_progressbar:
            self.counter += 1
            if self.counter % int((len(self.preprocessed_authors) / self.toolbar_width)) == 0:
                sys.stdout.write("-")
                sys.stdout.flush()

        word_tokens = word_tokenize(sentence)
        # removing the stop words from the sentence.
        filtered_sentence = list(filter(lambda item: item not in self.stop_words, word_tokens))
        # Splitting the sentence into words and then stemming each word.
        preprocessed = [self.ps.stem(word) for word in filtered_sentence]
        return preprocessed

    @staticmethod
    def preprocess_author(author):
        if len(author) > 2:
            return author[2][4:-1]
        else:
            return "ANONYMOUS_AUTHOR"

    def preprocess_all(self):

        self.ids = [one_id.split(")")[1] for one_id in self.ids]

        self.non_preprocessed_authors = [self.filter_common_title_parts_from_towards_data_science(title_author)
                                         for title_author in self.non_preprocessed_authors]

        self.non_preprocessed_authors = [title_author.split("|")
                                         for title_author in
                                         self.non_preprocessed_authors]
        self.preprocessed_dates = [date[0]
                                   for date in
                                   self.non_preprocessed_authors]
        self.preprocessed_authors = [self.preprocess_author(author)
                                     for author in
                                     self.non_preprocessed_authors]
        print("preprocessing titles")
        sys.stdout.write("[%s]" % (" " * self.toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (self.toolbar_width + 1))
        if self.make_csv_only:
            self.preprocessed_titles = [title[1]
                                        for title in
                                        self.non_preprocessed_authors]
        else:
            self.preprocessed_titles = [self.preprocess_one_piece_of_text(title[1])
                                        for title in
                                        self.non_preprocessed_authors]
        sys.stdout.write("]")
        sys.stdout.flush()
        print("\npreprocessing contents")
        sys.stdout.write("[%s]" % (" " * self.toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (self.toolbar_width + 1))
        if self.make_csv_only:
            self.preprocessed_contents = [self.filter_common_sentences_from_towards_data_science(content)
                                          for content in self.non_preprocessed_contents]
        else:
            self.preprocessed_contents = [self.preprocess_one_piece_of_text(
                self.filter_common_sentences_from_towards_data_science(content))
                for content in self.non_preprocessed_contents]
        sys.stdout.write("]")
        sys.stdout.flush()

    def write_output(self):

        result = pd.DataFrame(data={"hash": self.ids,
                                    "Date": self.preprocessed_dates,
                                    "Title": self.preprocessed_titles,
                                    "Content": self.preprocessed_contents,
                                    "Author": self.preprocessed_authors}
                                             )
        preprocessed_label = ""
        if not self.make_csv_only:
            preprocessed_label = "preprocessed_"
        result.to_csv("./preprocessed_data/" + preprocessed_label + self.f_name[-27:-3] + "csv",
                      sep=';', encoding='utf-8')
