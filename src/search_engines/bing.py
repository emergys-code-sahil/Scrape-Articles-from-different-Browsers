from html_manager.html_parsing import sending_request, parsing_html_from_response, list_of_HTML_of_artciles 
from utilities.date_format import parse_relative_time
import asyncio


async def search_bing(company_name, keyword, pages, baseurl='https://www.bing.com/news/search?q='):
    """
    Searches Bing for articles related to a company and keyword,
    and returns the results as a list.

    Args:
        company_name (str): The name of the company to search for.
        keyword (str): The keyword to associate with the company.
        pages (int): The number of pages to fetch.
        baseurl (str, optional): The base URL for Bing News search. Defaults to Bing's URL.

    Returns:
        list: List of all the list(Search string, Search engine, Link, Title, Time stamp, Media name) 
              of data for each articles
    
    """

    articles_data = []

    # Loop through the required number of pages
    for page_num in range(pages):

        # Calculate the 'start' parameter for pagination
        start = page_num * 10 + 1  # start = page * 10 + 1
        page_url_key="first"
        # Sending the request to Yahoo for the current page
        response = await sending_request(company_name, keyword, baseurl,page_url_key, start)
        
        # Parsing the response if status is OK (200)
        soup = parsing_html_from_response(response)
        
        # Extracting the articles from the parsed HTML
        all_articles = list_of_HTML_of_artciles(soup, "div", "t_t")

        # If no articles are found, break the loop (stop fetching pages)
        if not all_articles:
            break

        # Loop through the number of pages to extract the necessary data
        for i in range(len(all_articles)):
            # Extract media name
            media_name = all_articles[i].find("a", class_="title")
            media_name_get = media_name.get('data-author') if media_name else "Unknown"
            
            # Extract media title
            media_title = all_articles[i].find("a", class_="title")
            media_title_text = media_title.text if media_title else "Unknown"
            
            # Extract the article link
            link = media_name.get('href') if media_name else ""
            
            # Extract timestamp
            time_stamp_section = all_articles[i].find('span', {"tabindex": "0"})
            time_stamp = time_stamp_section.get('aria-label') if time_stamp_section else None
            parsed_time = parse_relative_time(time_stamp.strip()) if time_stamp else "N/A"

            # Collect article data into a list
            articles_data.append([f"{company_name} {keyword}", "Bing", media_name_get, media_title_text, link, parsed_time])
        
    # Return the list of article data
    return articles_data
