#Dockerfile
FROM apache/airflow:2.8.3-python3.9
# Install additional dependencies
USER root
USER airflow
RUN pip3 install --upgrade pip  # Removed --user flag
# Set up additional Python dependencies
RUN pip3 install --no-cache-dir psycopg2-binary pandas gspread sqlalchemy