from db.create_tables import create_product_table
from scraping.scrape_pages import scrape_all_pages
from db.connection import connect_db

def get_offset(file_path="offset.txt"):
    """
    Retrieve the current offset from the specified file. If the file is not found,
    return an initial offset of 0.
    """
    try:
        # Read the offset value from the file
        with open(file_path, "r") as file:
            offset = int(file.read().strip())
    except FileNotFoundError:
        # If the file does not exist, set the offset to 0
        offset = 0
    return offset

def update_offset(offset, file_path="offset.txt"):
    """
    Update the offset in the specified file to keep track of processed records.
    """
    # Write the new offset value to the file
    with open(file_path, "w") as file:
        file.write(str(offset))

def process_links_in_batches(batch_size=2, file_path="offset.txt"):
    """
    Process product links in batches from the database, starting from the offset.
    After processing, update the offset to ensure each link is processed only once.
    """
    # Get the current offset to know where to start processing links
    offset = get_offset(file_path)
    
    # Establish a connection to the database
    db_connection = connect_db()
    cursor = db_connection.cursor()

    # Query the database to fetch a batch of product links, starting from the offset
    cursor.execute(f"SELECT company_id, products_link FROM company_data LIMIT {batch_size} OFFSET {offset}")
    rows = cursor.fetchall()
    
    # Close the database connection
    cursor.close()
    db_connection.close()

    # If no links are retrieved, print a message and exit the function
    if not rows:
        print("No more links to process.")
        return

    # Loop through the retrieved rows (company ID and link)
    for row in rows:
        company_id, link = row
        
        # Extract the base link from the full URL to use for scraping
        base_link = link.split('.html')[0]
        
        # Call the function to scrape all pages for the given base link
        scrape_all_pages(base_link,company_id)

    # Calculate the new offset after processing the batch
    new_offset = offset + batch_size
    
    # Update the offset in the file to ensure the next batch starts from the correct point
    update_offset(new_offset, file_path)
    print(f"Updated offset to: {new_offset}")

if __name__ == "__main__":
    # Create the product table if it doesn't exist
    create_product_table()
    
    # Start processing product links in batches, with a default batch size of 2
    process_links_in_batches(batch_size=2)
