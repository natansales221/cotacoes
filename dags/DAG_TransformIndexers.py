import pendulum

from airflow.sdk import dag, task

from src.transformation.transform_indexer import TransformIndexer

@dag(
    dag_id="DAG_TransformIndexer",
    schedule="10 8 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "indexer", "transform"],
)

def transform_indexer_dag():
    
    @task
    def transform_indexer():

        service = TransformIndexer()
        service.main()

    transform_indexer()


transform_indexer_dag()