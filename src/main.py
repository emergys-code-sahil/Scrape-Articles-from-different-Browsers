from config_manager.json_handler import create_config, load_config  # Importing config_manager for handling json tasks
from search_engines.google import search_google  # Importing google search function 
from output_handler.output_writer import write_to_csv  # Importing output_writer for file writing
from search_engines.yahoo import search_yahoo  # Importing yahoo search function
from search_engines.bing import search_bing  # Importing yahoo search function
import asyncio
import time

print("Assignment 1: Extract the article details from the news section of the following search engines Google, Yahoo and Bing.")

def get_user_input():
    '''
        Taking user input for companies[list], keyword[list] and page count for storing in JSON
    '''
    try:
        companies = [input("Enter the name of company: ") for _ in range(int(input("Enter the number of companies: ")))]
        keywords = [input("Enter a keyword: ") for _ in range(int(input("Enter the number of keywords: ")))]
        page_count = int(input("Enter the number of pages to fetch: "))

        create_config(companies, keywords, page_count)  # Store data into the config JSON file
    except ValueError:
        print("Error: Invalid input. Please enter numbers correctly.")
    except Exception as e:
        print(f"Unexpected error occurred while taking user input: {e}")
        

async def process_articles(config_data):
    """
    Process articles for each company and keyword combination and write them to CSV
    """
    try:
        all_articles_data=[]
        tasks=[]
        # Loop through each company and keyword, then search Google, Yahoo and Bing
        for company_name in config_data['company']:
            for keyword in config_data['keyword']:
                pages = config_data['pages']  # Number of pages to scrape

                # Create tasks for each search engine (Google, Yahoo, Bing)
                tasks.append(search_google(company_name, keyword, pages))
                tasks.append(search_yahoo(company_name, keyword, pages))
                tasks.append(search_bing(company_name, keyword, pages))

        # Gather the results from all tasks concurrently
        all_results = await asyncio.gather(*tasks)

        # Fill the list of results into a single list of articles
        for result in all_results:
            all_articles_data.extend(result)

        # Write the result data to CSV
        write_to_csv(all_articles_data)
    except Exception as e:
        print(f"Error occurred while processing articles: {e}")


async def main():

    # Get the user input and create the config file
    get_user_input()
    
    # Load configuration data from the JSON file
    config_data = load_config()

    start_time = time.time()
    # Process the articles using the loaded config data
    await process_articles(config_data)
    end_time = time.time()
    print(f"It took {end_time - start_time} seconds to fetch extract articles")



if __name__ == '__main__':

    
    asyncio.run(main())
    
    

    

