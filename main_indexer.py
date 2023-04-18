#  date: 1. 4. 2023
#  author: Daniel Schnurpfeil


import os

import pandas as pd

from indexers.kiv_ir_indexer import index_data, save_to_json

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Simple indexer')
    parser.add_argument('-i', '--input_file_path',
                        required=True)
    parser.add_argument('-t', '--index_titles',
                        default=True, type=bool,
                        )
    parser.add_argument('-c', '--index_contents',
                        default=True, type=bool,
                        )
    args = parser.parse_args()

    if not os.path.isfile(args.input_file_path):
        raise "bad input_file_path..."

    df = pd.read_csv(args.input_file_path,
                     sep=";", header=0,
                     low_memory=True)
    if args.index_titles:
        indexed_titles = index_data(df["Title"])
        save_to_json(indexed_titles, "titles.JSON", "indexed_data")
    if args.index_contents:
        indexed_contents = index_data(df["Content"])
        save_to_json(indexed_contents, "contents.JSON", "indexed_data")
