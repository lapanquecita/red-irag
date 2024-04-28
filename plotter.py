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

    df = pd.read_csv("./data.csv", parse_dates=["isodate"], index_col="isodate")

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
            line_shape="spline",
            fill="tozeroy",
        )
    )

    fig.update_xaxes(
        tickformat="%b<br>%Y",
        ticks="outside",
        ticklen=10,
        zeroline=False,
        tickcolor="#FFFFFF",
        linewidth=2,
        gridwidth=0.5,
        showline=True,
        mirror=True,
        nticks=20,
    )

    fig.update_yaxes(
        title="Promedio semanal de camas ocupadas",
        ticks="outside",
        ticklen=10,
        title_standoff=10,
        zeroline=False,
        tickcolor="#FFFFFF",
        linewidth=2,
        gridwidth=0.5,
        showline=True,
        mirror=True,
        nticks=17,
    )

    fig.update_layout(
        showlegend=False,
        width=1280,
        height=720,
        # font_family="Quicksand",
        font_color="#FFFFFF",
        font_size=16,
        title_text="Número de camas generales ocupadas para COVID-19 en México",
        title_x=0.5,
        title_y=0.97,
        margin_t=55,
        margin_r=40,
        margin_b=105,
        margin_l=100,
        title_font_size=26,
        plot_bgcolor="#2A0944",
        paper_bgcolor="#3B185F",
        annotations=[
            dict(
                x=0.01,
                y=-0.18,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: Red IRAG (2024)",
            ),
            dict(
                x=0.5,
                y=-0.18,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="Mes y año de registro",
            ),
            dict(
                x=1.01,
                y=-0.18,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image("./imgs/1.png")


def crear_calendarios():
    """
    Esta función creará un calendario para cada año.
    """

    for año in [2020, 2021, 2022, 2023, 2024]:
        crear_calendario(año)


def crear_calendario(year):
    """
    Esta función crea un calendario, el cual es en relidad
    un mapa de calor pero disfrazado.
    """

    # Cargamos el dataset y especificamos el campo 'isodate' como nuestro índice.
    df = pd.read_csv("./data.csv", parse_dates=["isodate"], index_col="isodate")

    # Solo seleccionamos los valores del año específicado.
    df = df[df.index.year == year]

    # Creamos un esqueleto con todos los días del año especificado.
    # Después agregamos la columna de hospitalizados de nuestro DataFrame anterior.
    # Para los días sin datos esto nos dará valores NaN.
    final = pd.DataFrame(
        index=pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="d"),
        data={"hospitalizados": df["hospitalizados"]},
    )

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

    final["semana"] = numeros_de_esmanas[pad : len(final) + pad]

    final["diadelasemana"] = final.index.dayofweek

    # Creamos una columna donde solo el primer día de cada mes tendrá un borde.
    final["borde"] = final.index.map(lambda x: 1 if x.day == 1 else 0)

    # Utilizado para nuestro eje horizontal.
    meses_etiquetas = [
        "Ene.",
        "Feb.",
        "Mar.",
        "Abr.",
        "May.",
        "Jun.",
        "Jul.",
        "Ago.",
        "Sep.",
        "Oct.",
        "Nov.",
        "Dic.",
    ]
    meses_marcas = np.linspace(1.5, 49.5, 12)

    # Utilizado para nuestro eje vertical.
    days_ticks = {
        0: "Lun.",
        1: "Mar.",
        2: "Mié.",
        3: "Jue.",
        4: "Vie.",
        5: "Sáb.",
        6: "Dom.",
    }

    # Creamos las marcas para nuestra escala lateral.
    valor_min = final["hospitalizados"].min()
    valor_max = final["hospitalizados"].quantile(0.95)

    marcas_valores = np.linspace(valor_min, valor_max, 7)
    marcas_textos = list()

    for marca in marcas_valores:
        if marca >= 1000:
            marcas_textos.append(f"{marca / 1000:,.1f}k")
        else:
            marcas_textos.append(f"{marca:,.0f}")

    marcas_textos[-1] = f"≥{marcas_textos[-1]}"

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
            colorscale=["hsla(0, 100%, 100%, 0.0)", "hsla(0, 100%, 100%, 1.0)"],
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
            colorscale="portland",
            zmin=valor_min,
            zmax=valor_max,
            colorbar=dict(
                tickvals=marcas_valores,
                ticktext=marcas_textos,
                ticks="outside",
                outlinewidth=1.5,
                thickness=20,
                outlinecolor="#FFFFFF",
                tickwidth=2,
                tickcolor="#FFFFFF",
                ticklen=10,
                tickfont_size=16,
            ),
        )
    )

    fig.update_xaxes(
        side="top",
        tickfont_size=20,
        range=[-1, final["semana"].max() + 1],
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
        height=400,
        # font_family="Quicksand",
        font_color="#FFFFFF",
        font_size=20,
        title_text=f"Número de camas generales ocupadas para COVID-19 en México durante el {year}",
        title_x=0.5,
        title_y=0.93,
        margin_t=100,
        margin_l=90,
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
                text="Fuente: Red IRAG (2024)",
            ),
            dict(
                x=0.5,
                y=-0.19,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="El □ indica el Inicio de cada mes",
            ),
            dict(
                x=1.01,
                y=-0.19,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image(f"./imgs/{year}.png")


if __name__ == "__main__":
    area_chart()
    crear_calendarios()
