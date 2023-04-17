#  date: 3. 3. 2023
#  author: Daniel Schnurpfeil
#
import sys

import numpy as np
import pandas as pd
from nltk import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def preprocess_query(sentence: str,
                     # Creating a list of stop words and a stemmer.
                     stop_words=stopwords.words('english'),
                     ps=PorterStemmer()):
    # It splits the sentence into words.
    word_tokens = word_tokenize(sentence)
    preprocessed = ""
    # Splitting the sentence into words and then stemming each word.
    for word in word_tokens:
        if word not in stop_words:
            preprocessed_word = ps.stem(word)
            # removing the stop words from the sentence.
            if preprocessed_word not in stop_words:
                preprocessed += preprocessed_word + " "
    return preprocessed


# It takes a list of documents, applies a bunch of preprocessing steps, and returns a list of processed documents
class NltkPreprocessor:

    def __init__(self, f_name, stop_words, ps, make_csv_only=False):

        # Assigning the values of the parameters to the attributes of the class.
        self.f_name, self.stop_words, self.ps = f_name, set(stop_words), ps
        self.make_csv_only = make_csv_only

        if self.f_name != "":
            # Reading the csv file and storing it in a dataframe.
            df = pd.read_csv(self.f_name, header=None, sep='\0', low_memory=True)

            # Taking the values from the dataframe and storing them in arrays.
            self.non_preprocessed_contents = np.squeeze(df.values[2:len(df.values):3])
            self.non_preprocessed_authors = np.squeeze(df.values[1:len(df.values):3])
            # Creating an empty array of lists.
            self.preprocessed_contents = np.zeros(int(len(df) / 3), dtype=list)
            self.preprocessed_authors = np.zeros(int(len(df) / 3), dtype=list)
            self.preprocessed_titles = np.zeros(int(len(df) / 3), dtype=list)
            self.preprocessed_dates = np.zeros(int(len(df) / 3), dtype=list)
            self.preprocessed_links = np.zeros(int(len(df) / 3), dtype=list)

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
        2. Remove stopwords
        3. Stems the words

             and it is extremely SLOW 😑

        :param sentence: the text to be preprocessed
        :type sentence: str
        """
        if self.f_name != "":
            # A progress bar.
            if self.use_progressbar:
                self.counter += 1
                if self.counter % int((len(self.preprocessed_authors) / self.toolbar_width)) == 0:
                    sys.stdout.write("-")
                    sys.stdout.flush()

        # It splits the sentence into words.
        word_tokens = word_tokenize(sentence)
        preprocessed = ""
        # Splitting the sentence into words and then stemming each word.
        for word in word_tokens:
            if word not in self.stop_words:
                preprocessed_word = self.ps.stem(word)
                # removing the stop words from the sentence.
                if preprocessed_word not in self.stop_words:
                    preprocessed += preprocessed_word + " "
        return preprocessed

    @staticmethod
    def preprocess_author(author):
        """
        It takes a list of strings, and if the list has more than two elements, it returns the fourth
        element from the third element of the list

        :param author: The author of the post
        :return: The author's name.
        """
        if len(author) > 3:
            return author[3][4:-1]
        else:
            return "ANONYMOUS_AUTHOR"

    def preprocess_all(self):

        # Removing the first part of the id, which is the number of the post.
        self.ids = [one_id.split(")")[1] for one_id in self.ids]

        # Removing the common title parts from the line.
        self.non_preprocessed_authors = [self.filter_common_title_parts_from_towards_data_science(title_author)
                                         for title_author in self.non_preprocessed_authors]

        # Splitting the date, the title and the author into separate strings.
        self.non_preprocessed_authors = [title_author.split("|")
                                         for title_author in
                                         self.non_preprocessed_authors]
        # Taking the first element of each row and storing it in the self.preprocessed_dates array.
        self.preprocessed_dates = [date[0]
                                   for date in
                                   self.non_preprocessed_authors]
        # Taking the first element of each row and storing it in the self.preprocessed_dates array.
        self.preprocessed_links = [date[1]
                                   for date in
                                   self.non_preprocessed_authors]
        # Taking the author's name from the list of strings that is the author's name, the title and the date.
        self.preprocessed_authors = [self.preprocess_author(author)
                                     for author in
                                     self.non_preprocessed_authors]
        # A progress bar.
        print("preprocessing titles")
        sys.stdout.write("[%s]" % (" " * self.toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (self.toolbar_width + 1))

        # If we only want to make a csv file, we don't need to preprocess the text.
        if self.make_csv_only:
            # Taking the second element of each row and storing it in the self.preprocessed_titles array.
            self.preprocessed_titles = [title[2]
                                        for title in
                                        self.non_preprocessed_authors]
        else:
            # Preprocessing the titles of the posts.
            self.preprocessed_titles = [self.preprocess_one_piece_of_text(title[2])
                                        for title in
                                        self.non_preprocessed_authors]
        # A progress bar.
        sys.stdout.write("]")
        sys.stdout.flush()
        print("\npreprocessing contents")
        sys.stdout.write("[%s]" % (" " * self.toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (self.toolbar_width + 1))
        # If we only want to make a csv file, we don't need to preprocess the text.
        if self.make_csv_only:
            # Filtering out the common sentences from the text.
            self.preprocessed_contents = [self.filter_common_sentences_from_towards_data_science(content)
                                          for content in self.non_preprocessed_contents]
        else:
            # Preprocessing the contents of the posts.
            self.preprocessed_contents = [self.preprocess_one_piece_of_text(
                self.filter_common_sentences_from_towards_data_science(content))
                for content in self.non_preprocessed_contents]
        # A progress bar.
        sys.stdout.write("]")
        sys.stdout.flush()

    def write_output(self):
        """
        It writes the output of the program to a file.
        """
        # Creating a dataframe from the data that we have preprocessed.
        result = pd.DataFrame(data={
            "hash": self.ids,
            "Date": self.preprocessed_dates,
            "Author": self.preprocessed_authors,
            "Link": self.preprocessed_links,
            "Title": self.preprocessed_titles,
            "Content": self.preprocessed_contents
        }
        )
        # Writing the preprocessed data to a csv file.
        preprocessed_label = ""
        if not self.make_csv_only:
            preprocessed_label = "preprocessed_"
        result.to_csv("./preprocessed_data/" + preprocessed_label + self.f_name[-27:-3] + "csv",
                      sep=';', encoding='utf-8')
