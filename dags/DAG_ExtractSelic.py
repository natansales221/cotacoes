import pendulum

from airflow.sdk import dag, task

from src.extraction.ext_selic import ExtractSelic


@dag(
    dag_id="DAG_ExtractCurrency",
    schedule=None,
    start_date=pendulum.datetime( 2026,1,1,tz="America/Sao_Paulo"),
    catchup=False,
    tags=["dev", "currency"],
)
def currency_pipeline():

    @task
    def extract_currency():

        service = ExtractSelic()

        service.main()

    extract_currency()


currency_pipeline()