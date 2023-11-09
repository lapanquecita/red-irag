"""
Este programa se encarga de graficar los datos de scraper.py
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def area_chart():
    """
    Esta función grafica una simple gráfica de área.
    """

    df = pd.read_csv(
        "./data.csv", parse_dates=["isodate"], index_col="isodate")

    # Remuestreado con la media semanal.
    # Se libre de filtrar por fecha o cambiar el periodo.
    df = df.resample("W").mean()

    fig = go.Figure()

    fig.add_traces(
        go.Scatter(
            x=df.index,
            y=df["hospitalizados"],
            mode="lines",
            line_color="#FEC260",
            line_width=5,
            fill="tozeroy")
    )

    fig.update_xaxes(
        title="",
        tickformat="%b<br>%Y",
        ticks="outside",
        ticklen=10,
        zeroline=False,
        title_standoff=0,
        tickcolor="#FFFFFF",
        linewidth=2,
        gridwidth=0.5,
        showline=True,
        mirror=True,
        nticks=20
    )

    fig.update_yaxes(
        title="Prom. hospitalizados semanales",
        ticks="outside",
        ticklen=10,
        title_standoff=10,
        zeroline=False,
        tickcolor="#FFFFFF",
        linewidth=2,
        gridwidth=0.5,
        showline=True,
        mirror=True,
        nticks=17
    )

    fig.update_layout(
        showlegend=False,
        legend_borderwidth=1.5,
        xaxis_rangeslider_visible=False,
        width=1280,
        height=720,
        font_family="Quicksand",
        font_color="white",
        font_size=18,
        title_text="Hospitalizados (no  UCI) semanales en México por COVID-19",
        title_x=0.5,
        title_y=0.95,
        margin_t=90,
        margin_l=120,
        margin_r=40,
        margin_b=0,
        title_font_size=36,
        plot_bgcolor="#2A0944",
        paper_bgcolor="#3B185F"
    )

    fig.write_image("./1.png")


def crear_calendarios():
    """
    Esta función creará un calendario para cada año.
    """

    for año in [2020, 2021, 2022]:
        crear_calendario(año)


def crear_calendario(year):
    """
    Esta función crea un calendario, el cual es en relidad
    un mapa de calor pero disfrazado.
    """

    # Cargamos el dataset y especificamos el campo 'isodate' como nuestro índice.
    df = pd.read_csv(
        "./data.csv",
        parse_dates=["isodate"],
        index_col="isodate"
    )

    # Solo seleccionamos los valores del año específicado.
    df = df[df.index.year == year]

    # Creamos un esqueleto con todos los días del año especificado.
    # Después agregamos la columna de hospitalizados de nuestro DataFrame anterior.
    # Para los días sin datos esto nos dará valores NaN.
    final = pd.DataFrame(index=pd.date_range(
        f"{year}-01-01", f"{year}-12-31", freq="d"), data={"hospitalizados": df["hospitalizados"]})

    # Opcional: rellenar valores NaN con 0.
    final.fillna(0, inplace=True)

    # Vamos a crear una lista para calcular todas lase semanas del año
    # esto es para poder acomodarlas de 0 a 52.
    numeros_de_esmanas = list()

    for semana in range(54):
        numeros_de_esmanas.extend([semana for _ in range(7)])

    # Necesitamos saber en que día de la semana fue el primer dái del año
    # esto con el propósito de poder cortar la lista anterior.
    pad = final.index[0].dayofweek

    final["semana"] = numeros_de_esmanas[pad:len(final) + pad]

    final["diadelasemana"] = final.index.dayofweek

    # Creamos una columna donde solo el primer día de cada mes tendrá un borde.
    final["borde"] = final.index.map(lambda x: 1 if x.day == 1 else 0)

    # Utilizado para nuestro eje horizontal.
    meses_etiquetas = [
        "Ene.", "Feb.", "Mar.", "Abr.",
        "May.", "Jun.", "Jul.", "Ago.",
        "Sep.", "Oct.", "Nov.", "Dic."
    ]
    meses_marcas = np.linspace(1.5, 49.5, 12)

    # Utilizado para nuestro eje vertical.
    days_ticks = {0: "Lun.", 1: "Mar.", 2: "Mié.",
                  3: "Jue.", 4: "Vie.", 5: "Sáb.", 6: "Dom."}

    # Creamos las marcas para nuestra escala lateral.
    marcas_valores = np.arange(0, 28000, 4000)
    marcas_textos = [f"{valor / 1000:,.0f}k" for valor in marcas_valores]
    marcas_textos[0] = "0"

    # Esta escala de colores está diseñada para acentuar los
    # valores máximos y ocultar los mínimos (0).`
    escala_de_colores = [
        [0, "#041C32"],
        [0.0005, "#0d47a1"],
        [0.25, "#689f38"],
        [0.5, "#ffd600"],
        [0.75, "#ff6f00"],
        [0.95, "#c62828"],
        [1.0, "#8B0000"],
    ]

    # Vamos a crear dos mapas de calor, uno será usado para lor bordes
    # decada mes y el otro para poner los datos de hospitalizaciones.
    fig = go.Figure()


    # El mapa de calor de bordes es muy sencillo, pero es importante notar
    # los parámetros xgap y ygap.
    fig.add_trace(
        go.Heatmap(
            x=final["semana"],
            y=final["diadelasemana"],
            z=final["borde"],
            xgap=1,
            ygap=12,
            colorscale=["hsla(0, 100%, 100%, 0.0)",
                        "hsla(0, 100%, 100%, 1.0)"],
            showscale=False,
        )
    )

    # El segundo mapa de calor estará sobre el primero
    # y mostrará los valores de cada día. Aquí los parámetros
    # xgapy y ygap son distintos para permitir ver los bordes.
    fig.add_trace(
        go.Heatmap(
            x=final["semana"],
            y=final["diadelasemana"],
            z=final["hospitalizados"],
            xgap=5,
            ygap=16,
            colorscale=escala_de_colores,
            zmin=0,
            zmax=24000,
            colorbar={
                "tickvals": marcas_valores,
                "ticktext": marcas_textos,
                "ticks": "outside",
                "outlinewidth": 1.5,
                "thickness": 20,
                "outlinecolor": "#FFFFFF",
                "tickwidth": 2,
                "tickcolor": "#FFFFFF",
                "ticklen": 10,
                "tickfont_size": 16,
            }
        )
    )

    fig.update_xaxes(
        side="top",
        tickfont_size=20,
        range=[-1, 53 if len(final) == 365 else 54],
        ticktext=meses_etiquetas,
        tickvals=meses_marcas,
        ticks="outside",
        ticklen=5,
        tickwidth=0,
        linecolor="#FFFFFF",
        tickcolor="#1E1E1E",
        showline=True,
        zeroline=False,
        showgrid=False,
        mirror=True,
    )

    fig.update_yaxes(
        range=[6.75, -0.75],
        ticktext=list(days_ticks.values()),
        tickvals=list(days_ticks.keys()),
        ticks="outside",
        tickfont_size=16,
        ticklen=10,
        title_standoff=0,
        tickcolor="#FFFFFF",
        linewidth=1.5,
        showline=True,
        zeroline=False,
        showgrid=False,
        mirror=True,
    )

    fig.update_layout(
        showlegend=False,
        width=1280,
        height=380,
        font_family="Quicksand",
        font_color="#FFFFFF",
        font_size=20,
        title_text=f"Número de camas generales ocupadas por COVID-19 en México durante el {year} por día",
        title_x=0.5,
        title_y=0.93,
        margin_t=100,
        margin_l=100,
        margin_r=125,
        margin_b=55,
        title_font_size=26,
        plot_bgcolor="#041C32",
        paper_bgcolor="#04293A",
        annotations=[
            dict(
                x=0.01,
                y=-0.19,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: Red IRAG"
            ),
            dict(
                x=0.5,
                y=-0.19,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="□: Inicio del mes"
            ),
            dict(
                x=1.01,
                y=-0.19,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita"
            )
        ]
    )

    fig.write_image(f"./{year}.png")


if __name__ == "__main__":

    area_chart()
    crear_calendarios()
