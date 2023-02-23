#  date: 21. 2. 2023
#  author: Daniel Schnurpfeil
#
import os
import time
from copy import copy

from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import requests
from requests import Response


# Crawler is a class that crawls a website.
class Crawler:

    def __init__(self, output_dir: str, main_site="https://towardsdatascience.com/", robots_txt="robots.txt"):
        """
        This function initializes the Crawler class by setting the output directory, main site, and robots.txt file.

        :param output_dir: The directory where the scraped data will be stored
        :type output_dir: str
        :param main_site: The main site that you want to scrape, defaults to https://towardsdatascience.com/ (optional)
        :param robots_txt: The name of the robots.txt file, defaults to robots.txt (optional)
        """
        self.robots_txt = robots_txt
        self.main_site = main_site
        self.output_dir = output_dir

    @staticmethod
    def try_request(url) -> Response:
        """
        It tries to make a request to the given url, and returns the response

        :param url: The URL to request
        """
        response = requests.get(url)
        # Checking if the response status code is 429, which means that the server is too busy. If it is, it waits
        #         for the amount of time specified in the Retry-After header.
        if response.status_code == 429:
            time.sleep(int(response.headers["Retry-After"]))
        if response.status_code == 200:
            return response
        else:
            raise ConnectionError

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
        robots = self.try_request(self.main_site + self.robots_txt).text
        with open(self.output_dir + "/" + self.robots_txt, mode="w") as out_writer:
            out_writer.writelines(copy(robots))
        robots = robots.split("\n")
        return robots

    def check_sitemap_consistency(self, robots: list) -> str:
        """
        It takes a list of strings (robots) and returns a string (sitemap_url) if the main_site is in the list of strings

        :param robots: list
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
        soup = BeautifulSoup(urls_from_sitemap.text, 'lxml')
        root = fromstring(str(soup.contents[1]))
        sub_sitemap = (root.xpath(xpath))
        return sub_sitemap

    def get_urls_from_sitemap(self):

        sitemap_url = self.check_sitemap_consistency(self.get_robots_txt())
        print(sitemap_url)
        sub_sitemaps = self.get_urls_from_sitemap_by_xpath(sitemap_url)

        html_sites = []
        t1 = time.time()
        with open(self.output_dir + "/urls_to_crawl.txt", mode="w") as out_writer:
            for index, sub_sitemap_url in enumerate(sub_sitemaps):
                sites = self.get_urls_from_sitemap_by_xpath(sub_sitemap_url.text,
                                                            "//loc[contains(text(),'" + self.main_site + "')]")
                for site in sites:
                    html_sites.append(site.text)
                    out_writer.writelines(str(site.text + "\n"))
                    if index % 25 == 0:
                        print("amount prepared urls:", len(html_sites), "elapsed time:", time.time() - t1, "s")

        print(html_sites)

    def crawl_one_site(self, site):
        """
        It takes a site, requests it, parses it, and then prints the title and the text of the paragraphs.
        # todo save contents
        :param site: the url of the site to be crawled
        """
        soup = BeautifulSoup(self.try_request(site).text, 'lxml')
        root = fromstring(str(soup.contents[1]))
        print(root.xpath("//title/text()"))
        print(root.xpath("//p/text()"))
