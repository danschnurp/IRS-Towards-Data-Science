#  date: 21. 2. 2023
#  author: Daniel Schnurpfeil
#
import os
import sys
import time
from copy import copy

from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
from requests import get


class Crawler:

    def __init__(self, output_dir: str, main_site="https://towardsdatascience.com/", robots_txt="robots.txt"):
        """
        This function initializes the Crawler class by setting the output directory, main site, and robots.txt file.

        :param output_dir: The directory where the scraped data will be stored
        :param main_site: The main site that you want to scrape, defaults to https://towardsdatascience.com/ (optional)
        :param robots_txt: The name of the robots.txt file, defaults to robots.txt (optional)
        """
        self.robots_txt = robots_txt
        self.main_site = main_site
        self.output_dir = output_dir
        self.html_sites = []

    @staticmethod
    def try_request(url) -> str:
        """
        It tries to make a request to the given url, and returns the response

        :param url: The URL to request
        """
        try:
            response = get(url)
        # Checking if the response status code is 429, which means that the server is too busy. If it is, it waits
        #         for the amount of time specified in the Retry-After header.
            if response.status_code == 429:
                time.sleep(int(response.headers["Retry-After"]))
            if response.status_code == 200:
                return response.text
            else:
                print(ConnectionError(response), file=sys.stderr)
                return ""
        except Exception:
            return ""

    def get_robots_txt(self):
        """
        If the robots.txt file exists in the output directory, open it and return the contents. If it doesn't exist, call
        the save_robots() function
        :return: A list of lines from the robots.txt file.
        """
        if self.robots_txt in os.listdir(self.output_dir):
            with open(self.output_dir + "/" + self.robots_txt) as f:
                return f.readlines()
        else:
            return self.save_robots()

    def save_robots(self) -> list:
        """
        This function saves the robots.txt file to the output directory
        :return: The robots.txt list
        """
        robots = self.try_request(self.main_site + self.robots_txt)
        with open(self.output_dir + "/" + self.robots_txt, mode="w") as out_writer:
            out_writer.writelines(copy(robots))
        robots = robots.split("\n")
        return robots

    def check_sitemap_consistency(self, robots: list) -> str:
        """
        It takes a list of strings (robots) and returns a string (sitemap_url) if the main_site is in the list of strings

        :param robots: list of lines of content of robots.txt
        :type robots: list
        :return: The sitemap url
        """
        robots.reverse()
        for i in robots:
            # It checks if the main_site is in the robots.txt file.
            if "Sitemap:" in i and self.main_site in i:
                sitemap_url = i.replace("Sitemap: ", "")
                sitemap_url = sitemap_url.strip()
                return sitemap_url

    def get_urls_from_sitemap_by_xpath(self,
                                       sitemap_url: str,
                                       xpath="//loc[contains(text(),'posts')]"):
        """
        It takes a sitemap URL, downloads the sitemap, parses it, and returns a list of URLs that match the given XPath

        :param sitemap_url: url of sitemap
        :param xpath: The xpath to the element
               that contains the URL, defaults to //loc[contains(text(),'posts')] (optional)
        :return: A list of urls
        """
        urls_from_sitemap = self.try_request(sitemap_url)
        soup = BeautifulSoup(urls_from_sitemap, 'lxml')
        root = fromstring(str(soup.contents[1]))
        sub_sitemap = (root.xpath(xpath))
        return sub_sitemap

    def get_urls_from_sitemap(self):
        """
        > This function gets the urls from a sitemap and saves them to a file
        """
        sitemap_url = self.check_sitemap_consistency(self.get_robots_txt())
        print(sitemap_url)
        sub_sitemaps = self.get_urls_from_sitemap_by_xpath(sitemap_url)

        t1 = time.time()
        # Checking if the file exists, and if it does, it returns the contents of the file.
        with open(self.output_dir + "/urls_to_crawl.txt", mode="a+") as in_file:
            html_sites = in_file.readlines()
        if len(html_sites) > 0:
            self.html_sites = html_sites
            return

        html_sites = []

        # Opening a file, and then writing the urls to the file.
        with open(self.output_dir + "/urls_to_crawl.txt", mode="w", encoding="utf-8") as out_writer:
            # Iterating through the sub_sitemaps, and then getting the urls from the sub_sitemaps.
            for index, sub_sitemap_url in enumerate(sub_sitemaps):
                sites = self.get_urls_from_sitemap_by_xpath(sub_sitemap_url.text,
                                                            xpath="//loc[contains(text(),'" + self.main_site + "')]")
                dates = self.get_urls_from_sitemap_by_xpath(sub_sitemap_url.text,
                                                            xpath="//url[contains(loc/text(),'data')]/lastmod/text()")
                # Iterating through the sites, and then appending the text of the site to the html_sites list.
                for datum, site in zip(dates, sites):
                    html_sites.append(site.text)
                    out_writer.writelines(str(datum + " " + site.text + "\n"))
                    if index % 25 == 0:
                        print("amount prepared urls:", len(html_sites), "elapsed time:", time.time() - t1, "s")
        self.html_sites = html_sites

    def crawl_all_sites(self):
        """
        It crawls all cached the sites.
        """
        # Checking if the list of html sites is empty, and if it is, it raises an exception.

        if "urls_to_crawl.txt" in os.listdir(self.output_dir):
            with open(self.output_dir + "/urls_to_crawl.txt", mode="r+", encoding="utf-8") as reader:
                self.html_sites = reader.readlines()

        if not len(self.html_sites) > 0:
            raise Exception("Empty list with html sites!")
        # creates file with timestamp
        with open(self.output_dir + "/crawled_content" + time.strftime("%Y_%m_%d_%H_%M") + ".txt", mode="a",
                  encoding="utf-8") as out_writer:
            # iterating over cached sites can be parallelized
            for index, site in enumerate(self.html_sites):
                datum, site_url = site.split(" ")
                title, text_content = self.crawl_one_site(site_url)
                if title == "failed":
                    print(site_url, "failed")
                    continue
                print(title)
                text_content = [i.replace("\n", " ") for i in text_content]
                title = [i.replace("\n", " ") for i in title]
                out_writer.writelines(str(index) + ")" + str(hash(' '.join(title))) + "\n")
                out_writer.writelines(datum + "|" + ' '.join(title) + "\n")
                out_writer.writelines(' '.join(text_content) + "\n")

    def crawl_one_site(self, site) -> tuple:
        """
        It takes a site, requests it, parses it, and then prints the title and the text of the paragraphs.
        :param site: the url of the site to be crawled
        """
        site = site.strip()
        print("crawling:", site)
        soup = BeautifulSoup(self.try_request(site), 'lxml')
        try:
            root = fromstring(str(soup.contents[1]))
        except Exception or IndexError:
            return "failed", "no content"
        # gets title and paragraphs
        return root.xpath("//title/text()"), root.xpath("//p/text()")
