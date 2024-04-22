from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
from airflow import configuration as conf
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
import os

from src.preprocess import write_preprocessed_data
from src.download_new import download_file
from src.unzip_new import unzip
from src.create import create_newfile
from src.merge import merg_files
from src.read_new import load_data
from src.gradient_descent_model import train_sgd
from src.decision_tree_model import train_decision_tree
from src.knn_regressor_model import train_knn
from src.model_selection import get_Best_run

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


upload_processesd_data_gcs = LocalFilesystemToGCSOperator(
    task_id=f'upload_processesd_data_gcs',
    src=os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')), 'data','output.csv'),
    dst=os.path.join('processed_output_data','output.csv'),
    bucket='dvc_bucket_mlops_lab',
    gcp_conn_id='mlops_gs',
    dag = dag
)

slack_processing_complete = SlackWebhookOperator(
    task_id = 'slack_processing_complete',
    slack_webhook_conn_id = 'mlops_slack_alerts',
    message = "Processed data has been uploaded to Google cloud storage bucket.",
    channel = '#mlops_alerts',
    dag = dag,
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


train_knn_task = PythonOperator(
    task_id = 'train_knn_task',
    python_callable= train_knn,
    dag = dag
)

get_best_run_task = PythonOperator(
    task_id = 'get_best_run_task',
    python_callable= get_Best_run,
    dag = dag
)



send_slack_notification = SlackWebhookOperator(
    task_id = 'send_slack_notification',
    slack_webhook_conn_id = 'mlops_slack_alerts',
    message = "Your datapipeline is complete.",
    channel = '#mlops_alerts',
    dag = dag,
)


download_file_task >> unzip_file_task >> create_newfile_task >> merge_files_task \
>> preprocess_data_task >> upload_processesd_data_gcs >> slack_processing_complete >> [train_sgd_task \
, train_decision_tree_task , train_knn_task] >> get_best_run_task >>  send_slack_notification



# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()
    
    
