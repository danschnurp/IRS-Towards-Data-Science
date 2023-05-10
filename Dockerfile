# Use an official Python runtime as a parent image
FROM python:3.10


RUN mkdir /usr/local/nltk_data/
RUN mkdir /usr/local/nltk_data/corpora
RUN mkdir /usr/local/nltk_data/corpora/stopwords
COPY ./venv/nltk_data/corpora/stopwords/english /usr/local/nltk_data/corpora/stopwords/english
COPY ./venv/nltk_data/tokenizers/punkt/PY3/english.pickle usr/local/nltk_data/tokenizers/punkt/PY3/english.pickle

WORKDIR /usr/src

# Copy the requirements all
COPY ./requirements.txt .
COPY ./indexers ./indexers
COPY ./preprocessors ./preprocessors
COPY ./crawlers ./crawlers
COPY ./web_app .
COPY ./utils.py .

RUN apt-get update && \
    apt-get install -y wget
RUN mkdir ./indexed_data
RUN mkdir ./preprocessed_data


COPY ./indexed_data/contents.JSON ./indexed_data/contents.JSON
COPY ./indexed_data/titles.JSON ./indexed_data/titles.JSON
COPY ./preprocessed_data/preprocessed_content2023_04_01_17_10.csv ./preprocessed_data/preprocessed_content2023_04_01_17_10.csv
COPY ./preprocessed_data/content2023_04_01_17_10.csv ./preprocessed_data/content2023_04_01_17_10.csv

RUN chmod -R 777  ./indexed_data
RUN chmod -R 777 ./preprocessed_data

RUN rm -rf /var/lib/apt/lists/*

RUN pip install virtualenv

RUN virtualenv ./venv
RUN . ./venv/bin/activate

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt

# Expose port 8081 for the app
EXPOSE 8081

# Run the command to start the Flask application
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8081"]
