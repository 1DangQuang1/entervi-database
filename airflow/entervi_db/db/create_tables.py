def create_table(connection):
    
    """
    Creates the 'company_data' table in the MySQL database if it doesn't already exist.
    
    Args:
        connection (object): MySQL connection object.
    
    This function defines the table schema and executes the SQL query to create the table.
    Errors during table creation are caught and displayed.
    """


    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS company_data (
            company_id INT AUTO_INCREMENT PRIMARY KEY,
            category_id INT,
            company_name VARCHAR(255),
            logo TEXT,
            link TEXT,
            rating VARCHAR(50),
            response_time VARCHAR(50),
            main_products TEXT,
            capacity_info TEXT,
            product_1_price VARCHAR(255),
            product_1_moq VARCHAR(255),
            product_1_img TEXT,
            product_2_price VARCHAR(255),
            product_2_moq VARCHAR(255),
            product_2_img TEXT,
            view_images TEXT,
            products_link TEXT
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
    except Exception as e:
        print(f"Error creating table:{e}")
    finally:
        cursor.close()
