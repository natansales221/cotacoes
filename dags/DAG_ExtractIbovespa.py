import pendulum

from airflow.sdk import dag, task

from src.extraction.ext_ibovespa import ExtractIbovespa


@dag(
    dag_id="DAG_ExtractIbovespa",
    schedule="20 6 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "extract", "ibovespa"],
)
def ibovespa_pipeline():

    @task
    def extract_ibovespa():

        service = ExtractIbovespa()

        service.main()

    extract_ibovespa()


ibovespa_pipeline()