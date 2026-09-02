import pendulum

from airflow.sdk import dag, task

from src.extraction.ext_ipca import ExtractIpca
from src.utils.utilidades import logs

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
    tags=["dev", "extract", "ipca"],
)
def ipca_pipeline():

    @task
    def extract_ipca():

        arquivo_log = logs()

        service = ExtractIpca()

        service.main(arquivo_log=arquivo_log)

    extract_ipca()


ipca_pipeline()