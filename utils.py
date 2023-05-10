#  date: 21. 2. 2023
#  author: Daniel Schnurpfeil
#
import os


def make_output_dir(output_filename="crawled_data", output_dir="./") -> str:
    """
    > This function creates a directory to store the crawled data

    :param output_filename: The name of the file that will be created in the output_dir, defaults to crawled_data (optional)
    :param output_dir: The directory where the output file will be saved, defaults to ./ (optional)
    """
    if output_dir[-1] != "/":
        output_dir += "/"
    output_dir += output_filename
    if os.path.exists(output_dir) and os.path.isdir(output_dir):
        return os.path.abspath(output_dir)
    else:
        os.mkdir(output_dir + output_filename)
        return os.path.abspath(output_dir)
