import pendulum

from airflow.sdk import dag, task

from src.extraction.ext_currency import Extraction
from src.utils.utilidades import logs

@dag(
    dag_id="DAG - Extract",
    schedule=None,
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "currency"],
)
def currency_pipeline():

    @task
    def extract_currency():

        arquivo_log = logs()

        service = Extraction()

        service.main(arquivo_log=arquivo_log)

    extract_currency()


currency_pipeline()