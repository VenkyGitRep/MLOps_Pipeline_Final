from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
from airflow import configuration as conf

from src.download_new import download_file
from src.unzip_new import unzip
from src.create import create_newfile
from src.merge import merg_files
from src.read_new import load_data
from src.missing import null_handler
from src.duplicates import handle_duplicates
from src.total_cost import total_cost
from src.dateformat import date_format
from src.groupby import groupby
from src.outliers import outlier_handler
from src.splitdata import split_data
from src.create_openpyxl import create_files_from_sheets


conf.set('core', 'enable_xcom_pickling', 'True')
conf.set('core', 'enable_parquet_xcom', 'True')

default_args = {
    'owner': 'Group_9',
    'start_date': datetime(2024, 3, 1),
    'retries': 0, # Number of retries in case of task failure
    'retry_delay': timedelta(minutes=5), # Delay before retries
}

dag = DAG(
    'MLOP_pro',
    default_args=default_args,
    description='IE7374_project',
    schedule_interval=None, 
    catchup=False,
)

download_file_task = PythonOperator(
    task_id='download_file_task',
    python_callable=download_file,
    op_args=["https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"],
    dag=dag,
)

unzip_file_task = PythonOperator(
    task_id='unzip_file_task',
    python_callable=unzip,
    op_args=[download_file_task.output],
    dag=dag,
)

create_newfile_task = PythonOperator(
    task_id='create_newfile_task',
    python_callable=create_files_from_sheets,
    op_kwargs={
        'input': '{{ ti.xcom_pull(task_ids="unzip_file_task") }}',
    },
    dag=dag,
)
merge_files_task = PythonOperator(
    task_id = 'merge_files_task',
    python_callable = merg_files,
    op_kwargs = {
        'input': '{{ ti.xcom_pull(task_ids="create_newfile_task") }}'
    },
    dag = dag
)

load_data_task = PythonOperator(
    task_id = 'load_data_task',
    python_callable= load_data,
    op_kwargs = {
        'csv_path': '{{ ti.xcom_pull(task_ids="merge_files_task") }}'
    },
    dag = dag
)

null_handler_task = PythonOperator(
    task_id='null_handler_task',
    python_callable=null_handler,
    op_kwargs={
        'input': '{{ ti.xcom_pull(task_ids="load_data_task") }}',
    },
    dag=dag,
)
handle_duplicates_task = PythonOperator(
    task_id = 'handle_duplicates_task',
    python_callable= handle_duplicates,
    op_kwargs={
        'input': '{{ ti.xcom_pull(task_ids="null_handler_task") }}',
    },
    dag=dag,
)

total_cost_task = PythonOperator(
    task_id = 'total_cost_task',
    python_callable=total_cost,
    op_kwargs={
        'input': '{{ ti.xcom_pull(task_ids="handle_duplicates_task") }}',
    },
    dag=dag,
)
date_format_task = PythonOperator(
    task_id = 'date_format_task',
    python_callable= date_format,
    op_kwargs={
        'input': '{{ ti.xcom_pull(task_ids="total_cost_task") }}',
    },
    dag=dag,
)
groupby_task = PythonOperator(
    task_id = 'groupby_task',
    python_callable=groupby,
    op_kwargs={
        'input': '{{ ti.xcom_pull(task_ids="date_format_task") }}',
    },
    dag = dag  
)
outlier_handler_task = PythonOperator(
    task_id = 'outlier_handler_task',
    python_callable=outlier_handler,
    op_kwargs={
        'input': '{{ ti.xcom_pull(task_ids="date_format_task") }}',
    },
    dag = dag 
)
split_data_task = PythonOperator(
    task_id = 'split_data_task',
    python_callable=split_data,
    op_kwargs={
        'input': '{{ ti.xcom_pull(task_ids="outlier_handler_task") }}',
    },
    dag = dag 
)

download_file_task >> unzip_file_task >> create_newfile_task >> merge_files_task \
>> load_data_task >> null_handler_task >> handle_duplicates_task >> total_cost_task \
>> date_format_task >> groupby_task >> outlier_handler_task >> split_data_task

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()