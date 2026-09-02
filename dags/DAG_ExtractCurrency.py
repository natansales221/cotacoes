import pendulum

from airflow.sdk import dag, task

from src.extraction.ext_currency import ExtractCurrency
from src.utils.utilidades import logs

@dag(
    dag_id="DAG_ExtractCurrency",
    schedule="0 6 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "currency", "extract"],
)
def currency_pipeline():

    @task
    def extract_currency():

        service = ExtractCurrency()
        service.main()

    extract_currency()


currency_pipeline()