# Use the official Apache Airflow Docker image
FROM apache/airflow:2.5.1-python3.9

# Install necessary libraries for MySQL and other dependencies
USER root
RUN apt-get update && \
    apt-get install -y mysql-client libmysqlclient-dev && \
    pip install mysql-connector-python pendulum

# Set environment variables for Airflow
ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHONPATH=${PYTHONPATH}:${AIRFLOW_HOME}/dags

# Copy your DAGs into the Airflow dags directory
COPY dags /opt/airflow/dags
COPY sql_scripts /opt/airflow/sql_scripts

# Set ownership and permissions for the airflow user
RUN chown -R airflow: ${AIRFLOW_HOME}

USER airflow

# Entry point to run Airflow scheduler and webserver
ENTRYPOINT ["/entrypoint"]
CMD ["webserver"]
