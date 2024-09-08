FROM apache/airflow:2.5.1-python3.9

# Install necessary libraries for MySQL and any other dependencies
USER root
RUN apt-get update && apt-get install -y mysql-client libmysqlclient-dev

# Set the Airflow home directory and copy necessary files
ENV AIRFLOW_HOME=/opt/airflow

# Copy your DAGs and SQL scripts to the container
COPY dags /opt/airflow/dags
COPY sql_scripts /opt/airflow/sql_scripts

# Copy the entrypoint.sh script to the container and give it executable permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the custom entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
