# ETL Pipeline for Data Migrating to Entervi.com Database

This project involves creating an automated ETL pipeline to crawl manufacturer and product information from Alibaba.com, clean the data using SQL scripts, and upload it to a MySQL database and entervi.com via a REST API. Although the pipeline has run successfully, I’ve encountered challenges like handling Alibaba's CAPTCHA, which wasn’t an issue when I manually ran Entervi_db and Product_info on Windows machines. I’m using WSL (Windows Subsystem for Linux) to run Airflow commands which I consider not a good practice when too many commands have to be executed.Therefore,Im exploring Docker to reduce the need for manual intervention.


# How the Pipeline Works
1. **Data crawling**:
   
Selenium is used to automate the process of crawling manufacturer and product data from Alibaba.com.
The crawlers interact with the website as if they are real users, navigating through pages, and extracting relevant data such as manufacturer details, product specifications, etc.
   
Now Im using batch processing for crawling product table which data can come up to 1500 each manufacturer. Therefore, I only ingest 2 links that is in company data each time.( It means that manufacturers crawlers (entervi_db) only run once, after that only product_info run ). I did it by create a offset file, each time product_info run, offset value will update

2. **Data exporting to MySQL workbench**:

Extracted data is processed and exported into a MySQL database using the mysql-connector-python library.
Separate tables are used for manufacturer and product information, ensuring clean data organization.

![Entities Relation Diagram](https://github.com/user-attachments/assets/760c2d07-4bb2-4289-bd7c-17df216e3035)

3. **Data cleaning**:

SQL scripts located in the Clean folder are used to clean and process the data.
These scripts remove duplicates, filter irrelevant data, and standardize the format before final upload.

4. **Data uploading**: (This part contains authentication of entervi.com, therefore I decide not to push it into github)

The cleaned data is uploaded to entervi.com using its REST API.
The upload process is handled by the Upload folder, where the main.py script sends the cleaned data to the website via HTTP POST requests.

5. **Orchestration with Apache Airflow**:
   - The entire process is scheduled and orchestrated using **Apache Airflow**.
   - The `data_crawl_pipeline.py` DAG (Directed Acyclic Graph) defines the sequence of tasks—crawling data, cleaning data, and uploading the cleaned data—ensuring everything runs smoothly and on time.

![DAG](https://github.com/user-attachments/assets/88763f4e-0fed-40c4-8fe1-13d416b7c09b)


## Prerequisites

To run this project, you'll need:

- **Python 3.8+**
- **Apache Airflow**
- **MySQL 5.7+**
- **Docker Desktop**
- **Selenium**: Used for web scraping with Chrome WebDriver.
- **MySQL Connector**: Python library to interact with MySQL.
- **entervi.com API credentials**: Necessary for uploading data via the REST API.

## Setup Instructions

#### Step 1: Clone the Repository

Clone this repository to your local machine.

```bash
git clone <repository-url>
cd <project-directory>
```

#### Step 2: Build the Docker Image

Build the Docker images for the project, which will include all dependencies like Airflow, MySQL, and other necessary libraries.

```bash
docker-compose build
```

#### Step 3: Start the Airflow and MySQL Services

Once the Docker images are built, you can start the Airflow and MySQL services using Docker Compose.

```bash
docker-compose up -d
```

- This command will run the services in the background.
- Airflow's web interface will be accessible at `http://localhost:8080`.
- MySQL will run on `localhost:3306` with the database `alibaba_db`.

#### Step 4: Access the Airflow Web Interface

To monitor and trigger the DAGs, visit the Airflow web interface by navigating to `http://localhost:8080` in your web browser. Use the default login credentials:

- **Username**: airflow
- **Password**: airflow

#### Step 5: Trigger the DAG

In the Airflow web interface, you should see your DAG (`data_crawl_pipeline`). You can manually trigger the DAG or let it run on its daily schedule.

#### Step 6: Stop the Services

When you're done, you can stop the Docker services using:

```bash
docker-compose down
```

## Contributions

Feel free to fork this repository and submit pull requests for any improvements. You can also open issues for bug reports or feature requests.
