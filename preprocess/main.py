import os

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

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

sentence = "Towards Data Science Save There are many lingering questions surrounding Covid-19; as time passes, " \
           "we unveil the varied different subgroups. It’s instinctual to try and understand " \
           "science. A Medium publication  Privacy " \
           "Terms About Text to speech "

stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(sentence)

# A list comprehension that is removing the stop words from the sentence.
filtered_sentence = [w for w in word_tokens if not w in stop_words]
print(filtered_sentence)

# Creating an object of the PorterStemmer class.
ps = PorterStemmer()

# Splitting the sentence into words and then stemming each word.
for word in sentence.split():
    print(ps.stem(word))
