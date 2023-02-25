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
    if output_filename not in os.listdir(output_dir):
        if output_dir[-1] != "/":
            output_dir += "/"
        os.mkdir(output_dir + output_filename)
    output_dir += output_filename
    return output_dir
