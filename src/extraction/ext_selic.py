import requests
import os
  
from datetime import datetime
import pandas as pd


class ExtractSelic():
    
    def nomes_arquivos(self):
        return {'selic': "selic.csv"}
    
    def url(self):
        return {
            "api_bcb": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1178/dados",
            "diretorio_download": r'data\downloads\selic'
                }
        
    def periodos(self):
        return [
        ("01/01/2000", "31/12/2009"),
        ("01/01/2010", "31/12/2019"),
        ("01/01/2020", "31/12/2026")
    ]
    def main(self):
         
        print("Iniciando processo")
        
        todos_dados = []

        for data_inicial, data_final in self.periodos():

            print(f"Consultando: {data_inicial} até {data_final}")

            parametros = {"formato": "json","dataInicial": data_inicial,"dataFinal": data_final}

            resposta = requests.get(self.url()['api_bcb'],params=parametros, headers={"User-Agent": "Mozilla/5.0"})

            if resposta.status_code != 200:
                print(f"Erro na consulta: {resposta.status_code}")
                print(resposta.text)
                exit()

            dados = resposta.json()

            todos_dados.extend(dados)

            print(f"Registros encontrados: {len(dados)}")


        os.makedirs(self.url()['diretorio_download'], exist_ok=True)

        caminho_arquivo = os.path.join(self.url()['diretorio_download'], self.nomes_arquivos()['selic'])

        df = pd.DataFrame(todos_dados)
        df.to_csv(caminho_arquivo, index=False, encoding="utf-8")

        print("CSV criado com sucesso!")
        print(f"Total de registros: {len(todos_dados)}")


if __name__ == "__main__":
    service = ExtractSelic()
    service.main()