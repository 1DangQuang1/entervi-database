def create_products_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        SELECT com.company_name, pro.product_name, pro.product_price, 
            CONCAT('Shipping info: ', pro.shipping_info, '\nMOQ: ', pro.moq) as description
        FROM product_data as pro 
        JOIN company_data as com 
        WHERE pro.company_id = com.company_id;
        """
        cursor.excute(create_table_query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print ('Error when fetching table: {e}')

    finally :
        cursor.close()