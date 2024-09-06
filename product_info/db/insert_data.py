from db.connection import connect_db
import mysql.connector
def insert_product_data(products):
    # Establish a connection to the database
    db_connection = connect_db()
    cursor = db_connection.cursor()

    # SQL query to insert product data into the database
    insert_product_query = """
    INSERT INTO product_data 
    (company_id,product_link, product_name, product_image, product_price, shipping_info, moq) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        # Loop through the list of products and execute the insert query for each one
        for product in products:
            cursor.execute(insert_product_query, product)
        
        # Commit the transaction to save changes in the database
        db_connection.commit()
    except mysql.connector.Error as err:
        # Print an error message if there is a MySQL-related error during insertion
        print(f"Error when inserting data: {err}")
    finally:
        # Close the cursor and the database connection to free up resources
        cursor.close()
        db_connection.close()
