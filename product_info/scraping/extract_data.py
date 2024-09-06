from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from config.scraper_config import SCRAPER_TIMEOUT
from selenium.webdriver.chrome.options import Options
def scrape_product_data(url, company_id):
    # Initialize a new Chrome WebDriver instance
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer

    driver = webdriver.Chrome(options= chrome_options)
    
    # Navigate to the target URL
    driver.get(url)
    
    # Create a WebDriverWait object with a timeout defined in the configuration
    wait = WebDriverWait(driver, SCRAPER_TIMEOUT)

    try:
        # Wait until the gallery view element is present on the page
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gallery-view")))
    except TimeoutException:
        # If the element doesn't load within the timeout, print an error message
        print("The page doesn't load properly or there are no products available.")
        return []  # Return an empty list if the page fails to load products

    # Initialize an empty list to store product data
    products = []
    
    # Find all elements with the class 'gallery-view' representing product sections
    four_product_cards = driver.find_elements(By.CLASS_NAME, "gallery-view")
    
    # Loop through each product section
    for product_cards in four_product_cards:
        # Find all elements with the class 'product-item' within the product section
        product_card = product_cards.find_elements(By.CLASS_NAME, 'product-item')
        
        # Loop through each individual product card
        for card in product_card:
            try:
                # Extract product link and name
                product_element = card.find_element(By.CSS_SELECTOR, "a.title-link.icbu-link-normal")
                product_link = "https:" + product_element.get_attribute("href")
                product_name = product_element.text

                try:
                    # Wait for and extract the product image
                    product_image_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.img-box img"))
                    )
                    product_image = "https:" + product_image_element.get_attribute("src")
                except TimeoutException:
                    # If the image fails to load, set the product image to None
                    product_image = None
                
                # Extract additional product details like price, shipping info, and MOQ
                card1 = card.find_element(By.CLASS_NAME, "product-info")
                
                product_price_element = card1.find_element(By.CSS_SELECTOR, "div.price")
                product_price = product_price_element.text.strip()
                
                shipping_info_element = card1.find_element(By.CSS_SELECTOR, "div.freight-str")
                shipping_info = shipping_info_element.text.strip()
                
                moq_element = card1.find_element(By.CSS_SELECTOR, "div.moq")
                moq = moq_element.text.strip()
                
                # Append the extracted product data to the products list
                products.append((company_id, product_link, product_name, product_image, product_price, shipping_info, moq))
            except NoSuchElementException as e:
                # If any required element is missing, print an error message with details
                print(f"Error when extracting product info: {e}")
    
    # Close the WebDriver session
    driver.quit()
    
    # Return the list of products scraped from the page
    return products
