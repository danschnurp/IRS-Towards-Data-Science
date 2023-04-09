#  date: 1. 4. 2023
#  author: Daniel Schnurpfeil

import numpy as np


def index_data(data: list):
    """
    The function "index_data" takes in a list of data as input.

    :param data: The parameter "data" is a list that contains the data that needs to be indexed
    :type data: list
    """
    simple_index = {}
    advanced_index = {}
    # Creating a dictionary with the words as keys and the indices of the documents as values.
    for index, i in enumerate(data):
        for j in i.split():
            if j not in simple_index:
                simple_index[j] = [index]
            else:
                simple_index[j].append(index)
    # creating a dictionary of dictionaries
    for key, val in zip(simple_index.keys(), simple_index.values()):
        if len(val) > 1:
            # Converting the list to a numpy array and then squeezing it.
            val_numpied = np.squeeze(np.array([val]))

            # Counting the number of times a word appears in a document.
            unique, counts = np.unique(val_numpied, return_counts=True)
            advanced_index[key] = {"doc_id": list(unique.astype(int).astype(object)),
                                   # weighted term frequency
                                   "term_frequency": list((1 + np.log(counts)).astype(int).astype(object)),
                                   # Calculating the inverse document frequency.
                                   "inverted_doc_frequency": [(np.log(len(simple_index) / len(unique))).astype(float).astype(object)],
                                   "tf-idf": list(((1 + np.log(counts)) * np.log(len(simple_index) / len(unique))).astype(float).astype(object))
                                   }
        # If the word only appears once in the document, it is added to the dictionary with the value 1.
        else:
            advanced_index[key] = {"doc_id": [val[0]],
                                   "term_frequency": [(1 + np.log(1)).astype(int).astype(object)],
                                   "inverted_doc_frequency": [np.log(len(simple_index)).astype(float).astype(object)],
                                   "tf-idf": [((1 + np.log(1)) * np.log(len(simple_index))).astype(float).astype(object)]}

    return advanced_index


def save_to_json(advanced_index: dict, name: str):
    """
    This function saves a dictionary object to a JSON file with a specified name.

    :param advanced_index: A dictionary containing advanced indexing information that needs to be saved to a JSON file
    :type advanced_index: dict
    :param name: The `name` parameter is a string that represents the name of the file where the JSON data will be saved
    :type name: str
    """
    from json import dumps
    from utils import make_output_dir

    directory = make_output_dir("indexed_data", output_dir="../")
    with open(directory + "/" + name, mode="w") as out:
        out.write(dumps(advanced_index))
