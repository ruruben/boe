from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

import lote


subastas = lote.Subastas
subastaDato = lote.SubastaDato
lotes = lote.Lote

subastaBoeUrl = 'https://subastas.boe.es/'
#subastaBoeHTML = BeautifulSoup(requests.get(subastaBoeUrl).content, 'html.parser').find_all('area')
#url2 = lote.regexClean(r"href=\"[^\"]*", lote.regexClean(r"<area alt=\"M.laga[^\>]*", str(subastaBoeHTML))).replace("href=\"", subastaBoeUrl)
#urlBarcelona = 'https://subastas.boe.es/subastas_ava.php?campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D=EJ&campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=I&campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D=08&campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&page_hits=40&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar'
url = 'https://subastas.boe.es/subastas_ava.php?campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D=EJ&campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=I&campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D=29&campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&page_hits=40&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar'
urls = lote.getUrlSubastas(url)
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
            for l in range(numLotes):
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
              "html": subastas.casasHtml}).to_csv('./data/subastas.csv', index=False)

pd.DataFrame({"identificador": subastaDato.identificador,
              "tipo_subasta": subastaDato.tipoSubasta,
              "fecha_inicio": subastaDato.fechaInicio,
              "fecha_fin": subastaDato.fechaFin,
              "cantidad_reclamada": subastaDato.cantidadReclamada,
              "lotes": subastaDato.lotes,
              "forma_Adjudicacion": subastaDato.formaAdjudicacion,
              "anuncio_BOE": subastaDato.anuncioBoe,
              "valor_subasta": subastaDato.valorSubasta,
              "tasacion": subastaDato.tasacion,
              "puja_minima": subastaDato.pujaMinima,
              "tramos_entre_pujas": subastaDato.tramosEntrePujas,
              "importe_deposito": subastaDato.importeDeposito}).to_csv("./data/subastaDato.csv", index=False)

pd.DataFrame({"identificador": lotes.identificador,
              "valor_subasta": lotes.valorSubasta,
              "descripcion": lotes.descripcion,
              "importe_deposito": lotes.importeDeposito,
              "tramos_entre_pujas": lotes.tramosEntrePujas,
              "puja_minima": lotes.pujaMinima,
              "direccion": lotes.direccion,
              "provincia": lotes.provincia,
              "localidad": lotes.localidad,
              "codigo_postal": lotes.codigoPostal,
              "situacion_posesoria": lotes.situacionPosesoria,
              "visitable": lotes.visitable,
              "inscripcion_registral": lotes.inscripcionRegistral,
              "idufir": lotes.idufir}).to_csv("./data/lotes.csv", index=False)