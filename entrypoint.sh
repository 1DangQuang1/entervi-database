# Wait for the database to be ready
echo "Waiting for the database to be ready..."
sleep 10  # Tăng thời gian chờ nếu cần, tùy thuộc vào độ chậm của việc khởi động database.

# Initialize the Airflow database
echo "Initializing Airflow database..."
airflow db init

# Create the admin user if it doesn't exist
echo "Creating Airflow admin user..."
airflow users create \
    --username airflow \
    --firstname Airflow \
    --lastname Admin \
    --role Admin \
    --email admin@example.com \
    --password airflow

# Start the Airflow webserver
echo "Starting Airflow webserver..."
airflow webserver & airflow scheduler
