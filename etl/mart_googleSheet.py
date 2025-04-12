import logging
import pandas as pd
import json
import gspread
import os

from urllib.parse import quote_plus
from sqlalchemy import create_engine

from config_etl import dwh_conn
from oauth2client.service_account import ServiceAccountCredentials

import warnings
warnings.filterwarnings('ignore')

import warnings
warnings.filterwarnings('ignore')

credential_path="/opt/airflow/credential.json"

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
        
# Load the data mart into Google Sheet
def load_to_separate_google_sheets(dfs: dict, credential_path=credential_path, share_email=None):
    try:
        with open(credential_path, 'r') as f:
            creds_dict = json.load(f)

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        for sheet_title, df in dfs.items():
            try:
                # Check and delete old file
                for spreadsheet in client.list_spreadsheet_files():
                    if spreadsheet['name'] == sheet_title:
                        client.del_spreadsheet(spreadsheet['id'])
                        logging.info(f"Deleted existing spreadsheet: {sheet_title}")

                # create new file
                sheet = client.create(sheet_title)
                logging.info(f"Created new spreadsheet: {sheet.url}")

                if share_email:
                    sheet.share(share_email, perm_type="user", role="writer")
                    logging.info(f"Shared {sheet_title} with {share_email}")

                # Add worksheet and content
                worksheet = sheet.sheet1
                worksheet.update([df.columns.tolist()] + df.astype(str).values.tolist())
                logging.info(f"Uploaded data to spreadsheet: {sheet_title}")

            except Exception as e:
                logging.error(f"Error uploading {sheet_title}: {e}")
                raise

    except Exception as e:
        logging.error(f"Google Sheet auth or upload failed: {e}")
        raise


def run_mart_gsheet():
    queries = {
        "Demografi Pekerja": "SELECT * FROM mart_demografi_pekerja",
        "Demografi Pelamar": "SELECT * FROM mart_demografi_pelamar",
        "Biaya SDM": "SELECT * FROM mart_biaya_sdm"
    }

    try:
        extracted_data = extract(queries, dwh_conn)

        share_email = os.getenv("SHARED_EMAIL")

        load_to_separate_google_sheets(extracted_data, credential_path=credential_path, share_email=share_email)
        logging.info("All data uploaded successfully to separate Google Sheets.")

    except Exception as e:
        logging.error(f"Process failed: {e}")

if __name__ == "__main__":
    run_mart_gsheet()