#  date: 21. 2. 2023
#  author: Daniel Schnurpfeil
#
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from crawler import Crawler
from utils import make_output_dir

if __name__ == '__main__':
    prepared_output_dir = make_output_dir()
    crawler = Crawler(prepared_output_dir,
                      # main_site=
                      # "https://towardsdatascience.com/"
                      # "5-signs-youve-become-an-advanced-pythonista-without-even-realizing-it-2b1dd7ef57f3"
                      )
    crawler.html_sites = crawler.get_urls_from_sitemap()
    crawler.crawl_all_sites()
    # print(crawler.crawl_one_site("https://towardsdatascience.com/linear-algebra-cheat-sheet-for-deep-learning-cd67aba4526c"))
#     with ThreadPoolExecutor(max_workers = 8) as execut:
#         pass
#
#
# def do_work(sleep_secs: float, i: int) -> str:
#     time.sleep(sleep_secs)
#     return f"foo-{i}"
#
#
# def do_more_concurrent_work(executor: ThreadPoolExecutor) -> None:
#             results_gen = executor.map(partial(do_work, 1.0), range(10, 20))
#             print("more map results: ", list(results_gen))