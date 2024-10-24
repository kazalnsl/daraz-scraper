import csv
import os
import random
import time
from typing import List
import requests

from models import Item

KEYWORD = 'books'

def pydantic_models_to_csv(models: List[Item], csv_file_path: str):
    try:
        # Extract data from models into a list of dictionaries
        data = [model.model_dump() for model in models]
        
        # Get field names (keys from the first dictionary)
        fieldnames = data[0].keys()
        
        # Check if the file already exists
        file_exists = os.path.exists(csv_file_path)
        
        # Open the file in append mode
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write header only if the file is newly created
            if not file_exists:
                writer.writeheader()
            
            # Write the rows of data
            writer.writerows(data)
    except Exception as e:
        print(e)
        print("An error occurred while writing data to the CSV file")
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; moto g power (2021)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; DE2118) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
]

def main():
    try:
        session = requests.Session()
        headers = {
            'Referer': 'https://www.daraz.com.bd/',
            'User-Agent': USER_AGENTS[0]
        }
        data = session.get('https://www.daraz.com.bd/catalog/?ajax=true&isFirstRequest=true&page=1&q={KEYWORD}',headers=headers).json()
        total_items = int(data['mainInfo']['totalResults'])
        page_size = int(data['mainInfo']['pageSize'])
        print(f'Total items: {total_items}, Page size: {page_size}')
        items:List[dict] = data['mods']['listItems']
        pydantic_models_to_csv([Item(**item) for item in items], 'items.csv')

        for page in range(2, total_items//page_size + 1):
            random_delay = random.randint(1, 10)
            print(f"Going to sleep for {random_delay} seconds")
            time.sleep(random_delay)
            print(f'Fetching page {page} of {total_items//page_size}')
            headers['User-Agent'] = USER_AGENTS[page % len(USER_AGENTS)]
            data = session.get(f'https://www.daraz.com.bd/catalog/?ajax=true&page={page}&q={KEYWORD}', headers=headers).json()
            items = data['mods']['listItems']
            pydantic_models_to_csv([Item(**item) for item in items], 'items.csv')
    except Exception as e:
        print(e)
        print("An error occurred while fetching data from Daraz")
        raise e
if __name__ == "__main__":
    main()