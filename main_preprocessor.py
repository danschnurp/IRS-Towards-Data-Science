#  date: 20. 4. 2023
#  author: Daniel Schnurpfeil

import os
import time

from utils import make_output_dir



if __name__ == '__main__':
    from preprocessors.nltk_preprocessor import NltkPreprocessor, download_nltk
    import argparse

    parser = argparse.ArgumentParser(description='preprocessor using NLTK lib')
    parser.add_argument('-i', '--input_file_path',
                        required=True)
    parser.add_argument('-o', '--make_csv_only',
                        default=False, type=bool,
                        help='reformat to csv only? True/False')
    args = parser.parse_args()

    if not os.path.isfile(args.input_file_path):
        raise "bad input_file_path..."

    # Checking if the venv folder is in the parent directory, and if the nltk_data folder is in the venv folder. If not,
    # it downloads the stopwords and punkt packages from nltk.
    download_nltk()
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer

    # Creating a list of stop words and a stemmer.
    stop_words = stopwords.words('english')
    ps = PorterStemmer()

    # Creating an instance of the NltkPreprocessor class.
    preprocessor = NltkPreprocessor(args.input_file_path, stop_words, ps, make_csv_only=args.make_csv_only)

    t1 = time.time()
    # Preprocessing the data.
    preprocessor.preprocess_all()
    print()
    print("Data preprocessed in", time.time() - t1, "sec")

    # Writing the preprocessed data to a csv file.
    make_output_dir(output_filename="preprocessed_data")
    preprocessor.write_output()
