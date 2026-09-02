import pendulum

from airflow.sdk import dag, task

from src.load.load_ipca import LoadIpca

@dag(
    dag_id="DAG_LoadIpca",
    schedule="30 7 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "ipca", "load"],
)

def load_ipca_dag():
    
    @task
    def load_ipca():

        service = LoadIpca()
        service.main()

    load_ipca()


load_ipca_dag()