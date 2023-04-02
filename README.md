# Information Retrieval System of Towards Data Science



- before start:
`pip install -r requirements.txt`

## Components

### Web Application 

- usage: `python ./web_app/manage.py runserver`

in progress





### Simple Crawler
- crawling website: [Towards Data Science](https://towardsdatascience.com/) posts(articles) 
read from sitemap.xml and for each post saving title 
and content in `<p>...</p>` by using simple xpath expressions

- usage: `python main_crawler.py`
- or with custom parameters:
```
usage: main.py [-h] [-u MAIN_SITE_URL] [-o OUTPUT_DIR] [-p PREPARED_URLS]

SImple Crawler.

options:
  -h, --help            show this help message and exit
  -u MAIN_SITE_URL, --main_site_url MAIN_SITE_URL
                        main site that contains file robots.txt...
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        path to output dir where crawled_data directory is
                        created...
  -p PREPARED_URLS, --prepared_urls PREPARED_URLS
                        crawl prepared urls? True/False
```

- prefetch data from this app on my onedrive: [here](https://onedrive.live.com/?authkey=%21AEi6buOuVgTO4QE&id=8D9B8AAC1B2B5597%2185066&cid=8D9B8AAC1B2B5597)
- extract to "./crawled_data"
- if needed, dataset can be easily extended

- parallelization can be added as well but due to politeness of the crawler is not implemented

### NLTK preprocessor
- usage: `python main_preprocessor.py`
```
usage: main_preprocessor.py [-h] -i INPUT_FILE_PATH [-o MAKE_CSV_ONLY]

preprocessor using NLTK lib

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE_PATH, --input_file_path INPUT_FILE_PATH
  -o MAKE_CSV_ONLY, --make_csv_only MAKE_CSV_ONLY
                        reformat to csv only? True/False

```

### Indexer (inverted index creator)

- usage: `python main_indexer.py`

```
usage: main_indexer.py [-h] -i INPUT_FILE_PATH [-t INDEX_TITLES] [-c INDEX_CONTENTS]

Simple indexer

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE_PATH, --input_file_path INPUT_FILE_PATH
  -t INDEX_TITLES, --index_titles INDEX_TITLES True/False
  -c INDEX_CONTENTS, --index_contents INDEX_CONTENTS True/False
```