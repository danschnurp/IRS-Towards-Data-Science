#  date: 21. 2. 2023
#  author: Daniel Schnurpfeil
#
from crawler import Crawler
from utils import make_output_dir

if __name__ == '__main__':
    prepared_output_dir = make_output_dir()
    crawler = Crawler(prepared_output_dir,
                      # main_site=
                      # "https://towardsdatascience.com/"
                      # "5-signs-youve-become-an-advanced-pythonista-without-even-realizing-it-2b1dd7ef57f3"
                      )
    crawler.get_sitemap_url()

