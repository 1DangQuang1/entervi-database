# Import necessary libraries for the Airflow DAG, task decorators, time handling, MySQL, and logging
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

# Function to dynamically get the base directory and the correct Python interpreter based on the operating system.
# This allows the script to run correctly on both Windows and Linux (or WSL) environments.
def get_base_dir_and_python_interpreter():
    if sys.platform.startswith('win'):
        # Set base directory for Windows environment
        base_dir = r'C:/Users/Admin/Desktop/entervi.com_db'  # Adjust this path to your project root on Windows
        python_interpreter = 'python'  # Use 'python' as the interpreter for Windows
    else:
        # Set base directory for WSL/Linux environment
        base_dir = '/mnt/c/Users/Admin/Desktop/entervi.com_db'  # Adjust this for WSL/Linux environment
        python_interpreter = 'python3'  # Use 'python3' as the interpreter for Linux
    return base_dir, python_interpreter

# Define the Airflow DAG with daily scheduling and a maximum execution time of 60 minutes.
# This is the entry point of the pipeline, and the DAG orchestrates the tasks in a sequence.
with DAG(
    'data_crawl_pipeline',
    default_args={
        'owner': 'airflow',  # Default owner of the DAG
        'start_date': pendulum.today('UTC'),  # The start date is set to today
        'execution_timeout': timedelta(minutes=60)  # Max execution time of each run
    },
    description='Data crawling pipeline with batch processing',
    schedule_interval='@daily',  # The DAG runs once per day
    catchup=False  # Prevent backfilling of DAG runs for past dates
) as dag:

    # Task to run the company crawler script, which collects company information.
    # This script checks for a flag file to determine if the crawler has already run, ensuring idempotency.
    @task
    def run_company_crawler():
        base_dir, python_interpreter = get_base_dir_and_python_interpreter()
        company_crawler_flag = os.path.join(base_dir, 'entervi_db', 'db', 'company_crawler_done.txt')

        logging.info(f"Running company crawler with base_dir={base_dir}")
        
        if not os.path.exists(company_crawler_flag):
            # If the company crawler flag file doesn't exist, run the crawler script
            logging.info("Company crawler not yet completed, running crawler...")
            result = subprocess.run([python_interpreter, os.path.join(base_dir, 'entervi_db', 'main.py')], 
                                    capture_output=True, text=True)
            logging.info(f"Company crawler output: {result.stdout}")
            
            # Handle errors if the crawler script fails
            if result.returncode != 0:
                logging.error(f"Error running company crawler: {result.stderr}")
                raise RuntimeError(f"Company crawler failed with error: {result.stderr}")

            # Create a flag file to indicate the crawler has finished running
            with open(company_crawler_flag, 'w') as f:
                f.write('Company crawler completed')
            logging.info("Company crawler completed.")
        else:
            # If the flag file exists, skip running the crawler
            logging.info("Company crawler already done, skipping.")

    # Task to run the product crawler script, which collects product information from the website.
    # This script runs every day and handles the crawling in batches.
    @task
    def run_product_crawler():
        base_dir, python_interpreter = get_base_dir_and_python_interpreter()
        logging.info(f"Running product crawler with base_dir={base_dir}")
        
        # Run the product crawler and capture its output for logging
        result = subprocess.run([python_interpreter, os.path.join(base_dir, 'product_info', 'main.py')], 
                                capture_output=True, text=True)
        logging.info(f"Product crawler output: {result.stdout}")
        
        # Handle errors if the crawler script fails
        if result.returncode != 0:
            logging.error(f"Error running product crawler: {result.stderr}")
            raise RuntimeError(f"Product crawler failed with error: {result.stderr}")
        
        logging.info("Product crawler completed for the current batch.")

    # Task to clean the crawled data using SQL scripts.
    # This task connects to the MySQL database and executes the cleaning SQL scripts for both company and product data.
    @task
    def run_data_cleaner():
        try:
            # Establish connection to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Quangci@123",
                database="alibaba_db"  # Replace with the actual database name
            )
            if connection.is_connected():
                cursor = connection.cursor()
                logging.info("Running data cleaner...")

                base_dir, _ = get_base_dir_and_python_interpreter()
                company_crawler_flag = os.path.join(base_dir, 'entervi_db', 'db', 'company_crawler_done.txt')
                
                # Run company data cleaning script only if the company crawler has completed
                if not os.path.exists(company_crawler_flag):
                    with open(os.path.join(base_dir, 'SQL_Scripts_for_cleaning_data', 'company_data_clean.sql'), 'r') as f:
                        script = f.read()
                    for statement in script.split(';'):
                        if statement.strip():
                            cursor.execute(statement)

                # Run product data cleaning script
                with open(os.path.join(base_dir, 'SQL_Scripts_for_cleaning_data', 'product_data_clean.sql'), 'r') as f:
                    script = f.read()
                for statement in script.split(';'):
                    if statement.strip():
                        cursor.execute(statement)

                connection.commit()  # Commit changes to the database
                logging.info("Data cleaning completed.")
            cursor.close()  # Close the cursor
            connection.close()  # Close the database connection

        except Error as e:
            # Log any errors encountered during the MySQL connection or execution
            logging.error(f"Error connecting to MySQL: {e}")
            raise

    # Task to upload the cleaned data to the final destination.
    # This task runs an external script that handles the data upload process.
    @task
    def run_data_uploader():
        base_dir, python_interpreter = get_base_dir_and_python_interpreter()
        logging.info(f"Running data uploader with base_dir={base_dir}")
        
        # Run the data uploader script and capture its output for logging
        result = subprocess.run([python_interpreter, os.path.join(base_dir, 'Upload', 'main.py')], 
                                capture_output=True, text=True)
        logging.info(f"Data uploader output: {result.stdout}")
        
        # Handle errors if the uploader script fails
        if result.returncode != 0:
            logging.error(f"Error running data uploader: {result.stderr}")
            raise RuntimeError(f"Data uploader failed with error: {result.stderr}")
        
        logging.info("Data upload completed.")

    # Define the dependencies between tasks to ensure they run in the correct order.
    # The company crawler runs first, followed by the product crawler, then data cleaning, and finally data uploading.
    company_crawler = run_company_crawler()
    product_crawler = run_product_crawler()
    data_cleaner = run_data_cleaner()
    data_uploader = run_data_uploader()

    # Task dependency order: company_crawler -> product_crawler -> data_cleaner -> data_uploader
    company_crawler >> product_crawler >> data_cleaner >> data_uploader
