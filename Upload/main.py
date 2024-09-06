from db.create_manufacturer_table import create_manufacturers_table
from db.create_product_table import create_products_table
from db.connection import create_connection
import json
def main():
    connection = create_connection()
    if connection :
        manufacturers = create_manufacturers_table(connection)
        products = create_products_table(connection)

    else :
        print ('Could not create connection to the database')

    company_data_list = []
    for row in manufacturers :
        data ={
            'Category' : row[0],
            'Company_name' : row[1],
            'Logo' : row[2],
            'Description' : row[3]
        }
        company_data_list.append(data)
    product_data_list = []
    for row in products :
        data ={
            'Company_name' : row[0],
            'Product_name' : row[1],
            'Price' : row[2],
            'Description' : row[3]
        }
        product_data_list.append(data)

    
    
    company_json = json.dumps(company_data_list,ensure_ascii=False)
    product_json = json.dumps(product_data_list,ensure_ascii=False)

    
