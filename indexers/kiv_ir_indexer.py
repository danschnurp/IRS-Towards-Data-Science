#  date: 1. 4. 2023
#  author: Daniel Schnurpfeil

import numpy as np


def index_data(data: list):
    """
    creates inverted index
    :param data: list
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
            advanced_index[key] = {"doc_id": list(unique),
                                   # weighted term frequency
                                   "term_frequency": list(1 + np.log(counts)),
                                   # Calculating the inverse document frequency.
                                   "inverted_doc_frequency": np.log(len(simple_index) / len(unique))}
        # If the word only appears once in the document, it is added to the dictionary with the value 1.
        else:
            advanced_index[key] = {val[0]: 1}

    return advanced_index
