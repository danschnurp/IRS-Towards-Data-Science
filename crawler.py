#  date: 21. 2. 2023
#  author: Daniel Schnurpfeil
#
import os
import time

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
                # todo check self.main_site in robots
        else:
            return self.save_robots()

    def save_robots(self) -> str:
        """
        This function saves the robots.txt file to the output directory
        :return: The robots.txt str
        """
        robots = self.try_request(self.main_site + self.robots_txt).text
        with open(self.output_dir + "/" + self.robots_txt, mode="w") as out_writer:
            out_writer.writelines(robots)
        return robots

    def get_sitemap_url(self):
        """
        It takes the robots.txt file, reverses it, and then looks for the first line that contains "Sitemap:" and the main
        site name
        :return: The sitemap url
        """
        robots = self.get_robots_txt()
        robots.reverse()
        for i in robots:
            if "Sitemap:" in i and self.main_site in i:
                sitemap_url = i.replace("Sitemap: ", "")
                sitemap_url = sitemap_url.strip()
                return sitemap_url

    def get_urls_from_sitemap(self):
        """
        It takes a sitemap URL, downloads the sitemap, parses it, and returns a list of URLs
        """
        pass
    # todo

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
