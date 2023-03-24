import os
import time

from utils import make_output_dir


def download_nltk():
    """
    If the venv folder is in the parent directory, and the nltk_data folder is in the venv folder, download the stopwords
    and punkt packages from nltk
    """
    # Checking if the venv folder is in the parent directory.
    if "venv" not in os.listdir("./"):
        raise "NO venv dir found!"
    # Checking if the nltk_data folder is in the venv folder.
    if "nltk_data" not in os.listdir("./venv/"):
        import nltk
        import ssl

        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        # Downloading the stopwords and punkt packages from nltk.
        nltk.download("stopwords", download_dir="./venv/nltk_data")
        nltk.download("punkt", download_dir="./venv/nltk_data")


if __name__ == '__main__':
    from preprocessors.nltk_preprocessor import NltkPreprocessor
    import argparse

    parser = argparse.ArgumentParser(description='preprocessor using NLTK lib')
    parser.add_argument('-i', '--input_file_path',
                        required=True)
    parser.add_argument('-o', '--make_csv_only',
                        default=False, type=bool,
                        help='reformat to csv only? True/False')
    args = parser.parse_args()

    # Checking if the venv folder is in the parent directory, and if the nltk_data folder is in the venv folder. If not,
    # it downloads the stopwords and punkt packages from nltk.
    download_nltk()
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer

    stop_words = stopwords.words('english')
    ps = PorterStemmer()

    # Creating an instance of the NltkPreprocessor class.
    preprocessor = NltkPreprocessor(args.input_file_path, stop_words, ps, make_csv_only=args.make_csv_only)

    t1 = time.time()
    print("starting...")
    print("preprocessing:" + " " * 14 + "\\/")
    # Preprocessing the data.
    preprocessor.preprocess_all()
    print()
    print("Data preprocessed in", time.time() - t1, "sec")

    # Writing the preprocessed data to a csv file.
    make_output_dir(output_filename="preprocessed_data")
    preprocessor.write_output()