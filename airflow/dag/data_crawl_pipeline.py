from airflow import DAG
from airflow.decorators import task
import pendulum
import os
import mysql.connector
from mysql.connector import Error
import subprocess
import logging
import sys
from datetime import timedelta

# Function to dynamically get base directory and Python interpreter
def get_base_dir_and_python_interpreter():
    if sys.platform.startswith('win'):
        base_dir = r'C:/Users/Admin/Desktop/entervi.com_db'  # Adjust this path to your project root on Windows
        python_interpreter = 'python'
    else:
        base_dir = '/mnt/c/Users/Admin/Desktop/entervi.com_db'  # Adjust this for WSL/Linux environment
        python_interpreter = 'python3'
    return base_dir, python_interpreter

# Define the DAG and its schedule
with DAG(
    'data_crawl_pipeline',
    default_args={
        'owner': 'airflow',
        'start_date': pendulum.today('UTC'),
        'execution_timeout': timedelta(minutes=60)
    },
    description='Data crawling pipeline with batch processing',
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Define a function to run the company crawler
    @task
    def run_company_crawler():
        base_dir, python_interpreter = get_base_dir_and_python_interpreter()
        company_crawler_flag = os.path.join(base_dir, 'entervi_db', 'db', 'company_crawler_done.txt')

        logging.info(f"Running company crawler with base_dir={base_dir}")
        
        if not os.path.exists(company_crawler_flag):
            logging.info("Company crawler not yet completed, running crawler...")
            result = subprocess.run([python_interpreter, os.path.join(base_dir, 'entervi_db', 'main.py')], 
                                    capture_output=True, text=True)
            logging.info(f"Company crawler output: {result.stdout}")
            if result.returncode != 0:
                logging.error(f"Error running company crawler: {result.stderr}")
                raise RuntimeError(f"Company crawler failed with error: {result.stderr}")

            # Create a flag file once the company crawler is completed
            with open(company_crawler_flag, 'w') as f:
                f.write('Company crawler completed')
            logging.info("Company crawler completed.")
        else:
            logging.info("Company crawler already done, skipping.")

    # Define a function to run the product crawler with batch processing
    @task
    def run_product_crawler():
        base_dir, python_interpreter = get_base_dir_and_python_interpreter()
        logging.info(f"Running product crawler with base_dir={base_dir}")
        result = subprocess.run([python_interpreter, os.path.join(base_dir, 'product_info', 'main.py')], 
                                capture_output=True, text=True)
        logging.info(f"Product crawler output: {result.stdout}")
        if result.returncode != 0:
            logging.error(f"Error running product crawler: {result.stderr}")
            raise RuntimeError(f"Product crawler failed with error: {result.stderr}")
        logging.info("Product crawler completed for the current batch.")

    # Define a function to clean data
    @task
    def run_data_cleaner():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="quangci112",
                database="alibaba_db"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                logging.info("Running data cleaner...")

                base_dir, _ = get_base_dir_and_python_interpreter()
                company_crawler_flag = os.path.join(base_dir, 'entervi_db', 'db', 'company_crawler_done.txt')
                
                if not os.path.exists(company_crawler_flag):
                    with open(os.path.join(base_dir, 'SQL_Scripts_for_cleaning_data', 'company_data_clean.sql'), 'r') as f:
                        script = f.read()
                    for statement in script.split(';'):
                        if statement.strip():
                            cursor.execute(statement)

                with open(os.path.join(base_dir, 'SQL_Scripts_for_cleaning_data', 'product_data_clean.sql'), 'r') as f:
                    script = f.read()
                for statement in script.split(';'):
                    if statement.strip():
                        cursor.execute(statement)

                connection.commit()
                logging.info("Data cleaning completed.")
            cursor.close()
            connection.close()

        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            raise

    # Define a function to upload data
    @task
    def run_data_uploader():
        base_dir, python_interpreter = get_base_dir_and_python_interpreter()
        logging.info(f"Running data uploader with base_dir={base_dir}")
        result = subprocess.run([python_interpreter, os.path.join(base_dir, 'Upload', 'main.py')], 
                                capture_output=True, text=True)
        logging.info(f"Data uploader output: {result.stdout}")
        if result.returncode != 0:
            logging.error(f"Error running data uploader: {result.stderr}")
            raise RuntimeError(f"Data uploader failed with error: {result.stderr}")
        logging.info("Data upload completed.")

    # Set task dependencies
    company_crawler = run_company_crawler()
    product_crawler = run_product_crawler()
    data_cleaner = run_data_cleaner()
    data_uploader = run_data_uploader()

    company_crawler >> product_crawler >> data_cleaner >> data_uploader
