from selenium import webdriver
from db.connection import create_connection
from db.create_tables import create_table
from db.insert_data import insert_data
from scraping.scrape_pages import scrape_all_pages
import os 
from selenium.webdriver.chrome.options import Options

def main():
    """
    Main function to control the entire scraping process.
    
    This function reads URLs from 'links.txt', initializes Selenium WebDriver, connects to MySQL,
    scrapes data from each URL, and inserts the scraped data into the database.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    links_file = os.path.join(base_dir, 'links.txt') 
    # Reading the links from 'links.txt'
    with open(links_file, 'r') as file:
        base_urls = file.read().splitlines()

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Specify the path to the Google Chrome binary
    driver = webdriver.Chrome(options=chrome_options)

    connection = create_connection()
    if connection:
        create_table(connection)
    else:
        print("Could not establish connection to the database")
        return

    max_pages_per_url = 100
    current_id = 1

    for link_id, base_url in enumerate(base_urls, start=1):
        url_data = scrape_all_pages(driver, base_url, link_id=link_id, start_id=current_id, max_pages=max_pages_per_url)
        
        if url_data:
            insert_data(connection, url_data)
        current_id += len(url_data)
    
    driver.quit()
    connection.close()
    print("Data has been succesfully imported into SQL")

if __name__ == "__main__":
    main()
