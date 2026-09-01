import pendulum

from airflow.sdk import dag, task

from src.transformation.transform_currency import TransformCurrency

@dag(
    dag_id="DAG_TransformCurrency",
    schedule="0 8 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "transform", "currency"],
)

def transform_currency_dag():
    
    @task
    def transform_currency():

        service = TransformCurrency()
        service.main()

    transform_currency()


transform_currency_dag()