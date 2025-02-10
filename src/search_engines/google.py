from html_manager.html_parsing import sending_request, parsing_html_from_response, list_of_HTML_of_artciles 
from urllib.parse import urljoin
import asyncio

async def search_google(company_name, keyword, pages, baseurl='https://news.google.co.in/search?q='):
    """
    Searches Google for articles related to a company and keyword.

    Args:
        company_name (str): The name of the company to search for.
        keyword (str): The keyword to associate with the company.
        pages (int): The number of pages to fetch.
        baseurl (str, optional): The base URL for Google News search. Defaults to Google's URL.

    Returns:
        list: List of all the list(Search string, Search engine, Link, Title, Time stamp, Media name) 
              of data for each articles
    """
    # Sending the request to Google
    response = await sending_request(company_name, keyword, baseurl, None, None)
    
    # Parsing the response if status is OK (200)
    soup =parsing_html_from_response(response)
    
    # Extracting the articles from the parsed HTML
    all_articles = list_of_HTML_of_artciles(soup, "c-wiz", "PO9Zff")    
    articles_data = []


    for i in range(len(all_articles)):
        media_name = all_articles[i].find("div", class_="vr1PYe")
        media_title = all_articles[i].find("a", class_="JtKRv")
        
        # Handle missing media names or titles
        media_name_text = media_name.text if media_name else "Not available"
        media_title_text = media_title.text if media_title else "Not available"

        # Extract links
        a_tag = all_articles[i].find('a', class_="JtKRv")
        href = a_tag.get('href') if a_tag else "" # Getting the link from "href" tag
        full_link = urljoin(baseurl, href.lstrip('.')) if href else "" #Preparing the full link by joining the base url with href

        # Extract timestamp
        time_stamp = all_articles[i].find('time', 'hvbAAd')
        time = time_stamp.get('datetime') if time_stamp else "N/A" #GEtting the timestamp from the attribut named "datetime"

        articles_data.append([f"{company_name} {keyword}", 'Google', media_name_text, media_title_text, full_link, time])
    
    # Returning the articles data so it can be handled elsewhere (e.g., writing to CSV)
    return articles_data
