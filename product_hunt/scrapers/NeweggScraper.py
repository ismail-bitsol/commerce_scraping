import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
import random
import re
from ..models import Website, Product
from .utils import sentiment_score, sentiment_label
from .utils import *

class NeweggScraper:

    def __init__(self, base_url, max_pages=2):
        """
        Initializes an instance of the NeweggScraper class.

        Args:
            base_url (str): The base URL of the Newegg website.
            max_pages (int, optional): The maximum number of pages to scrape. Defaults to 5.

        Returns:
            None

        Initializes the instance variables of the NeweggScraper class with the provided base URL and maximum number of pages.
        Sets the user agent and timeout for making HTTP requests.
        Configures the logging module to log messages at the INFO level.
        """
        self.base_url = base_url
        self.max_pages = max_pages
        self.USER_AGENTS = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
            # Add more user agents here
        ]
        self.TIMEOUT = 10
        logging.basicConfig(level=logging.INFO)

    def fetch_html(self, url):
        """
        Fetches the HTML content of a webpage using the provided URL.

        Parameters:
            url (str): The URL of the webpage to fetch.

        Returns:
            str or None: The HTML content of the webpage if the request is successful, None otherwise.
        """
        try:
            headers = {
                "User-Agent": random.choice(self.USER_AGENTS),
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.Newegg.com/"
            }
            response = requests.get(url, headers=headers, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                logging.error(f"404 Not Found: {url}")
            else:
                logging.error(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch webpage: {url}. Exception: {str(e)}")
            return None

    def parse_html(self, html_text):
        """
        Parses the given HTML text using the BeautifulSoup library and returns the parsed HTML object.

        Parameters:
            html_text (str): The HTML text to be parsed.

        Returns:
            BeautifulSoup: The parsed HTML object.
        """
        try:
            return BeautifulSoup(html_text, 'html.parser')
        except Exception as e:
            logging.error(f"Error parsing HTML: {str(e)}")
            return None


    def extract_product_name(self, soup):
        """
        Extracts the product name from the given BeautifulSoup object.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.

        Returns:
            str: The product name extracted from the HTML content. If the product name cannot be found, it returns 'N/A'.

        """ 
        try:
            name = soup.select_one('.item-title').text if soup.select_one('.item-title') else None
            return name
        except Exception as e:
            logging.error(f"Error extracting product name: {str(e)}")
            return None

    def extract_product_price(self, soup):
        """
        Extracts the price of a product from the given BeautifulSoup object.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.

        Returns:
            str: The price of the product. If the price cannot be found, it returns 'N/A'.
        """
        try:
            price = soup.select_one('.price-current').text
            if price:
                price = re.sub(r'[^\d$.]+', '', price)
                return price
            else:
                return 'N/A'
        except Exception as e:
            logging.error(f"Error extracting product price: {str(e)}")
            return 'N/A'

    def extract_product_reviews(self, soup):
        """
        Extracts the product reviews from the given BeautifulSoup object.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.

        Returns:
            str: The product reviews extracted from the HTML content. If the reviews cannot be found, it returns 'N/A'.
        """
        try:
            rating_tag = soup.select_one('.item-rating i')
            if rating_tag:
                reviews = rating_tag['aria-label']
                match = re.search(r'rated (\d) out of (\d)', reviews)
                if match:
                    reviews = f"{match.group(1)}/{match.group(2)}"
                    score = sentiment_score(reviews)
                    label = sentiment_label(score)
                    return {
                        'reviews': reviews,
                        'sentiment_score': score['compound'],
                        'sentiment_label': label
                    }
            
            return {
                'reviews': None,
                'sentiment_score': 0.0,
                'sentiment_label': 'Neutral'
            }
        except Exception as e:
            logging.error(f"Error extracting product reviews: {str(e)}")
            return {
                'reviews': None,
                'sentiment_score': 0.0,
                'sentiment_label': 'Neutral'
            }

    def extract_product_url(self, soup):
        """
        Extracts the URL of a product from the given BeautifulSoup object.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.

        Returns:
            str: The URL of the product. If the URL cannot be found, it returns 'N/A'. If an error occurs during extraction, it returns 'URL not found' and logs the error message.
        """
        try:
            product_url = soup.select_one('.item-title')['href'] if soup.select_one('.item-title') else None
            return product_url
        except Exception as e:
            logging.error(f"Error extracting product URL: {str(e)}")
            return None

    def extract_product_image_url(self, soup):
        """
        Extracts the product image URL from the given BeautifulSoup object.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.

        Returns:
            str: The URL of the product image. If the image URL cannot be found, it returns 'Image URL not found'.
        """
        try:
            img_tag = soup.select_one('.item-img img')
            return img_tag['src'] if img_tag else "Image URL not found"
        except Exception as e:
            logging.error(f"Error extracting product image URL: {str(e)}")
            return "Image URL not found"

    def get_next_page_url(self, soup):
        """
        Extracts the next page URL from the given BeautifulSoup object.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.

        Returns:
            str: The URL of the next page. If the next page URL cannot be found, it returns None.
        """
        try:
            next_page = soup.select_one('.list-tool-pagination .btn-group-cell a[title="Next"]')
            return next_page['href'] if next_page else None
        except Exception as e:
            logging.error(f"Error extracting next page URL: {str(e)}")
            return None


    def drop_placeholder_rows(self, product_data):
        try:
            return [product for product in product_data if all(value is not None for value in product.values())]
        except Exception as e:
            logging.error(f"Error dropping placeholder rows: {str(e)}")
            return product_data
    def scrape_page(self, url):
        try:
            html_text = self.fetch_html(url)
            if not html_text:
                return []

            soup = self.parse_html(html_text)
            if not soup:
                return []

            product_data = []
            items = soup.select('.item-cell')

            for item in items:
                product_data.append({
                    "name": self.extract_product_name(item),
                    "price": self.extract_product_price(item),
                    "reviews": self.extract_product_reviews(item),
                    "product_url": self.extract_product_url(item),
                    "image_url": self.extract_product_image_url(item),
                })
                time.sleep(1)  # To avoid being blocked by Newegg
            return product_data
        except Exception as e:
            logging.error(f"Error scraping page: {str(e)}")
            return []
        
    def save_to_database(self, product_data,keyword):
        try:
            website, created = Website.objects.get_or_create(name='Newegg', url=self.base_url)
            for product in product_data:
                Product.objects.create(
                    name=product['name'],
                    price=product['price'],
                    reviews=product['reviews'],
                    product_url=product['product_url'],
                    image_url=product['image_url'],
                    website=website,sentiment_score=product['sentiment_score'],
                    sentiment_label=product['sentiment_label'],
                    keyword=keyword
                )
        except Exception as e:
            logging.error(f"Error saving to database: {str(e)}")
            
    def scrape(self, keyword):
        """
        Scrapes Amazon for product data and returns it as a pandas DataFrame.

        Parameters:
            keyword (str): The search keyword.

        Returns:
            pandas.DataFrame: A DataFrame containing the scraped product data.
                The DataFrame has the following columns:
                - name (str): The name of the product.
                - price (str): The price of the product.
                - reviews (str): The number of reviews for the product.
                - product_url (str): The URL of the product page.
                - image_url (str): The URL of the product image.
        """
        all_product_data = []
        current_url = f"{self.base_url}"
        try:
            for _ in range(self.max_pages):
                logging.info(f"Scraping page: {current_url}")
                product_data = self.scrape_page(current_url)
                if not product_data:
                    break
                all_product_data.extend(product_data)
                current_url = self.get_next_page_url(self.parse_html(self.fetch_html(current_url)))
                if not current_url:
                    break
            all_product_data = self.drop_placeholder_rows(all_product_data)
            self.save_to_database(all_product_data, keyword)  # Pass the keyword to save_to_database
        except Exception as e:
            logging.error(f"Error during scraping: {str(e)}")
    
# if __name__ == '__main__':
#     scraper = NeweggScraper('https://www.newegg.com/p/pl?d=iphone')
#     scraper.scrape()