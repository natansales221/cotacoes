import sqlite3
import os
import hashlib
import pandas as pd
from datetime import datetime
from pathlib import Path


class LoadSelic():
    
    def database_path(self):
    
        return Path("data/database/database.db")

    def downloads_path(self):

        return Path("data/downloads/yfinance/ibovespa")
    
    def criar_tabela(self, cursor):
    
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ibovespa
                (
                    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo                  TEXT NOT NULL,
                    ticker                TEXT NOT NULL,
                    data                  TEXT NOT NULL,
                    ano                   INTEGER NOT NULL,
                    abertura              REAL,
                    maxima                REAL,
                    minima                REAL,
                    fechamento            REAL,
                    fechamento_ajustado   REAL,
                    volume                INTEGER,
                    fonte                 TEXT,
                    dt_carga              TEXT NOT NULL,
                    record_hash           TEXT NOT NULL UNIQUE
                );
            """
        )
        
    def gerar_hash(self, row):
    
        conteudo = (f"{row['tipo']}|{row['ticker']}|{row['fechamento']}")

        return hashlib.sha256(conteudo.encode("utf-8")).hexdigest()
    
    def main(self):
    
        print("=" * 60)
        print("INÍCIO DA CARGA IBOVESPA")
        print("=" * 60)

        database = self.database_path()
        pasta_ibovespa = self.downloads_path()

        print(f"Database: {database}")
        print(f"Diretório dos arquivos: {pasta_ibovespa}")
        
        if not database.parent.exists():
    
            raise FileNotFoundError(f"Diretório do banco não encontrado: {database.parent}")

        if not pasta_ibovespa.exists():

            raise FileNotFoundError(f"Diretório ibovespa não encontrado: {pasta_ibovespa}")

        arquivos = sorted(pasta_ibovespa.glob("*.csv"))
        
        if not arquivos:
    
            raise FileNotFoundError(f"Nenhum arquivo CSV encontrado em: {pasta_ibovespa}")

        conn = sqlite3.connect(database)

        print("DATABASE CONNECTED")

        try:
            cursor = conn.cursor()
            self.criar_tabela(cursor)
            conn.commit()
            for arquivo_csv in arquivos:

                print(f"Lendo arquivo: {arquivo_csv.name}")

                df = pd.read_csv(arquivo_csv)

                if df.empty:

                    print(f"{arquivo_csv.name} | arquivo vazio")

                    continue

                total_lidos = len(df)

                df = df.dropna(subset=["dt_carga"])

                rejeitados = total_lidos - len(df)

                df["record_hash"] = df.apply(self.gerar_hash, axis=1)

                df["dt_carga"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                df_load = df[
                    ['tipo', 'ticker', 'data', 'ano', 'abertura', 'maxima', 'minima',
                    'fechamento', 'fechamento_ajustado', 'volume', 'fonte', 'dt_carga',
                    'record_hash']].drop_duplicates(
                    subset=["record_hash"])

                registros = list( df_load.itertuples(index=False,name=None))

                total_antes = conn.total_changes

                cursor.executemany(
                    """
                    INSERT OR IGNORE INTO ibovespa
                    (
                        tipo,
                        ticker,
                        data,
                        ano,
                        abertura,
                        maxima,
                        minima,
                        fechamento,
                        fechamento_ajustado,
                        volume,
                        fonte,
                        dt_carga,
                        record_hash
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    registros
                )

                conn.commit()

                inseridos = (conn.total_changes - total_antes)

                existentes = (len(df_load) - inseridos)

                print(
                    f"{arquivo_csv.name} | "
                    f"lidos={total_lidos} | "
                    f"válidos={len(df_load)} | "
                    f"inseridos={inseridos} | "
                    f"já existentes={existentes} | "
                    f"rejeitados={rejeitados}"
                )

            print("=" * 60)
            print("CARGA IBOVESPA FINALIZADA")
            print("=" * 60)

        except Exception:

            conn.rollback()

            print("Erro durante a carga da Selic")

            raise

        finally:

            conn.close()

            print("DATABASE CLOSED")

        
if __name__ == "__main__":
    service = LoadSelic()
    service.main()