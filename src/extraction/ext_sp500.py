import os
from datetime import date, datetime, timedelta
from pathlib import Path
  
import pandas as pd
import yfinance as yf


class ExtractSP500:
    TICKER = "^GSPC"
    TIPO = "SP500"
    DATA_INICIAL = "2000-01-01"

    def output_path(self):
        base_data = Path(f"data/downloads/yfinance/sp500/sp500.csv")
        return base_data

    def extract(self):
        data_final_exclusiva = (date.today() + timedelta(days=1)).isoformat()

        dados = yf.download(
            self.TICKER,
            start=self.DATA_INICIAL,
            end=data_final_exclusiva,
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=False,
            timeout=30,
        )

        if dados.empty:
            raise RuntimeError(f"Nenhum dado retornado para {self.TICKER}.")

        if isinstance(dados.columns, pd.MultiIndex):
            dados.columns = dados.columns.get_level_values(0)

        dados = dados.reset_index()
        coluna_data = "Date" if "Date" in dados.columns else "Datetime"
        datas = pd.to_datetime(dados[coluna_data])

        resultado = pd.DataFrame(
            {
                "tipo": self.TIPO,
                "ticker": self.TICKER,
                "data": datas.dt.strftime("%Y-%m-%d"),
                "ano": datas.dt.year,
                "abertura": pd.to_numeric(dados.get("Open"), errors="coerce"),
                "maxima": pd.to_numeric(dados.get("High"), errors="coerce"),
                "minima": pd.to_numeric(dados.get("Low"), errors="coerce"),
                "fechamento": pd.to_numeric(dados.get("Close"), errors="coerce"),
                "fechamento_ajustado": pd.to_numeric(
                    dados.get("Adj Close", dados.get("Close")), errors="coerce"
                ),
                "volume": pd.to_numeric(dados.get("Volume"), errors="coerce"),
                "fonte": "Yahoo Finance via yfinance",
                "dt_carga": datetime.now().isoformat(timespec="seconds"),
            }
        )

        return resultado.drop_duplicates(subset=["tipo", "data"]).sort_values("data")

    def main(self):
         
        arquivo_saida = self.output_path()
        arquivo_saida.parent.mkdir(parents=True, exist_ok=True)

        dados = self.extract()
        dados.to_csv(arquivo_saida, index=False, encoding="utf-8", float_format="%.6f")

        print(f"{len(dados)} registros de {self.TIPO} salvos em: {arquivo_saida}")


if __name__ == "__main__":
    ExtractSP500().main()
