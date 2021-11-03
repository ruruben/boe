from bs4 import BeautifulSoup
import re
import requests

urlMalga = 'https://subastas.boe.es/subastas_ava.php?campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D=EJ&campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=I&campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D=29&campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&page_hits=40&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar'
urlMadrid = 'https://subastas.boe.es/subastas_ava.php?campo%5B1%5D=SUBASTA.ESTADO&dato%5B1%5D=EJ&campo%5B2%5D=BIEN.TIPO&dato%5B2%5D=I&campo%5B7%5D=BIEN.COD_PROVINCIA&dato%5B7%5D=28&campo%5B16%5D=SUBASTA.FECHA_INICIO_YMD&dato%5B16%5D%5B0%5D=&dato%5B16%5D%5B1%5D=&page_hits=40&sort_field%5B0%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B0%5D=desc&sort_field%5B1%5D=SUBASTA.FECHA_FIN_YMD&sort_order%5B1%5D=asc&sort_field%5B2%5D=SUBASTA.HORA_FIN&sort_order%5B2%5D=asc&accion=Buscar'

class Subastas:
    identificador = list()
    casasJuzagdo = list()
    casasExpediente = list()
    casasEstado = list()
    casasWeb = list()
    casasTexto = list()
    casasHtml = list()

    def __init__(self, subasta, web):
        self.identificador.append(regexClean(r"<h3>[^<\\h3>]*", subasta)[12:])
        self.casasJuzagdo.append(regexClean(r"<h4>[^<\\h4>]*", subasta)[4:])
        self.casasExpediente.append(regexClean(r"Expediente:[^<\\p>]*", subasta)[12:])
        self.casasEstado.append(regexClean(r"Estado:[^<\\]*", subasta)[8:])
        self.casasWeb.append(web)
        self.casasTexto.append(str(subasta.text).replace("\n", "").replace("  ", ""))
        self.casasHtml.append(str(subasta).replace("\n", "").replace("  ", ""))


class SubastaDato:
    identificador = list()
    tipoSubasta = list()
    fechaInicio = list()
    fechaFin = list()
    cantidadReclamada = list()
    lotes = list()
    formaAdjudicacion = list()
    anuncioBoe = list()
    valorSubasta = list()
    tasacion = list()
    pujaMinima = list()
    tramosEntrePujas = list()
    importeDeposito = list()

    def __init__(self, data):
        self.identificador.append(regexClean(r"Identificador</th><td><strong>[^<//]*", data)[30:])
        self.tipoSubasta.append(regexClean(r"Tipo de subasta</th><td><strong>[^<//]*", data)[32:])
        self.fechaInicio.append(regexClean(r"Fecha de inicio</th><td>[^<//td>]*CET", data)[24:])
        self.fechaFin.append(regexClean(r"Fecha de conclusión</th><td><strong class=\"destaca\">[^<//]*", data)[52:])
        self.cantidadReclamada.append(values(regexClean(r"Cantidad reclamada</th><td>[^<//]*", data)[27:]))
        self.lotes.append(regexClean(r"Lotes</th><td>[^<\>]*", data)[14:])
        self.formaAdjudicacion.append(regexClean(r"Forma adjudicación</th><td>[^<//]*", data)[27:])
        self.anuncioBoe.append(regexClean(r"Anuncio BOE</th><td>[^<\>]*", data)[20:])
        self.valorSubasta.append(values(regexClean(r"Valor subasta</th><td>[^<\>]*", data)[22:]))
        self.tasacion.append(values(regexClean(r"Tasación</th><td>[^<\>]*", data)[21:]))
        self.pujaMinima.append(regexClean(r"Puja mínima</th><td>[^<\>]*", data)[20:])
        self.tramosEntrePujas.append(values(regexClean(r"Tramos entre pujas</th><td>[^<\>]*", data)[27:]))
        self.importeDeposito.append(values(regexClean(r"Importe del depósito</th><td>[^<\>]*", data)[29:]))


class Lote:
    identificador = list()
    valorSubasta = list()
    importeDeposito = list()
    pujaMinima = list()
    tramosEntrePujas = list()
    descripcion = list()
    idufir = list()
    direccion = list()
    codigoPostal = list()
    localidad = list()
    provincia = list()
    situacionPosesoria = list()
    visitable = list()
    inscripcionRegistral = list()

    def __init__(self, data):
            self.identificador.append(regexClean(r"<div id=\"contenido\"><h2>[^<//]*", data)[32:])
            self.valorSubasta.append(values(regexClean(r"Valor Subasta</th><td>[^<//td>]*", data)[22:]))
            self.importeDeposito.append(values(regexClean(r"Importe del depósito</th><td>[^<//td>]*", data)[29:]))
            self.pujaMinima.append(values(regexClean(r"Puja mínima</th><td>[^<//td>]*", data)[20:]))
            self.tramosEntrePujas.append(values(regexClean(r"Tramos entre pujas</th><td>[^<//td>]*", data)[27:]))
            self.descripcion.append(regexClean(r"Descripción</th><td>[^<\>]*", data)[20:])
            self.idufir.append(regexClean(r"IDUFIR</th><td>[^<\>]*", data)[15:])
            self.direccion.append(regexClean(r"Dirección</th><td>[^<\>]*", data)[18:])
            self.codigoPostal.append(regexClean(r"Código Postal</th><td>[^<\>]*", data)[22:])
            self.localidad.append(regexClean(r"Localidad</th><td>[^<\>]*", data)[18:])
            self.provincia.append(regexClean(r"Provincia</th><td>[^<\>]*", data)[18:])
            self.situacionPosesoria.append(regexClean(r"Situación posesoria</th><td>[^<\>]*", data)[28:])
            self.visitable.append(regexClean(r"Visitable</th><td>[^<\>]*", data)[18:])
            self.inscripcionRegistral.append(regexClean(r"Inscripción registral</th><td>[^<\>]*", data)[30:])


def values(value):
    try:
        return float(value[:-2].replace(".", "").replace(",", "."))
    except:
        return None
    else:
        return None


def pagRegex(url):
    rege = re.search(r"id_busqueda=[^\">]*", str(url))
    if rege is None:
        return None
    else:
        return rege.group(0).replace("id_busqueda", "https://subastas.boe.es/subastas_ava.php?accion=Mas&id_busqueda")


def getUrlSubastas(url):
    paginas = BeautifulSoup(requests.get(url).content, 'html.parser').find('div', class_='paginar2').find_all('a')
    data = str(paginas).replace("[", "").replace("]", "").replace(", ", "").split("<a href=\"subastas_ava.php?accion=Mas&amp;")
    return list(set(filter(None, map(pagRegex, data))))


def regexClean(reg, data):
    rege = re.search(reg, str(data).replace("\n", "").replace("  ", ""))
    if rege is None:
        return ''
    else:
        return rege.group(0)


def regexValues(r):
    if r is None:
        return None
    else:
        return r.group(0).replace("\n", "").replace("  ", "")


def getHtmlSubastas(url):
    return BeautifulSoup(requests.get(url).content, 'html.parser').find_all('li', class_='resultado-busqueda')