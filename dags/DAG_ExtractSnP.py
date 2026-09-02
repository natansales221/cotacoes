import pendulum

from airflow.sdk import dag, task

from src.extraction.ext_sp500 import ExtractSP500

@dag(
    dag_id="DAG_ExtractSP500",
    schedule="50 6 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "SnP", "extract"],
)
def snp_pipeline():

    @task
    def extract_snp():

        service = ExtractSP500()

        service.main()

    extract_snp()


snp_pipeline()