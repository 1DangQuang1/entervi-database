def insert_data(connection, company_data):
    """
    Inserts multiple rows of company data into the 'company_data' table.
    
    Args:
        connection (object): MySQL connection object.
        company_data (list): A list of tuples, where each tuple contains data for one company.
    
    This function uses `executemany` for batch insertion and handles errors during the process.
    """
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO company_data (
            category_id, company_name, logo, link, rating, 
            response_time, main_products, capacity_info, 
            product_1_price, product_1_moq, product_1_img, 
            product_2_price, product_2_moq, product_2_img, 
            view_images, products_link
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        # Executing the query with multiple rows
        cursor.executemany(insert_query, company_data)
        connection.commit()
    except Exception as e:
        print(f"Error inserting data:{e}")
    finally:
        cursor.close()



