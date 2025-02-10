import asyncio
import aiohttp
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

async def sending_request(company_name, keyword, baseurl, page_url_key, start):
    """
    Sends an asynchronous HTTP request to the specified URL constructed using the company name and keyword.
    
    Args:
        company_name (str): The name of the company to search for.
        keyword (str): The keyword to search for in combination with the company name.
        baseurl (str): The base URL for the search query (default is Google News).
        page_url_key (str): The keyword for appending in url for getting the page number
        start (str): The start number of the articles from where we have to fetch it

    Returns:
        str: The HTML content of the response page.
    """
       # Construct the search query using the company name and keyword
    query = f"{company_name} {keyword}"
    update_query = quote_plus(query)  # URL-encode the query string
    url = f"{baseurl}{update_query}&{page_url_key}={start}"  # Construct the full URL by appending the encoded query and start value
    print(f"Requesting URL: {url}")  # Printing URL for debugging
    # Set the User-Agent header to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Using aiohttp for asynchronous HTTP request
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            #Getting HTML in response
            return await response.text()


def parsing_html_from_response(response):
    """
    Parses the HTML response using BeautifulSoup to extract the page content.

    Args:
        response (str): The raw HTML content returned from the HTTP request.

    Returns:
        BeautifulSoup: A BeautifulSoup object containing the parsed HTML content.
    """
    if response:
        # Parse the response using BeautifulSoup for easy extraction of data
        soup = BeautifulSoup(response, 'html.parser')
        return soup
    return None  # Return None if the response is empty or invalid


def list_of_HTML_of_artciles(soup, tag_name, class_name):
    """
    Extracts a list of articles from the parsed HTML soup based on specified tag and class.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML content.
        tag_name (str): The HTML tag to search for.
        class_name (str): The CSS class name associated with the articles.

    Returns:
        list: A list of BeautifulSoup objects representing each article found in the HTML.
    """
    # Find all articles by looking for the specified tag and class in the parsed HTML
    all_articles = soup.find_all(tag_name, class_=class_name)

    # Return the list of articles
    return all_articles
