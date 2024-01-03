"""
Este programa descarga la información de cuantas camas no UCI se encuentran ocupadas
en México de hospitales COVID.

La Red IRAG no tiene API, así que extraemoes el JSON dentro del HTML.
"""

import csv
from datetime import datetime, timedelta

import requests


def main():

    ayer = datetime.now() - timedelta(days=1)
    ayer_fecha = f"{ayer:%Y-%m-%d}"

    # Llamamos la primera URL con una sesión para generar cookies.
    primera_url = "https://www.gits.igg.unam.mx/red-irag-dashboard/reviewHome"
    session = requests.Session()
    session.get(primera_url)

    # En esta URL se encuentra la información que buscamos.
    segunda_url = "https://www.gits.igg.unam.mx/red-irag-dashboard/reviewStoryTrend"
    payload = {"date": ayer_fecha}

    # Aqui se encuentra el HTML que vamos a extraer.
    respuesta = session.post(segunda_url, data=payload).text

    # Primer día de datos
    primer_dia = datetime(2020, 3, 1)

    # ültimo día de datos
    ultimo_dia = datetime.today()

    diferencia_dias = (ultimo_dia - primer_dia).days

    datos = [["isodate", "hospitalizados"]]

    for i in range(diferencia_dias):

        fecha_temporal = "{:%Y-%m-%d}".format(primer_dia + timedelta(days=i))

        # No todas las fechas tienen valores.
        try:
            # Vamos a buscar los datos de la fecha de la iteración.
            inicio = respuesta.find(f"date:'{fecha_temporal}', hospi_phg:")
            final = respuesta.find(";", inicio)
            valor = int(respuesta[inicio + 29:final - 3])

            datos.append([fecha_temporal, valor])
        except:
            pass

    # Generamos UN CSV con todos los datos que encontramos.
    with open("./data.csv", "w", encoding="utf-8", newline="") as archivo_csv:
        csv.writer(archivo_csv).writerows(datos)


if __name__ == "__main__":

    main()
