import os
import sqlite3
from pathlib import Path


class TransformCurrency:

    def database_path(self):

        base_data = Path(f"data/database/database.db")

        return base_data

    def sql_path(self):

        pasta_sql = Path(__file__).parent

        return [
            pasta_sql / "fact_cotacao_diaria.sql",
            pasta_sql / "vw_variacao_diaria.sql",
        ]

    def main(self):
         
                
        print("=" * 60)
        print("INÍCIO DA TRANSFORMAÇÃO")
        print("=" * 60)
    
        database = self.database_path()

        conn = sqlite3.connect(database)
        print("DATABASE CONNECTED")

        try:

            cursor = conn.cursor()

            for arquivo_sql in self.sql_path():

                print(f"Executando: {arquivo_sql.name}")

                with open(arquivo_sql, "r", encoding="utf-8") as arquivo:

                    sql = arquivo.read()

                cursor.executescript(sql)

                print(f"{arquivo_sql.name} executado com sucesso!")

            conn.commit()

        finally:

            conn.close()


if __name__ == "__main__":

    service = TransformCurrency()
    service.main()