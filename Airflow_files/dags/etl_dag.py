from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators import (PostgresqlDataEntryOperator)
from helpers.helper_functions import scrape_data


default_args = {
    'owner': 'DE Task',
    'depends_on_past':False,
    'start_date': datetime(2022, 31, 8),
    'email_on_retry':False,
    'email_on_failure':False,
    'retries':3,
    'catchup':False,
    'retry_delay': timedelta(minutes=5),
    'provide_context': True
}

#Defining the DAG
dag = DAG('Datapipeline_with_airflow_dag',
          default_args=default_args,
          description='Scrape and load data into Postgresql db with Airflow',
          schedule_interval=timedelta(days=1),
          catchup = False
        )

#Defining the tasks

#Start Operator
start_operator = DummyOperator(
    task_id='Begin_execution',
    dag=dag
)

#Tasks for loading data into the staging tables from the json log files
scrape_tags = PythonOperator(
        task_id='scrape_tag_data',
        python_callable= scrape_data,
        op_kwargs = {"section" : "tags", "fromdate" : (datetime.now() - timedelta(1)).replace(hour=0, minute=0, second=0, microsecond=0)},
        dag=dag,
        do_xcom_push=True
    )

scrape_questions = PythonOperator(
        task_id='scrape_questions_data',
        python_callable= scrape_data,
        op_kwargs = {"section" : "questions", "fromdate" : (datetime.now() - timedelta(1)).replace(hour=0, minute=0, second=0, microsecond=0)},
        dag=dag,
        do_xcom_push=True
    )

scrape_answers = PythonOperator(
        task_id='scrape_answers_data',
        python_callable= scrape_data,
        op_kwargs = {"section" : "answers", "fromdate" : (datetime.now() - timedelta(1)).replace(hour=0, minute=0, second=0, microsecond=0)},
        dag=dag,
        do_xcom_push=True
    )

stage_tags_to_postgres = PostgresqlDataEntryOperator(
    task_id='Stage_tag_data',
    dag=dag,
    table_name = 'stackoverflow_tags_info',
    col_list = ['has_synonyms','moderator_tag','action_tag','tag_count','tag_name'],
    ptask_id = 'scrape_tag_data'
)

stage_questions_to_postgres = PostgresqlDataEntryOperator(
    task_id='Stage_questions_data',
    dag=dag,
    table_name = 'stackoverflow_questions_info',
    col_list = ['question_tags','question_owner','question_is_answered','question_view_count','question_acceptance_answer_id','question_answer_cout', 'question_score','question_last_activity_datetime','question_creation_datetime','question_last_edit_datetime','question_id','question_content_license','question_link','question_title'],
    ptask_id = 'scrape_questions_data'
)

stage_answers_to_postgres = PostgresqlDataEntryOperator(
    task_id='Stage_answers_data',
    dag=dag,
    table_name = 'stackoverflow_answers_info',
    col_list = ['answer_owner','answer_acceptance_status','answer_score','answer_last_activity_datetime','answer_edit_datetime','answer_creation_datetime','answer_id','answer_question_id','answer_content_license','',''],
    ptask_id = 'scrape_answers_data'
)


#The end task
end_operator = DummyOperator(
    task_id='Stop_execution',
    dag=dag
)

# Defining the dependencies
start_operator >> scrape_tags
start_operator >> scrape_questions
start_operator >> scrape_answers

scrape_answers >> stage_answers_to_postgres
scrape_questions >> stage_questions_to_postgres
scrape_tags >> stage_tags_to_postgres

stage_tags_to_postgres >> end_operator
stage_questions_to_postgres >> end_operator
stage_answers_to_postgres >> end_operator