#  date: 3. 3. 2023
#  author: Daniel Schnurpfeil
#
import os
import sys
import time

import numpy as np
import pandas as pd

from crawler.utils import make_output_dir


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


def filter_common_title_parts_from_towards_data_science(sentence: str) -> str:
    """
    It takes a sentence as input and returns a sentence with common title parts removed

    :param sentence: the sentence to be filtered
    :type sentence: str
    """
    return sentence.replace("| Towards Data Science", "")


def download_nltk():
    """
    If the venv folder is in the parent directory, and the nltk_data folder is in the venv folder, download the stopwords
    and punkt packages from nltk
    """
    # Checking if the venv folder is in the parent directory.
    if "venv" not in os.listdir("../"):
        raise "NO venv dir found!"
    # Checking if the nltk_data folder is in the venv folder.
    if "nltk_data" not in os.listdir("../venv/"):
        import nltk
        import ssl

        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        # Downloading the stopwords and punkt packages from nltk.
        nltk.download("stopwords", download_dir="../venv/nltk_data")
        nltk.download("punkt", download_dir="../venv/nltk_data")


def preprocess_one_piece_of_text(sentence: str):
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
    filtered_sentence = [w for w in word_tokens if not w in set(stop_words)]

    # Splitting the sentence into words and then stemming each word.
    preprocessed = []
    for word in filtered_sentence:
        preprocessed.append(ps.stem(word))
    return preprocessed


def preprocess_all():
    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))

    # Iterating over the titles and contents array and preprocessing each element.
    for counter, title_author, content, one_id in zip(range(len(ids)), preprocessed_authors, preprocessed_contents, ids):
        if use_progressbar:
            if counter % int((len(preprocessed_authors) / toolbar_width)) == 0:
                sys.stdout.write("-")
                sys.stdout.flush()
        if counter == len(preprocessed_authors):
            break

        ids[counter] = one_id.split(")")[1]

        # Preprocessing the content of the article.
        preprocessed_contents[counter] = preprocess_one_piece_of_text(
            filter_common_sentences_from_towards_data_science(content))

        title_author = filter_common_title_parts_from_towards_data_science(title_author)
        split = title_author.split("|")
        # Removing the "by " and the " " from the author name.
        if len(split) > 2:
            preprocessed_authors[counter] = split[2][4:-1]
        else:
            preprocessed_authors[counter] = "ANONYMOUS_AUTHOR"
            # Preprocessing the title of the article.
        try:
            preprocessed_titles[counter] = preprocess_one_piece_of_text(split[1])
        except IndexError:
            raise "Ups, input data are malformed."

        preprocessed_dates[counter] = split[0]

    sys.stdout.write("]")
    sys.stdout.flush()


def write_output():
    make_output_dir(output_filename="preprocessed_data")
    # Finding the minimum length of the arrays.
    result = pd.DataFrame(data=np.array([ids,
                                         preprocessed_dates,
                                         preprocessed_titles,
                                         preprocessed_contents,
                                         preprocessed_authors
                                         ]).T,
                          columns=["hash", "Date", "Title", "Content", "Author"])
    result.to_csv("./preprocessed_data/preprocessed_" + f_name[7:-3] + "csv", sep=';', encoding='utf-8')


def repair_data():
    # in progress
    with open("../crawler/crawled_data/" + f_name, encoding="utf-8") as f:
        df = f.readlines()
    for i in range(0, len(df), 3):
        if ")" not in df[i] or 10 != len(df[i+1].split("|")[0]) or len(df[i+1]) > len(df[i+2]):
            print(len(df[i+1].split("|")[0]))
            print(i/3, df[i])
            for j in df[i-5:i+5]:
                print(j)
            exit(0)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='preprocessor using NLTK lib')
    parser.add_argument('-i', '--input_file_name',
                        help="filename from ../crawler/crawled_data/", required=True)

    f_name = parser.parse_args().input_file_name

    download_nltk()
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    from nltk.tokenize import word_tokenize

    stop_words = stopwords.words('english')
    ps = PorterStemmer()

    # Reading the csv file and storing it in a dataframe.
    df = pd.read_csv("../crawler/crawled_data/" + f_name, header=None, sep='\0', low_memory=True)

    # Taking the values from the dataframe and storing them in arrays.
    preprocessed_contents = np.squeeze(df.values[2:len(df.values):3])
    preprocessed_authors = np.squeeze(df.values[1:len(df.values):3])
    preprocessed_titles = np.zeros(int(len(df) / 3), dtype=list)
    preprocessed_dates = np.zeros(int(len(df) / 3), dtype=list)

    # Taking the first element of each row and storing it in the ids array.
    ids = df.values[:len(df.values):3]
    ids = np.squeeze(ids)

    print("starting...")
    print("preprocessing:" + " " * 14 + "\\/")

    # The number of steps that the progress bar will have.
    toolbar_width = 25
    use_progressbar = True
    if len(preprocessed_authors) < toolbar_width:
        use_progressbar = False
    t1 = time.time()
    # Preprocessing the data.
    preprocess_all()
    print()
    print("Data preprocessed in", time.time() - t1, "sec")

    # Writing the preprocessed data to a csv file.
    write_output()
