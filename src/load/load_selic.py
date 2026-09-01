import sqlite3
import os
import hashlib
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path


class LoadSelic():
    
    def database_path(self):
    
        return Path("data/database/database.db")

    def downloads_path(self):

        return Path("data/downloads/selic")
    
    def criar_tabela(self, cursor):
    
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS selic
            (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                moeda           TEXT NOT NULL,
                dt_cotacao      TEXT NOT NULL,
                vl_cotacao      REAL NOT NULL,
                dt_carga        TEXT NOT NULL,
                record_hash     TEXT NOT NULL UNIQUE
            )
            """
        )
        
    def gerar_hash(self, row):
    
        conteudo = (f"{row['dt_cotacao']}|{row['vl_cotacao']}")

        return hashlib.sha256(conteudo.encode("utf-8")).hexdigest()
    
    def main(self):
    
        logger = logging.getLogger(__name__)

        logger.info("=" * 60)
        logger.info("INÍCIO DA CARGA DA SELIC")
        logger.info("=" * 60)

        database = self.database_path()
        pasta_selic = self.downloads_path()

        logger.info(f"Database: {database}")
        logger.info(f"Diretório dos arquivos: {pasta_selic}")
        
        if not database.parent.exists():
    
            raise FileNotFoundError(f"Diretório do banco não encontrado: {database.parent}")

        if not pasta_selic.exists():

            raise FileNotFoundError(f"Diretório da Selic não encontrado: {pasta_selic}")

        arquivos = sorted(pasta_selic.glob("*.csv"))
        
        if not arquivos:
    
            raise FileNotFoundError(f"Nenhum arquivo CSV encontrado em: {pasta_selic}")

        conn = sqlite3.connect(database)

        logger.info("DATABASE CONNECTED")

        try:
            cursor = conn.cursor()
            self.criar_tabela(cursor)
            conn.commit()
            for arquivo_csv in arquivos:

                logger.info(f"Lendo arquivo: {arquivo_csv.name}")

                df = pd.read_csv(arquivo_csv)

                if df.empty:

                    logger.warning(f"{arquivo_csv.name} | arquivo vazio")

                    continue

                colunas_obrigatorias = {
                    "data",
                    "valor"
                }

                colunas_ausentes = (colunas_obrigatorias - set(df.columns))

                if colunas_ausentes:

                    raise ValueError(f"{arquivo_csv.name} possui colunas ausentes: {sorted(colunas_ausentes)}")

                df = df.rename(
                    columns={
                        "data": "dt_cotacao",
                        "valor": "vl_cotacao"
                    }
                )

                df["moeda"] = "Selic"

                df["dt_cotacao"] = pd.to_datetime(df["dt_cotacao"], format="%d/%m/%Y", errors="coerce").dt.strftime("%Y-%m-%d")

                df["vl_cotacao"] = pd.to_numeric(df["vl_cotacao"].astype(str).str.replace(",",  ".", regex=False),errors="coerce")

                total_lidos = len(df)

                df = df.dropna(subset=["dt_cotacao", "vl_cotacao"])

                rejeitados = total_lidos - len(df)

                df["record_hash"] = df.apply(self.gerar_hash, axis=1)

                df["dt_carga"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                df_load = df[
                    [
                        "moeda",
                        "dt_cotacao",
                        "vl_cotacao",
                        "dt_carga",
                        "record_hash"
                    ]].drop_duplicates(
                    subset=["record_hash"])

                registros = list( df_load.itertuples(index=False,name=None))

                total_antes = conn.total_changes

                cursor.executemany(
                    """
                    INSERT OR IGNORE INTO selic
                    (
                        moeda,
                        dt_cotacao,
                        vl_cotacao,
                        dt_carga,
                        record_hash
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    registros
                )

                conn.commit()

                inseridos = (conn.total_changes - total_antes)

                existentes = (len(df_load) - inseridos)

                logger.info(
                    f"{arquivo_csv.name} | "
                    f"lidos={total_lidos} | "
                    f"válidos={len(df_load)} | "
                    f"inseridos={inseridos} | "
                    f"já existentes={existentes} | "
                    f"rejeitados={rejeitados}"
                )

            logger.info("=" * 60)
            logger.info("CARGA DA SELIC FINALIZADA")
            logger.info("=" * 60)

        except Exception:

            conn.rollback()

            logger.exception("Erro durante a carga da Selic")

            raise

        finally:

            conn.close()

            logger.info("DATABASE CLOSED")

        
if __name__ == "__main__":
    service = LoadSelic()
    service.main()