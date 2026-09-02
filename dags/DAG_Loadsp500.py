import pendulum

from airflow.sdk import dag, task

from src.load.load_sp500 import LoadSnP

@dag(
    dag_id="DAG_LoadSnP",
    schedule="50 7 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "SnP", "load"],
)

def load_snp_dag():
    
    @task
    def load_snp():

        service = LoadSnP()
        service.main()

    load_snp()


load_snp_dag()