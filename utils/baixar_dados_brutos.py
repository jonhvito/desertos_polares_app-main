import requests
import os


urls = [
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-82.5&longitude=-180&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MDEW,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-82.5&longitude=-90&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MDEW,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-82.5&longitude=0&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MDEW,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-82.5&longitude=90&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MDEW,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-82.5&longitude=180&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MDEW,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-79.17&longitude=-180&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MDEW,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-79.17&longitude=-90&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MDEW,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-79.17&longitude=0&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MDEW,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-79.17&longitude=90&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-79.17&longitude=180&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-75.83&longitude=-180&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-75.83&longitude=-90&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-75.83&longitude=0&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-75.83&longitude=90&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-75.83&longitude=180&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-72.5&longitude=-180&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-72.5&longitude=-90&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-72.5&longitude=0&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-72.5&longitude=90&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MWET",
    "https://power.larc.nasa.gov/api/temporal/monthly/point?start=2000&end=2023&latitude=-72.5&longitude=180&community=RE&format=CSV&parameters=ALLSKY_SFC_SW_DWN,WS10M,T2M,RH2M,PRECTOTCORR,PS,T2M_MAX,T2M_MIN,T2MWET"
]

# Pasta onde os arquivos serão salvos
pasta_destino = "downloads"
os.makedirs(pasta_destino, exist_ok=True)


# Função para baixar os arquivos com nome personalizado
def baixar_arquivo(url, pasta):
    # Extrai latitude e longitude da URL para criar o nome do arquivo
    lat = url.split("latitude=")[1].split("&")[0]
    lon = url.split("longitude=")[1].split("&")[0]
    nome_arquivo = f"data_lat_{lat}_lon_{lon}.csv"
    caminho_completo = os.path.join(pasta, nome_arquivo)

    print(f"Baixando {nome_arquivo}...")
    resposta = requests.get(url, stream=True)

    with open(caminho_completo, 'wb') as arquivo:
        for chunk in resposta.iter_content(chunk_size=8192):
            if chunk:
                arquivo.write(chunk)
    print(f"Concluído: {nome_arquivo}")


# Baixa todos os arquivos
for url in urls:
    baixar_arquivo(url, pasta_destino)

print("Todos os downloads concluídos!")