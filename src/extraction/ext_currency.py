from pathlib import Path
from datetime import datetime
import pandas as pd
import requests
  
from src.utils.utilidades import logs

class ExtractCurrency():
    
    # URL to search currency
    def url():
        return "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"

    # creating path to download the file
    def path(self, moeda):
        return Path(f"data/downloads/ptax/{moeda}")
    
    # Extracting wished currency since 2000's
    def main(self):
         
        
        print("=" * 60)
        print("INÍCIO DA EXTRAÇÃO PTAX")
        print("=" * 60)
        
        ano_atual = datetime.now().year
        lista_moedas = ["AUD", "CAD", "CHF", "DKK", "EUR", "GBP", "JPY", "NOK", "SEK", "USD"]
        for moeda in lista_moedas:
            for ano in range(2000, ano_atual + 1):
                print("=" * 60)
                print(f"Iniciando extração: moeda={moeda}, ano={ano}")
                PARAMS = {
                    "@moeda": f"'{moeda}'",
                    "@dataInicial": f"'01-01-{ano}'",
                    "@dataFinalCotacao": f"'12-31-{ano}'",
                    "$top": 100000,
                    "$format": "json",
                    "$select": "cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim"
                }

                response = requests.get(ExtractCurrency.url(), params=PARAMS, timeout=30)
                response.raise_for_status()
                print(f"Consulta feita com sucesso!")
                dados = response.json()["value"]

                df = pd.DataFrame(dados)
                
                print(f"Dataframe criado com sucesso")
                
                destino = self.path(moeda)
                destino.mkdir(parents=True, exist_ok=True)
                print(f"Pasta criada com sucesso")
                arquivo = destino / f"ptax_{moeda}_{ano}.csv"

                df.to_csv(arquivo, index=False, encoding="utf-8")
                
                print("Extração concluída")
                print(f"Foram extraídos {len(df)} registros")
                print("=" * 60)

        print("=" * 60)
        print("FIM DA EXTRAÇÃO PTAX")
        print("=" * 60)
    
if __name__ == "__main__":
    service=ExtractCurrency()
    service.main()
    
