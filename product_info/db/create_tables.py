from db.connection import connect_db
import mysql.connector 

def create_product_table():
    """
    Creates the 'product_data' table in the database if it does not already exist.
    The table stores product information such as link, name, image, price, shipping info, and MOQ.
    """
    # Establish a connection to the database
    db_connection = connect_db()
    cursor = db_connection.cursor()

    # SQL query to create the 'product_data' table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS product_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company_id INT,
        product_link VARCHAR(255) NOT NULL,
        product_name VARCHAR(255),
        product_image VARCHAR(255),
        product_price VARCHAR(50),
        shipping_info VARCHAR(100),
        moq VARCHAR(50)
    );
    """

    try:
        # Execute the table creation query
        cursor.execute(create_table_query)
        
        # Commit the transaction to ensure the table is created
        db_connection.commit()
        
        # Print success message
        print("The 'product_data' table was created successfully.")
    
    except mysql.connector.Error as err:
        # Print an error message if the table creation fails
        print(f"Error creating table: {err}")
    
    finally:
        # Close the cursor and database connection to free resources
        cursor.close()
        db_connection.close()
