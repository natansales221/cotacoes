import pendulum

from airflow.sdk import dag, task

from src.load.load_currency import LoadCurrency

@dag(
    dag_id="DAG_LoadCurrency",
    schedule="0 7 * * 1-5", 
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="America/Sao_Paulo"
    ),
    catchup=False,
    tags=["dev", "load", "currency"],
)

def load_currency_dag():
    
    @task
    def load_currency():

        service = LoadCurrency()
        service.main()

    load_currency()



load_currency_dag()