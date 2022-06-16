from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.models import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from airflow.providers.mysql.hooks.mysql import MySqlHook

class Constants:
    DAG_ID = "branch_group_loop_test"

default_args = {
    'owner': 'labase',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def return_branch(**context):
    run_id = context['task_instance'].xcom_pull(task_ids='read_id', key='id') or 0
    print(str(run_id))
    if int(run_id) < 5:
        return 'reschedule_group.reschedule'
    else:
        return 'success'


with DAG(Constants.DAG_ID,
         default_args=default_args,
         schedule_interval=None,
         tags=['branch', 'trigger', 'test']
         ) as dag:
    my55_hook = MySqlHook(mysql_conn_id='mysql_source')

    start = DummyOperator(task_id='start')

    branching = BranchPythonOperator(
        task_id='branching',
        python_callable=return_branch,
        provide_context=True)


    @task(task_id='read_id')
    def read_id(**context):
        """
        This task reads the current id value
        """
        try:
            engine = my55_hook.get_sqlalchemy_engine()
            connection = engine.raw_connection()
            cur = connection.cursor()
            select = """select max(id) from test.test;"""
            print("executing read id")
            cur.execute(select)
            tmp = cur.fetchone()
            print('executed read id')
            last_id = 0
            if tmp:
                last_id = tmp[0]
            context['task_instance'].xcom_push(key=f"id", value=last_id)
            return True
        except Exception as e:
            raise e


    with TaskGroup("reschedule_group", tooltip="Tasks for rescheduling dag") as reschedule_group:
        @task(task_id='increment_id')
        def increment_id(**context):
            """
            This task increments the id by 1 unit
            """
            try:
                engine = my55_hook.get_sqlalchemy_engine()
                connection = engine.raw_connection()
                cur = connection.cursor()
                insert = """insert into test.test values ('');"""
                print("executing increment id")
                cur.execute(insert)
                connection.commit()
                print('executed increment id')
                return True
            except Exception as e:
                raise e

        reschedule = DummyOperator(task_id='reschedule')

        trigger = TriggerDagRunOperator(
            task_id="trigger",
            trigger_dag_id="branch_group_loop_test",
            wait_for_completion=False
        )

        reschedule >> increment_id() >> trigger

    success = DummyOperator(task_id='success')

    start >> read_id() >> branching >> [success, reschedule_group]

