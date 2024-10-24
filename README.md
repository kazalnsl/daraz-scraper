# Daraz Scraper

`daraz-scraper` is a Python-based tool to scrape product information from [Daraz](https://www.daraz.com.bd/), a popular e-commerce website, based on specific keywords. It fetches product details like name, price, discount, rating, seller information, and more, and stores them in a CSV file.

## Features

- Scrape product data from Daraz using their api based on a keyword search.
- Retrieves detailed product information like name, price, discount, rating, review count, and seller info.
- Handles pagination and rate-limiting with random delays between requests to avoid overloading the server.
- Saves the scraped data into a CSV file.

## Project Structure

The main components of the project are:

- **Item Model**: A Pydantic model to handle product data validation and preparation.
- **Scraper Logic**: Sends requests to Daraz, parses product data, and handles pagination.
- **CSV Writer**: Saves product details to a CSV file.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/daraz-scraper.git
   cd daraz-scraper
   ```

2. **Install dependencies using Poetry:**

   ```bash
   poetry install
   ```

3. **Activate the virtual environment:**

   ```bash
   poetry shell
   ```

## Usage

1. To run the scraper, execute:

   ```bash
   python main.py
   ```

   By default, it will search for the keyword `"books"` on Daraz. You can modify the `KEYWORD` variable in the code to scrape other product categories.

2. Scraped data is saved in a CSV file named `items.csv` in the project directory.

## Example Output

Here is a sample of the data saved in `items.csv`:

| Name           | Item ID | Original Price | Price | Discount | Rating | Review | Location | Seller Name  | Seller ID | Items Sold | Item URL                     | Image URL                     |
| -------------- | ------- | -------------- | ----- | -------- | ------ | ------ | -------- | ------------ | --------- | ---------- | ---------------------------- | ----------------------------- |
| Sample Product | 123456  | 1500.0         | 1200  | 20%      | 4.8    | 120    | Dhaka    | Daraz Seller | S12345    | 100        | https://daraz.com.bd/item123 | https://daraz.com.bd/image123 |

## Configuration

You can adjust the following parameters in the code:

- **KEYWORD**: Update this variable to scrape products for different search terms.
- **USER_AGENTS**: List of user-agent strings to rotate between requests.

## Requirements

- Python 3.11+
- Poetry

## Dependencies

The project relies on the following dependencies, managed via Poetry:

- `requests`: To send HTTP requests and fetch data from the Daraz api.
- `pydantic`: For data validation and transformation.
