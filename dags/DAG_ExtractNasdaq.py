import pendulum

from airflow.sdk import dag, task

from src.extraction.ext_nasdaq import ExtractNasdaq


@dag(
    dag_id="DAG_ExtractNasdaq",
    schedule="40 6 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "nasdaq", "extract"],
)
def nasdaq_pipeline():

    @task
    def extract_nasdaq():

        service = ExtractNasdaq()

        service.main()

    extract_nasdaq()


nasdaq_pipeline()