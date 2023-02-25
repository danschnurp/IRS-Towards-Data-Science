#  date: 21. 2. 2023
#  author: Daniel Schnurpfeil


from crawler import Crawler
from utils import make_output_dir

if __name__ == '__main__':
    prepared_output_dir = make_output_dir()
    crawler = Crawler(prepared_output_dir)
    crawler.html_sites = crawler.get_urls_from_sitemap()
    crawler.crawl_all_sites()
