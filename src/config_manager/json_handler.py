import json

def load_config(file_path='search_company.json'):
    """
    Loads the configuration data from a JSON file.

    This function reads the JSON file from the given file path, parses its contents, 
    and returns the data as a Python dictionary.

    Args:
        file_path (str, optional): The path to the JSON configuration file. 
                                   Defaults to 'search_company.json'.

    Returns:
        dict: A dictionary containing the configuration data, such as company names, 
              keywords, and page count.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)   # Load JSON data into the dictionary
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
        return {}
    except Exception as e:
        print(f"Unexpected error occurred while loading config: {e}")
        return {}

def create_config(companies, keywords, page_count, file_path='search_company.json'):
    """
    Creates a new configuration JSON file with provided company names, keywords, 
    and page count.

    This function generates a dictionary containing the companies, keywords, 
    and the number of pages to fetch, then writes it to the specified file 
    as a JSON structure.

    Args:
        companies (list of str): A list of company names to search for.
        keywords (list of str): A list of keywords to associate with the companies.
        page_count (int): The number of pages to fetch for each search.
        file_path (str, optional): The path where the JSON configuration file will be saved. 
                                    Defaults to 'search_company.json'.
    """
    try:
        search_dict = {
            "company": companies,
            "keyword": keywords,
            "pages": page_count
        }
        with open(file_path, 'w') as file:
            json.dump(search_dict, file, indent=4) # Dumping dictionary into JSON
    except Exception as e:
        print(f"Error: An unexpected error occurred while creating the config file: {e}")
