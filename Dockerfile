# Use an official Python runtime as a parent image
FROM python:3.10

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

RUN mkdir ./venv/nltk_data

# Expose port 8080 for the app
EXPOSE 8081

# Run the command to start the Flask application
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8081"]
