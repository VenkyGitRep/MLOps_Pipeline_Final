from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
from airflow import configuration as conf
from airflow.operators.bash import BashOperator


from src.preprocess import write_preprocessed_data
from src.download_new import download_file
from src.unzip_new import unzip
from src.create import create_newfile
from src.merge import merg_files
from src.read_new import load_data
from src.gradient_descent_model import train_sgd
from src.decision_tree_model import train_decision_tree


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
    # op_args=["https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"],
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
    python_callable=create_newfile,
    dag=dag,
)

merge_files_task = PythonOperator(
    task_id = 'merge_files_task',
    python_callable = merg_files,
    dag = dag
)

preprocess_data_task = PythonOperator(
    task_id = 'preprocess_data_task',
    python_callable= write_preprocessed_data,
    dag = dag
)

train_sgd_task = PythonOperator(
    task_id = 'train_sgd_task',
    python_callable= train_sgd,
    dag = dag
)


train_decision_tree_task = PythonOperator(
    task_id = 'train_decision_tree_task',
    python_callable= train_decision_tree,
    dag = dag
)

download_file_task >> unzip_file_task >> create_newfile_task >> merge_files_task \
>> preprocess_data_task >> train_sgd_task >> train_decision_tree_task

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()
    
    
