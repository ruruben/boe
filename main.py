from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import lote
from tqdm import tqdm
import datetime

mapUrls = {'Madrid': lote.urlMadrid, 'Malaga': lote.urlMalga}
for zone in mapUrls:
    start = datetime.datetime.now()
    subastas = lote.Subastas
    subastaDato = lote.SubastaDato
    lotes = lote.Lote
    url = mapUrls.get(zone)
    urls = lote.getUrlSubastas(url)
    print()
    print()
    print()
    print("City", zone)
    for urlFor in range(len(urls)+1):
        if urlFor == 0:
            subastasHTML = lote.getHtmlSubastas(url)
        else:
            subastasHTML = lote.getHtmlSubastas(urls[urlFor-1])
        for sub in subastasHTML:
            loteUrl = lote.regexValues(re.search(r"href=\"[^\"]*", str(sub))).replace("href=\".", "https://subastas.boe.es")
            subastas = lote.Subastas(sub, loteUrl)
            lotesHTML = BeautifulSoup(requests.get(loteUrl).content, 'html.parser')
            subastaDato = lote.SubastaDato(lotesHTML)
            hrmlLotes = re.search(r"href=.*(?=\">Lotes[<\a>]*)", str(lotesHTML.find_all('li')))
            if hrmlLotes is not None:
                lotesw = hrmlLotes.group(0).replace("href=\".", "https://subastas.boe.es")
                numLotes = int(lote.regexClean(r"Lotes</th><td>[^<//td>]*", lotesHTML)[14:])
                for l in tqdm(range(numLotes)):
                    loteUno = lotesw.replace('&amp;ver=3&amp;idBus=&amp;idLote=&amp;numPagBus=', '&ver=3&idLote={}&idBus=&numPagBus=#cont-tabs'.format(l+1))
                    html = BeautifulSoup(requests.get(loteUno).content, 'html.parser')
                    data = html.find_all('tr')
                    lotes = lote.Lote(html)
    pd.DataFrame({"identificador": subastas.identificador,
                  "juzgado": subastas.casasJuzagdo,
                  "expediente": subastas.casasExpediente,
                  "estado": subastas.casasEstado,
                  "web": subastas.casasWeb,
                  "texto": subastas.casasTexto,
                  "html": subastas.casasHtml}).to_csv('./{}/subastas.csv'.format(zone), index=False)

    pd.DataFrame({"identificador": subastaDato.identificador,
                  "tipo_subasta": subastaDato.tipoSubasta,
                  "cantidad_reclamada": subastaDato.cantidadReclamada,
                  "lotes": subastaDato.lotes,
                  "valor_subasta": subastaDato.valorSubasta,
                  "tasacion": subastaDato.tasacion,
                  "tramos_entre_pujas": subastaDato.tramosEntrePujas,
                  "importe_deposito": subastaDato.importeDeposito,
                  "fecha_inicio": subastaDato.fechaInicio,
                  "fecha_fin": subastaDato.fechaFin,
                  "anuncio_BOE": subastaDato.anuncioBoe,
                  "forma_Adjudicacion": subastaDato.formaAdjudicacion,
                  "puja_minima": subastaDato.pujaMinima}).to_csv("./{}/subastaDato.csv".format(zone), index=False)

    lot = pd.DataFrame({"identificador": lotes.identificador,
                        "valor_subasta": lotes.valorSubasta,
                        "importe_deposito": lotes.importeDeposito,
                        "tramos_entre_pujas": lotes.tramosEntrePujas,
                        "puja_minima": lotes.pujaMinima,
                        "direccion": lotes.direccion,
                        "provincia": lotes.provincia,
                        "localidad": lotes.localidad,
                        "codigo_postal": lotes.codigoPostal,
                        "descripcion": lotes.descripcion,
                        "situacion_posesoria": lotes.situacionPosesoria,
                        "visitable": lotes.visitable,
                        "inscripcion_registral": lotes.inscripcionRegistral,
                        "idufir": lotes.idufir})
    lot.query("valor_subasta >= 140000 & valor_subasta <= 200000") \
        .to_csv("./{}/lotes.csv".format(zone), index=False)
    print("Has been processed", lot.size, "lots.")

    end = datetime.datetime.now() # time object
    d = end-start
    print("Time start: ", start)
    print("Time end: ",  end)
    print("Duration: ",  d)
