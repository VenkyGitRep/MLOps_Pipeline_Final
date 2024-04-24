from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator


def slack_alert(context):
    """This function is for us to monitor the failure of our datapipeline, we can receive the notification
    via slack to see which instance/task has error so that we can fix it. 
    """
    ti = context.get('task_instance')
    dag_name = context.get('task_instance').dag_id
    task_name = context.get('task_instance').task_id
    execution_date = context.get('task_instance')
    log_url = context.get('task_instance').log_url
    dag_run = context.get('dag_run')
    
    mssg = f"""
    :red_circle:Pipeline Failed.
    *Dag*:{dag_name}
    *Task*:P{task_name}
    *Execution Date*:{execution_date}
    *Task Instance*:{ti}
    *Log Url*:{log_url}
    *Dag Run*:{dag_run}
    """
    slack_failure_notification = SlackWebhookOperator(
        task_id = 'slack_failure_notification',
        slack_webhook_conn_id = 'mlops_slack_alerts',
        message = mssg,
        channel = '#mlops_alerts'
    )
    return slack_failure_notification.execute(context = context)
