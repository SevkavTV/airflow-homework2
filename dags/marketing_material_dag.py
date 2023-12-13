from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from ocr import perform_ocr
from db import check_and_update_company
from scrapper import extract_website_content
from gpt import analyze_text_with_gpt

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG('marketing_material_ingestion', default_args=default_args, schedule_interval=None)

def extract_content_wrapper(ti):
    domain = ti.xcom_pull(task_ids='perform_ocr')
    return extract_website_content(domain)

def analyze_text_wrapper(ti):
    content, domain = ti.xcom_pull(task_ids='extract_website_content')
    return analyze_text_with_gpt(content, domain)

def save_data_wrapper(ti):
    company_info = ti.xcom_pull(task_ids='analyze_text_with_gpt')
    
    if company_info:
        check_and_update_company(company_info)

ocr_task = PythonOperator(
    task_id='perform_ocr',
    python_callable=perform_ocr,
    op_kwargs={'image_path': 'path_to_image'},
    dag=dag,
)

extract_content_task = PythonOperator(
    task_id='extract_website_content',
    python_callable=extract_content_wrapper,
    dag=dag,
)

analyze_with_gpt_task = PythonOperator(
    task_id='analyze_text_with_gpt',
    python_callable=analyze_text_wrapper,
    dag=dag,
)

save_to_db_task = PythonOperator(
    task_id='save_data',
    python_callable=save_data_wrapper,
    dag=dag,
)

ocr_task >> extract_content_task >> analyze_with_gpt_task >> save_to_db_task
