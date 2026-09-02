import pendulum

from airflow.sdk import dag, task

from src.extraction.ext_ipca import ExtractIpca

@dag(
    dag_id="DAG_ExtractIPCA",
    schedule="30 6 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "ipca", "extract"],
)
def ipca_pipeline():

    @task
    def extract_ipca():

        service = ExtractIpca()

        service.main()

    extract_ipca()


ipca_pipeline()