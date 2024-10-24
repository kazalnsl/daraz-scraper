import streamlit as st
import csv
import os
import random
import time
from typing import List
import requests
from models import Item

def pydantic_models_to_csv(models: List[Item], csv_file_path: str):
    try:
        data = [model.model_dump() for model in models]
        fieldnames = data[0].keys()
        file_exists = os.path.exists(csv_file_path)
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        st.error(f"An error occurred while writing data to the CSV file: {e}")

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; moto g power (2021)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; DE2118) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
]

def scrape_data(keyword: str):
    try:
        session = requests.Session()
        headers = {'Referer': 'https://www.daraz.com.bd/', 'User-Agent': random.choice(USER_AGENTS)}
        url = f'https://www.daraz.com.bd/catalog/?ajax=true&isFirstRequest=true&page=1&q={keyword}'
        data = session.get(url, headers=headers).json()
        
        total_items = int(data['mainInfo']['totalResults'])
        page_size = int(data['mainInfo']['pageSize'])
        st.write(f'Total items: {total_items}, Page size: {page_size}')

        items: List[dict] = data['mods']['listItems']
        models = [Item(**item) for item in items]
        pydantic_models_to_csv(models, f'{keyword}_items.csv')

        total_pages = total_items // page_size + 1
        progress_bar = st.progress(0)  # Initialize a progress bar

        for page in range(1, total_pages + 1):
            # Random delay to avoid being blocked
            time.sleep(random.uniform(5, 10))
            headers['User-Agent'] = random.choice(USER_AGENTS)

            try:
                url = f'https://www.daraz.com.bd/catalog/?ajax=true&page={page}&q={keyword}'
                data = session.get(url, headers=headers).json()
                items = data['mods']['listItems']
                models = [Item(**item) for item in items]
                pydantic_models_to_csv(models, f'{keyword}_items.csv')

                # Update progress bar
                progress_bar.progress(page / total_pages)
                st.write(f'Fetched page {page} of {total_pages}')

            except requests.exceptions.RequestException as e:
                st.error(f"Request error at page {page}: {e}")
                time.sleep(random.randint(30, 60))  # Longer delay on error

        st.success('Data scraping completed successfully!')
        progress_bar.progress(1)  # Complete the progress bar at the end
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")

def main():
    st.title("Daraz Scraper")
    st.write("Select a keyword to scrape data from Daraz.")
    keywords = ["laptop", "smartphone", "camera", "headphone"]
    keyword = st.selectbox("Select a keyword", keywords)

    if st.button("Export to CSV"):
        st.write(f"Starting to scrape data for keyword: {keyword}")
        scrape_data(keyword)

if __name__ == "__main__":
    main()
