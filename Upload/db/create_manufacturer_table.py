def create_manufacturers_table(connection):
    """
    Required key to upload manufacturer to entervi.com : 
        category, 
        name, 
        logo, 
        description (concate rating, response_time, capacity_info and main_products)
    """
    try:
        cursor = connection.cursor()
        creat_table_query = """
        SELECT 
        cate.category AS category, 
        com.company_name AS name, 
        com.logo AS logo, 
        CONCAT('Rating: ', com.rating, '\nResponse Time: ', com.response_time, '\nCapacity Info: ', com.capacity_info, '\nMain Products: ', com.main_products) AS description
        FROM 
            company_data AS com 
        JOIN 
            category_name AS cate 
        ON 
            com.category_id = cate.id;

        """
        cursor.excute(creat_table_query)
        result = cursor.fetchall()
        return result
    
    except Exception as e:
        print(f'Error when fetching table   :{e}')
    
    finally:
        cursor.close()