#  date: 3. 3. 2023
#  author: Daniel Schnurpfeil
#
import sys

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
        self.preprocessed_contents = np.squeeze(df.values[2:len(df.values):3])
        self.preprocessed_authors = np.squeeze(df.values[1:len(df.values):3])
        self.preprocessed_titles = np.zeros(int(len(df) / 3), dtype=list)
        self.preprocessed_dates = np.zeros(int(len(df) / 3), dtype=list)

        # Taking the first element of each row and storing it in the self.ids array.
        self.ids = df.values[:len(df.values):3]
        self.ids = np.squeeze(self.ids)

        # The number of steps that the progress bar will have.
        self.toolbar_width = 25
        self.use_progressbar = True
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
    
        :param sentence: the text you want to preprocess
        :type sentence: str
        """

        word_tokens = word_tokenize(sentence)

        # A list comprehension that is removing the stop words from the sentence.
        filtered_sentence = [w for w in word_tokens if not w in set(self.stop_words)]

        # Splitting the sentence into words and then stemming each word.
        preprocessed = []
        for word in filtered_sentence:
            preprocessed.append(self.ps.stem(word))
        return preprocessed

    def preprocess_all(self):
        # setup toolbar
        sys.stdout.write("[%s]" % (" " * self.toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (self.toolbar_width + 1))

        # Iterating over the titles and contents array and preprocessing each element.
        for counter, title_author, content, one_id in zip(range(len(self.ids)), self.preprocessed_authors,
                                                          self.preprocessed_contents,
                                                          self.ids):
            if self.use_progressbar:
                if counter % int((len(self.preprocessed_authors) / self.toolbar_width)) == 0:
                    sys.stdout.write("-")
                    sys.stdout.flush()
            if counter == len(self.preprocessed_authors):
                break

            self.ids[counter] = one_id.split(")")[1]

            # Preprocessing the content of the article.
            if self.make_csv_only:
                self.preprocessed_contents[counter] = self.filter_common_sentences_from_towards_data_science(content)
            else:
                self.preprocessed_contents[counter] = self.preprocess_one_piece_of_text(
                    self.filter_common_sentences_from_towards_data_science(content))

            title_author = self.filter_common_title_parts_from_towards_data_science(title_author)
            split = title_author.split("|")
            # Removing the "by " and the " " from the author name.
            if len(split) > 2:
                self.preprocessed_authors[counter] = split[2][4:-1]
            else:
                self.preprocessed_authors[counter] = "ANONYMOUS_AUTHOR"
                # Preprocessing the title of the article.
            try:
                if self.make_csv_only:
                    self.preprocessed_titles[counter] = split[1]
                else:
                    self.preprocessed_titles[counter] = self.preprocess_one_piece_of_text(split[1])
            except IndexError:
                raise "Ups, input data are malformed."

            self.preprocessed_dates[counter] = split[0]

        sys.stdout.write("]")
        sys.stdout.flush()

    def write_output(self):

        result = pd.DataFrame(data=np.array([self.ids,
                                             self.preprocessed_dates,
                                             self.preprocessed_titles,
                                             self.preprocessed_contents,
                                             self.preprocessed_authors
                                             ]).T,
                              columns=["hash", "Date", "Title", "Content", "Author"])
        preprocessed_label = ""
        if not self.make_csv_only:
            preprocessed_label = "preprocessed_"
        result.to_csv("./preprocessed_data/" + preprocessed_label + self.f_name[-27:-3] + "csv",
                      sep=';', encoding='utf-8')
