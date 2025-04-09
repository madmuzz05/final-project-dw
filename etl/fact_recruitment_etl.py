import sys
import os
import warnings
import logging
import pandas as pd

from pymongo import MongoClient
from sqlalchemy import create_engine
from urllib.parse import quote_plus

sys.path.append(os.path.abspath("/opt/airflow/etl"))
from config_etl import etl_config_fact_recruitment
from config_etl import dwh_conn
from config_etl import oltp_conn_mongodb

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)

def db_connection(conn_params):
    """Create a PostgreSQL connection"""
    conn_str = f"postgresql+psycopg2://{conn_params['user']}:{quote_plus(conn_params['password'])}@{conn_params['host']}:{conn_params['port']}/{conn_params['database']}"
    logging.info(f"Connecting to PostgreSQL: {conn_str}")
    engine = create_engine(conn_str)
    return engine.connect()

def mongo_connection(mongo_uri):
    """Create MongoDB client"""
    return MongoClient(mongo_uri)

def validate_config(etl_config):
    """Validate the ETL configuration"""
    required_keys = ['collection_name', 'query', 'destination_table', 'column_mapping']
    for table_name, table_config in etl_config.items():
        for key in required_keys:
            if key not in table_config:
                raise ValueError(f"Missing {key} in config for table {table_name}")
    logging.info("Config validation passed")

def extract(table_config, mongo_uri):
    """Extract data from MongoDB"""
    try:
        logging.info(f"Extracting data from MongoDB collection {table_config['collection_name']}...")
        client = mongo_connection(mongo_uri)
        db = client[oltp_conn_mongodb['database']]  # Ubah ke nama database kamu
        collection = db[table_config["collection_name"]]
        data = list(collection.find(table_config.get("query", {})))
        df = pd.DataFrame(data)
        return df
    except Exception as err:
        logging.error(f"Error extracting data from MongoDB: {err}")
        raise

def transform(df, table_config):
    """Transform MongoDB data before loading"""
    try:
        logging.info(f"Transforming data for {table_config['destination_table']}...")
        df.rename(columns=table_config["column_mapping"], inplace=True)
        df.drop(columns=["_id"], errors="ignore", inplace=True)
        df.drop(columns=["Age"], errors="ignore", inplace=True)
        df.drop(columns=["Name"], errors="ignore", inplace=True)
        df.drop(columns=["Gender"], errors="ignore", inplace=True)

        df.drop_duplicates(subset=["candidate_id"], inplace=True)
        df["interview_date"] = pd.to_datetime(df["interview_date"], errors='coerce')
        df["application_date"] = pd.to_datetime(df["application_date"], errors='coerce')
        print(df.to_dict('records'))
        return df
    except Exception as err:
        logging.error(f"Error transforming data: {err}")
        raise

def load(df, table_config):
    """Load transformed data into PostgreSQL"""
    try:
        logging.info(f"Loading data into {table_config['destination_table']}...")
        with db_connection(dwh_conn) as conn:
            conn.execute(f"TRUNCATE TABLE {table_config['destination_table']} RESTART IDENTITY CASCADE;")
            df.to_sql(
                table_config["destination_table"],
                con=conn,
                if_exists="append",
                index=False
            )
        logging.info(f"Loaded {len(df)} rows into {table_config['destination_table']}")
    except Exception as err:
        logging.error(f"Error loading data into PostgreSQL: {err}")
        raise

def run_etl_fact_recruitment():
    try:
        logging.info("Starting MongoDB ETL process...")
        validate_config(etl_config_fact_recruitment)

        # Create MongoDB connection URI
        mongo_uri = f"mongodb://{oltp_conn_mongodb['user']}:{quote_plus(oltp_conn_mongodb['password'])}@{oltp_conn_mongodb['host']}:{oltp_conn_mongodb['port']}"
        print(f"Connecting to MongoDB: {mongo_uri}")

        for table_name, table_config in etl_config_fact_recruitment.items():
            df_raw = extract(table_config, mongo_uri)
            if df_raw.empty:
                logging.info(f"No data found in collection {table_config['collection_name']}")
                continue
            df = transform(df_raw, table_config)
            load(df, table_config)

        logging.info("ETL MongoDB process completed successfully!")

    except Exception as err:
        logging.error(f"ETL MongoDB process failed: {err}")
