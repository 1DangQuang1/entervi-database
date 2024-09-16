FROM apache/airflow:2.5.1-python3.9

# Switch to root to install system dependencies
USER root

# Install necessary libraries for MySQL and other dependencies
RUN apt-get update && apt-get install -y \
    mysql-client \
    libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the Airflow home directory environment variable
ENV AIRFLOW_HOME=/opt/airflow

# Switch back to airflow user
USER airflow

# Copy DAG and SQL scripts to the Airflow home directory
COPY --chown=airflow:airflow airflow/dag/data_crawl_pipeline.py $AIRFLOW_HOME/dags/data_crawl_pipeline.py
COPY --chown=airflow:airflow SQL_Scripts_for_cleaning_data/company_data_clean.sql $AIRFLOW_HOME/sql/company_data_clean.sql
COPY --chown=airflow:airflow SQL_Scripts_for_cleaning_data/product_data_clean.sql $AIRFLOW_HOME/sql/product_data_clean.sql

# Copy the entrypoint.sh script to the container and set executable permissions
COPY --chown=airflow:airflow entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the custom entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Default command for the container: run the webserver and scheduler together
CMD ["bash", "-c", "airflow scheduler & airflow webserver"]
