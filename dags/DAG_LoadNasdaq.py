import pendulum

from airflow.sdk import dag, task

from src.load.load_nasdaq import LoadNasdaq

@dag(
    dag_id="DAG_LoadNasdaq",
    schedule="40 7 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "Nasdaq", "load"],
)

def load_nasdaq_dag():
    
    @task
    def load_nasdaq():

        service = LoadNasdaq()
        service.main()

    load_nasdaq()


load_nasdaq_dag()