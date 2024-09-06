import time
from scraping.extract_company_data import extract_company_data

def scrape_all_pages(driver, base_url, link_id, start_id=1, max_pages=100):
    """
    Scrapes data from multiple paginated pages on a website.
    
    Args:
        driver (webdriver): Selenium WebDriver instance.
        base_url (str): Base URL for the page to be scraped.
        link_id (int): The ID representing the category or link being scraped.
        start_id (int): The starting ID for company records.
        max_pages (int): Maximum number of pages to scrape.
    
    Returns:
        all_data (list): A list of dictionaries containing all scraped data.
    
    This function handles the pagination of results and manages data extraction for each page.
    """
    all_data = []
    current_id = start_id

    for page in range(1, max_pages + 1):
        try:
            paginated_url = base_url + f"&&page={page}"
            driver.get(paginated_url)
            time.sleep(3)  
            
            if "No results found" in driver.page_source:
                break
            
            page_data = extract_company_data(driver, current_id, link_id)
            if not page_data:
                break

            all_data.extend(page_data)
            current_id += len(page_data)
        except Exception as e:
            print(f"Error scraping page {page} of {base_url}: {e}")
            break
    
    return all_data
