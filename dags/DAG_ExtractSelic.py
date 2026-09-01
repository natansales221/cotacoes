import pendulum

from airflow.sdk import dag, task

from src.extraction.ext_selic import ExtractSelic


@dag(
    dag_id="DAG_ExtractSelic",
    schedule=None,
    start_date=pendulum.datetime( 2026,1,1,tz="America/Sao_Paulo"),
    catchup=False,
    tags=["dev", "extract", "selic"],
)
def selic_pipeline():

    @task
    def extract_selic():

        service = ExtractSelic()

        service.main()

    extract_selic()


selic_pipeline()