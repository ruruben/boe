from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

url = 'https://subastas.boe.es/subastas_ava.php?campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D=EJ&campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=I&campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D=29&campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&page_hits=40&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

subastas = soup.find_all('li', class_='resultado-busqueda')

casasHtml = list()
casasWeb = list()
casasTexto = list()
casasTitulo = list()
casasJuzagdo = list()
casasExpediente = list()
casasEstado = list()
def regexValues(r):
    if r is None:
        return None
    else:
        return r.group(0).replace("\n", "").replace("  ", "")


for i in subastas:
    web = regexValues(re.search(r"href=\"[^\"]*", str(i))).replace("href=\".", "https://subastas.boe.es")
    pagew = requests.get(web)
    soupw = BeautifulSoup(pagew.content, 'html.parser')
    subastasw = soupw.find_all('tr')
    lotesw = re.search(r"href=.*(?=\">Lotes[<\a>]*)", str(soupw.find_all('li'))).group(0).replace("href=\".", "https://subastas.boe.es")

    soupww = BeautifulSoup(requests.get(lotesw).content, 'html.parser')
    subastasww = soupw.find_all('tr')

    casasTitulo.append(regexValues(re.search(r"<h3>[^<\\h3>]*", str(i))))
    casasJuzagdo.append(regexValues(re.search(r"<h4>[^<\\h4>]*", str(i))))
    casasExpediente.append(regexValues(re.search(r"Expediente:.*[0-9]*/[0-9]*", str(i))))
    casasEstado.append(regexValues(re.search(r"Estado:.*[^<\\p>]", str(i))))
    casasWeb.append(web)
    casasTexto.append(str(i.text).replace("\n", "").replace("  ", ""))
    casasHtml.append(str(i).replace("\n", "").replace("  ", ""))

df = pd.DataFrame({"titulo": casasTitulo, "juzgado": casasJuzagdo, "expediente": casasExpediente,
                   "estado": casasEstado, "web": casasWeb, "texto": casasTexto, "html": casasHtml})
print(df)
df.to_csv('output.csv', index=False)
