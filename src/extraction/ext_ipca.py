import os
from datetime import date, datetime
from pathlib import Path
  
import pandas as pd
import requests


class ExtractIpca:
    
    TIPO = "IPCA"
    DATA_INICIAL = date(2000, 1, 1)
    
    
    def url(self):
        return "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
    
    def output_path(self):
        base_data = Path(f"data/downloads/bcb/ipca/ipca.csv")
        return base_data

    def periodos(self):
        hoje = date.today()
        periodos = []

        # Divide a consulta para evitar limites de periodo do SGS.
        for ano_inicial in range(self.DATA_INICIAL.year, hoje.year + 1, 10):
            inicio = date(ano_inicial, 1, 1)
            ano_final = min(ano_inicial + 9, hoje.year)
            fim = hoje if ano_final == hoje.year else date(ano_final, 12, 31)
            periodos.append((inicio, fim))

        return periodos

    def extract(self):
         
        todos_dados = []

        for data_inicial, data_final in self.periodos():
            parametros = {
                "formato": "json",
                "dataInicial": data_inicial.strftime("%d/%m/%Y"),
                "dataFinal": data_final.strftime("%d/%m/%Y"),
            }

            print(f"Consultando {self.TIPO}: {parametros['dataInicial']} ate {parametros['dataFinal']}")

            resposta = requests.get(
                self.url(),
                params=parametros,
                headers={"User-Agent": "cotacoes-moedas/1.0"},
                timeout=30,
            )
            resposta.raise_for_status()
            todos_dados.extend(resposta.json())

        if not todos_dados:
            raise RuntimeError("Nenhum dado retornado para o IPCA.")

        dados = pd.DataFrame(todos_dados)
        datas = pd.to_datetime(dados["data"], format="%d/%m/%Y")

        resultado = pd.DataFrame(
            {
                "tipo": self.TIPO,
                "codigo_serie": 433,
                "data": datas.dt.strftime("%Y-%m-%d"),
                "ano": datas.dt.year,
                "valor_percentual": pd.to_numeric(dados["valor"].astype(str).str.replace(",", ".", regex=False),errors="coerce",),
                "periodicidade": "MENSAL",
                "fonte": "Banco Central do Brasil - SGS",
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
    ExtractIpca().main()
