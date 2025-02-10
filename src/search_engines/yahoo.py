from html_manager.html_parsing import sending_request, parsing_html_from_response, list_of_HTML_of_artciles
from urllib.parse import urljoin
from utilities.date_format import parse_relative_time
import asyncio



async def search_yahoo(company_name, keyword, pages, baseurl='https://news.search.yahoo.com/search?p='):
    """
    Searches Yahoo for articles related to a company and keyword,
    and returns the results as a list, handling pagination with the 'start' parameter.

    Args:
        company_name (str): The name of the company to search for.
        keyword (str): The keyword to associate with the company.
        pages (int): The number of pages to fetch.
        baseurl (str, optional): The base URL for Yahoo News search. Defaults to Yahoo's URL.
    
    Returns:
        list: List of all the articles data for each article.
    """
    articles_data = []  # To store all the article data

    # Loop through the required number of pages
    for page_num in range(pages):
        # Calculate the 'start' parameter for pagination
        start = page_num * 10 + 1  # start = page * 10 + 1
        page_url_key="b"
        # Sending the request to Yahoo for the current page
        response = await sending_request(company_name, keyword, baseurl,page_url_key, start)

        # Parse the HTML response
        soup = parsing_html_from_response(response)

        # Extract the articles from the page
        articles_section = soup.find("div", id='web')
        all_articles = articles_section.find_all("ul", class_="compArticleList")

        # If no articles are found, break the loop (stop fetching pages)
        if not all_articles:
            break

        # Extract data for each article on the current page
        for i in range(len(all_articles)):
            media_name = all_articles[i].find("span", class_="s-source")
            media_title = all_articles[i].find("h4", class_="s-title")

            # Handle missing media names or titles
            media_name_text = media_name.text if media_name else "Not available"
            media_title_text = media_title.text if media_title else "Not available"

            # Extract links
            a_tag = media_title.find('a')
            link = a_tag.get('href') if a_tag else ""

            # Extract timestamp and parse
            time_stamp = all_articles[i].find('span', class_='s-time')
            time = time_stamp.text.strip() if time_stamp else "N/A"
            parsed_time = parse_relative_time(time)

            # Append the data to the articles list
            articles_data.append([f"{company_name} {keyword}", 'Yahoo', media_name_text, media_title_text, link, parsed_time])

    # Return the list of article data
    return articles_data
