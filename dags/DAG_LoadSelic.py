import pendulum

from airflow.sdk import dag, task

from src.load.load_selic import LoadSelic

@dag(
    dag_id="DAG_LoadSelic",
    schedule="10 7 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "selic", "load"],
)

def load_selic_dag():
    
    @task
    def load_selic():

        service = LoadSelic()
        service.main()

    load_selic()



load_selic_dag()