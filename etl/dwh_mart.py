import logging
import pandas as pd

from urllib.parse import quote_plus
from sqlalchemy import create_engine

from config_etl import dwh_conn

import warnings
warnings.filterwarnings('ignore')

# Logging setup
logging.basicConfig(level=logging.INFO)

def db_connection(conn_params):
    """Create a connection engine to the database"""
    conn_str = f"postgresql://{conn_params['user']}:{quote_plus(conn_params['password'])}@{conn_params['host']}:{conn_params['port']}/{conn_params['database']}"
    engine = create_engine(conn_str)
    return engine.connect()

# Extract data from source using SQL query
def extract(queries, conn_params):
    """Extract data from PostgreSQL source table using a SQL query"""
    results = {}
    try:
        with db_connection(conn_params) as conn:
            for name, query in queries.items():
                logging.info(f"Extracting '{name}' using query:\n{query.strip()}")
                df = pd.read_sql(query, conn)
                results[name] = df
                logging.info(f"Extraction of '{name}' successful, rows: {len(df)}")
        return results
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
        raise

# Create Data Mart Demografi Pekerja
def create_employee_data_mart(df):
    """Transform data into a Data Mart"""
    
    bins = [0, 24, 34, 44, 54, 100] # kategori rentang usia
    labels = ['<25', '25-34', '35-44', '45-54', '>=55']
    
    df['Usia_Kategori'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)
    pekerja_per_usia = df['Usia_Kategori'].value_counts().sort_index()

    return df

# Create Data Mart Demografi Pelamar
def create_candidate_data_mart(df):
    """Transform data into a Data Mart"""
    
    bins = [0, 24, 34, 44, 54, 100] # kategori rentang usia
    labels = ['<25', '25-34', '35-44', '45-54', '>=55']
    
    df['Usia_Kategori'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)
    pelamar_per_usia = df['Usia_Kategori'].value_counts().sort_index()

    return df

# Create Data Mart Biaya SDM
def create_sdm_cost_data_mart(df_employee, df_payroll):
    """Merge employee & payroll, group by bulan, name, department"""
    
    df = pd.merge(df_payroll, df_employee, on='employee_id', how='left')
    df['bulan'] = pd.to_datetime(df['payment_date']).dt.to_period('M').astype(str)
    summary = df.groupby(['bulan', 'name', 'department'])[['salary', 'overtime_pay']].sum().reset_index()

    return summary


# Load the transformed data into Data Mart
def load_to_data_mart(df, table_name, conn_params):
    """Load the transformed data into Data Mart"""
    try:
        logging.info(f"Loading data into {table_name}...")
        with db_connection(conn_params) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        logging.info(f"Data successfully loaded into {table_name}")
    except Exception as e:
        logging.error(f"Error loading data into {table_name}: {e}")
        raise

def run_etl_mart():
    try:
        queries = {
            "employee": "SELECT  employee_id, name, age, gender, department FROM dim_employee",
            "candidate": "SELECT candidate_id, name, age, gender FROM dim_candidate",
            "payroll": "SELECT employee_id, payment_date, salary, overtime_pay FROM fact_payroll"
        }

        extracted_data = extract(queries, dwh_conn)

        df_employee = extracted_data["employee"]
        df_candidate = extracted_data["candidate"]
        df_payroll = extracted_data["payroll"]

        employee_data_mart = create_employee_data_mart(df_employee)
        load_to_data_mart(employee_data_mart, 'mart_demografi_pekerja', dwh_conn)
        logging.info("mart_demografi_pekerja created successfully!")

        candidate_data_mart = create_candidate_data_mart(df_candidate)
        load_to_data_mart(candidate_data_mart, 'mart_demografi_pelamar', dwh_conn)
        logging.info("mart_demografi_pelamar created successfully!")

        sdm_cost =  create_sdm_cost_data_mart(df_employee, df_payroll)
        load_to_data_mart(sdm_cost, 'mart_biaya_sdm', dwh_conn)
        logging.info("mart_biaya_sdm created Successfully!")

    except Exception as e:
        logging.error(f"ETL extraction failed: {e}")

    if __name__ == "__main__":
        run_etl_mart()