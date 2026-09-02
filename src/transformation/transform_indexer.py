import sqlite3

from pathlib import Path


class TransformIndexer:

    def database_path(self):

        return Path("data/database/database.db")

    def sql_paths(self):

        pasta_sql = Path(__file__).parent

        return {
            "dim_indexador": pasta_sql / "dim_indexador.sql",
            "fact_indexador": pasta_sql / "fact_indexador.sql"
        }

    def main(self):

        print("=" * 60)
        print("INÍCIO DA TRANSFORMAÇÃO DOS INDEXADORES")
        print("=" * 60)

        database = self.database_path()
        arquivos_sql = self.sql_paths()

        print(f"Database: {database}")

        if not database.exists():

            raise FileNotFoundError(
                f"Database não encontrado: {database}"
            )

        conn = sqlite3.connect(database)

        print("DATABASE CONNECTED")

        try:

            cursor = conn.cursor()

            for nome_transformacao, arquivo_sql in arquivos_sql.items():

                if not arquivo_sql.exists():

                    raise FileNotFoundError(
                        f"Arquivo SQL não encontrado: {arquivo_sql}"
                    )

                print("-" * 60)
                print(f"Executando transformação: {nome_transformacao}")
                print(f"Arquivo SQL: {arquivo_sql.name}")

                with open(
                    arquivo_sql,
                    "r",
                    encoding="utf-8"
                ) as arquivo:

                    sql = arquivo.read()

                cursor.executescript(sql)

                print(f"{nome_transformacao} criada com sucesso")

            conn.commit()

            print("=" * 60)
            print("TRANSFORMAÇÃO DOS INDEXADORES FINALIZADA")
            print("=" * 60)

        except Exception as erro:

            conn.rollback()

            print(f"Erro durante a transformação: {erro}")

            raise

        finally:

            conn.close()

            print("DATABASE CLOSED")


if __name__ == "__main__":

    service = TransformIndexer()
    service.main()