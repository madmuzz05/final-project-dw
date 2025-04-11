import sys
import os

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from datetime import datetime

sys.path.append(os.path.abspath("/opt/airflow/etl"))  # Adjusted path to match Airflow's structure
from dim_employee_etl import run_etl_dim_employee 
from fact_payroll_etl import run_etl_fact_payroll
from fact_training_etl import run_etl_fact_training
from dim_candidate_etl import run_etl_dim_candidate
from fact_recruitment_etl import run_etl_fact_recruitment

from dwh_mart import run_etl_mart
from mart_googleSheet import run_mart_gsheet

with DAG(
    dag_id='etl',
    start_date=datetime(2024, 5, 1),
    schedule_interval='0 0,12 * * *',  # Runs twice a day: at midnight and noon
    catchup=False
) as dag:
    

    start_task = EmptyOperator(
        task_id='start'
    )

    run_etl = PythonOperator(
        task_id='run_etl_function',
        python_callable=run_etl_dim_employee,
    )

    run_payroll_etl = PythonOperator(
        task_id='run_payroll_etl_function',
        python_callable=run_etl_fact_payroll,
    )

    run_training_etl = PythonOperator(
        task_id='run_training_etl_function',
        python_callable=run_etl_fact_training,
    )

    run_dim_candidate_etl = PythonOperator(
        task_id='run_dim_candidar_etl_function',
        python_callable=run_etl_dim_candidate,
    )

    run_recruitment_etl = PythonOperator(
        task_id='run_recruitment_etl_function',
        python_callable=run_etl_fact_recruitment,
    )

    run_dwh_mart = PythonOperator(
        task_id='run_dwh_mart',
        python_callable=run_etl_mart,
    )

    run_mart_googleSheet = PythonOperator(
        task_id='run_mart_googleSheet',
        python_callable=run_mart_gsheet,
    )

    end_task = EmptyOperator(
        task_id='end'
    )

start_task >> run_etl >> run_payroll_etl >>run_training_etl >> run_dim_candidate_etl >> run_recruitment_etl >> run_dwh_mart >> run_mart_googleSheet >> end_task