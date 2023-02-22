#  date: 21. 2. 2023
#  author: Daniel Schnurpfeil
#
import os
import time
from copy import copy

import numpy as np
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import requests
from numpy import fromstring as np_fromstring
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

    def get_urls_from_sitemap(self):
        """
        It takes a sitemap URL, downloads the sitemap, parses it, and returns a list of URLs
        """
        sitemap_url = self.check_sitemap_consistency(self.get_robots_txt())
        urls_from_sitemap = self.try_request(sitemap_url)
        soup = BeautifulSoup(urls_from_sitemap.text, 'lxml')
        root = fromstring(str(soup.contents[1]))
        sub_sitemap = (root.xpath("//loc[contains(text(),'posts')]"))
        return sub_sitemap

    def get_urls_from_sub_sitemap(self):
        pass
        # todo load all html sites to front

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
