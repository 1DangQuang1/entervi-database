from scraping.extract_data import scrape_product_data
from db.insert_data import insert_product_data

def scrape_all_pages(base_url, id):
    # Initialize an empty list to collect all product data across multiple pages
    all_products = []
    
    # Start scraping from the first page
    page_number = 1

    # Continue scraping until no more products are found on the next page
    while True:
        # Construct the URL for the current page, with parameters for sorting and filtering
        current_url = f"{base_url}-{page_number}.html?filterSimilar=true&isGallery=Y&filter=all&sortType=modified-desc&spm=a2700.shop_pl.41413.dbtmnavgo"
        
        # Print the current page being scraped for tracking purposes
        print(f"Đang thu thập dữ liệu từ: {current_url}")
        
        # Scrape product data from the current page
        products = scrape_product_data(current_url,id)
        
        # If no products are found, exit the loop as there are no more pages to scrape
        if not products:
            break
        
        # Add the scraped products from the current page to the all_products list
        all_products.extend(products)
        
        # Move to the next page
        page_number += 1
    
    # Insert all collected product data into the database
    insert_product_data(all_products)
