# Use an official Python runtime as a parent image
FROM python:3.10


RUN mkdir /usr/local/nltk_data/
RUN mkdir /usr/local/nltk_data/corpora
RUN mkdir /usr/local/nltk_data/corpora/stopwords
RUN wget -O english https://public.am.files.1drv.com/y4mwzxuZK4jxNsKTUPWvUwP5P-u7wIfoN6V7NMaURKIdAXeO1Z_tepSsktej0Ctw-oRkB_K_YqcivixgZb9HPQbmFtv7s0XD4w2GkfVYpLUL35gnq9tdx0kxde_rcqZejKqMRzUMBkJ8MbVFowHzDPjhhkaWmnW4SG2iwAo88zws_PdbWlvSYAE96iVP-DZJalXEPKBJKrlWtW6mwKZ43ZYMsW0yWJqshBc93CRH3zKt6Q?AVOverride=1
RUN mv english usr/local/nltk_data/corpora/stopwords/english

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

RUN wget -O ./indexed_data/contents.JSON https://1drv.ms/u/s!ApdVKxusipuNhZkqFonAK0yak5FT4Q?e=qPla2D
RUN wget -O ./indexed_data/titles.JSON https://1drv.ms/u/s!ApdVKxusipuNhZkpjEkfJJ1MSac3Tg?e=gPsnc4
RUN wget -O ./preprocessed_data/content2023_04_01_17_10.csv https://1drv.ms/u/s!ApdVKxusipuNhZheMwQ5p8jk0JPmYA?e=6snJms
RUN wget -O ./preprocessed_data/preprocessed_content2023_04_01_17_10.csv https://1drv.ms/u/s!ApdVKxusipuNhZhbKM3uVPL1YJ6mWw?e=EYRJei
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
