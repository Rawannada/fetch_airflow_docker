from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime

# ------------------ TASK FUNCTIONS ------------------

# Extract: simulate reading data
def extract_data(**context):
    data = [10, 20, 30, 40, 50]
    print(f"Extracted data: {data}")

    # Push data into XCom
    context['ti'].xcom_push(key='raw_data', value=data)
    print("Data pushed to XCom successfully.")


# Transform: process data and push result
def transform_data(**context):
    # Pull data from XCom
    data = context['ti'].xcom_pull(key='raw_data', task_ids='extract_task')
    print(f"Pulled raw data from XCom: {data}")

    # Calculate sum and average
    total = sum(data)
    avg = total / len(data)
    result = {'total': total, 'average': avg}
    print(f"Transformed data: {result}")

    # Push result back to XCom
    context['ti'].xcom_push(key='transformed_data', value=result)
    print("Transformed data pushed to XCom successfully.")


# Load: simulate saving or final output
def load_data(**context):
    # Pull result from transform task
    result = context['ti'].xcom_pull(key='transformed_data', task_ids='transform_task')
    print(f"Data received in load task: {result}")

    # Simulate load step
    print(f"✅ Loading complete. Total = {result['total']}, Average = {result['average']}")

    # Prepare email data and push it into XCom
    email_subject = "ETL Pipeline Completed Successfully ✅"
    email_body = f"""
    <h3>ETL Pipeline Report</h3>
    <p>Total Sum: {result['total']}</p>
    <p>Average Value: {result['average']}</p>
    <p>Status: Completed Successfully</p>
    """

    context['ti'].xcom_push(key='email_subject', value=email_subject)
    context['ti'].xcom_push(key='email_body', value=email_body)
    print("Email content pushed to XCom successfully.")


# ------------------ DAG DEFINITION ------------------

with DAG(
    dag_id='xcom_etl_email_example',
    start_date=datetime(2025, 10, 17),
    schedule_interval=None,
    catchup=False,
    tags=['xcom', 'etl', 'email']
) as dag:

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_data
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_data
    )

    # Email task (pull data from XCom)
    send_email = EmailOperator(
        task_id='send_email',
        to='ahmed.azab201829@gmail.com',
        subject="{{ task_instance.xcom_pull(task_ids='load_task', key='email_subject') }}",
        html_content="{{ task_instance.xcom_pull(task_ids='load_task', key='email_body') }}"
    )

    # ترتيب التنفيذ
    extract_task >> transform_task >> load_task >> send_email
