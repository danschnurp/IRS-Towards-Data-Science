# Simple Crawler
- crawling website: [Towards Data Science](https://towardsdatascience.com/) posts(articles) 
read from sitemap.xml and for each post saving title 
and content in `<p>...</p>` by using simple xpath expressions

- before start:
`pip install -r requirements.txt`
- usage: `python main.py`
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

