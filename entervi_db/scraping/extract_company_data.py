from selenium.webdriver.common.by import By
def extract_company_data(driver, start_id, link_id):
    """
    Extracts company data from the current page using Selenium.
    
    Args:
        driver (webdriver): Selenium WebDriver instance.
        start_id (int): The starting ID for company records on this page.
        link_id (int): The ID representing the category or link being scraped.
    
    Returns:
        company_data (list): A list of dictionaries containing company information.
    
    This function handles individual data extraction for company details like name, link, rating, etc.,
    including error handling for missing elements.
    """
    companies = driver.find_elements(By.CLASS_NAME, "factory-card")
    company_data = []

    for idx, company in enumerate(companies):
        try:
            company_name = company.find_element(By.CSS_SELECTOR, ".card-title h3 a").text
            company_link = company.find_element(By.CSS_SELECTOR, ".card-title h3 a").get_attribute("href")
            logo = company.find_element(By.CSS_SELECTOR, ".logo img").get_attribute("src")
            products_link = company_link.replace('company_profile.html', 'productlist.html')
            rating = company.find_element(By.CSS_SELECTOR, ".evaluate strong").text if company.find_elements(By.CSS_SELECTOR, ".evaluate strong") else "N/A"

            # Initialize variables for optional fields
            response_time = "N/A"
            main_products = "N/A"
            capacity_info = "N/A"

            # Extract additional details in capability-container
            capability_container = company.find_elements(By.CSS_SELECTOR, ".capability-container")
            response_time = capability_container[0].find_element(By.CSS_SELECTOR, "h4:nth-of-type(1) + strong").text if capability_container[0].find_elements(By.CSS_SELECTOR, "h4:nth-of-type(1) + strong") else "N/A"
            main_products = capability_container[0].find_element(By.CSS_SELECTOR, "h4:nth-of-type(2) + strong").text if capability_container[0].find_elements(By.CSS_SELECTOR, "h4:nth-of-type(2) + strong") else "N/A"
            capacity_info = company.find_element(By.CSS_SELECTOR, ".capability-wrapper").text if capacity_info else "N/A"

            # Extract product details
            products = company.find_elements(By.CSS_SELECTOR, ".product-box")
            product_1_price = product_1_moq = product_1_img = "N/A"
            product_2_price = product_2_moq = product_2_img = "N/A"

            if len(products) > 0:
                product_1_price = products[0].find_element(By.CSS_SELECTOR, ".price").text
                product_1_moq = products[0].find_element(By.CSS_SELECTOR, ".moq").text
                product_1_img = products[0].find_element(By.CSS_SELECTOR, ".product-img").get_attribute("src")

            if len(products) > 1:
                product_2_price = products[1].find_element(By.CSS_SELECTOR, ".price").text
                product_2_moq = products[1].find_element(By.CSS_SELECTOR, ".moq").text
                product_2_img = products[1].find_element(By.CSS_SELECTOR, ".product-img").get_attribute("src")

            # Extract view images
            view_images_elements = company.find_elements(By.CSS_SELECTOR, ".view .factory-carousel__slide__img")
            view_images = "\n ".join([img.get_attribute("src") for img in view_images_elements]) if view_images_elements else "N/A"

            # Append the extracted data as a dictionary
            company_data.append((
                    link_id,      
                    company_name,
                    logo,
                    company_link,      
                    rating,
                    response_time,
                    main_products,
                    capacity_info,
                    product_1_price,
                    product_1_moq,
                    product_1_img,
                    product_2_price,
                    product_2_moq,
                    product_2_img,
                    view_images,
                    products_link
            ))

        except Exception as e:
            print(f"Error extracting data for company ID {start_id + idx}:{e}")

    
    return company_data
