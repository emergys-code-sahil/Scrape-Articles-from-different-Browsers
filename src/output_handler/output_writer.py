import csv
import os

def write_to_csv(articles_data, file_name='articles_data.csv'):
    """
    Writes the articles data to a CSV file.

    Args:
        articles_data (list): The list of article data to be written to the CSV.
        file_name (str, optional): The name of the CSV file. Defaults to 'articles_data.csv'.
    """
    file_exists = os.path.isfile(file_name)

    with open(file_name, mode='a', newline='', encoding='utf-8') as file: # Open file in append mode
        writer =csv.writer(file)

        # Write header only if the file is empty (i.e., the header is not already present)
        if not file_exists:
            writer.writerow(['Search String', 'Search Engine', 'Media Name', 'Media Title', 'Link', 'Time'])

        # Write the actual article data
        writer.writerows(articles_data)
