import pendulum

from airflow.sdk import dag, task

from src.load.load_ibovespa import LoadIbovespa

@dag(
    dag_id="DAG_LoadIbovespa",
    schedule="10 7 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "ibovespa", "load"],
)

def load_ibovespa_dag():
    
    @task
    def load_ibovespa():

        service = LoadIbovespa()
        service.main()

    load_ibovespa()


load_ibovespa_dag()