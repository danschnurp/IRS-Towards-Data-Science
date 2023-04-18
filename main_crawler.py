#  date: 21. 2. 2023
#  author: Daniel Schnurpfeil
from crawlers.crawler import Crawler

from utils import make_output_dir
        
if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='SImple Crawler.')
    parser.add_argument('-u', '--main_site_url',
                        help='main site that contains file robots.txt...',
                        default="https://towardsdatascience.com/")
    parser.add_argument('-o', '--output_dir',
                        default="./crawled_data/",
                        help='path to output dir where crawled_data directory is created...')
    parser.add_argument('-p', '--prepared_urls',
                        default=True, type=bool,
                        help='crawl prepared urls? True/False')
    args = parser.parse_args()

    prepared_output_dir = make_output_dir()
    crawler = Crawler(prepared_output_dir, main_site=args.main_site_url)
    if not args.prepared_urls:
        crawler.get_urls_from_sitemap()
    crawler.crawl_all_sites()
