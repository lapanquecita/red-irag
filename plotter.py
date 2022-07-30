"""
Este programa se encarga de graficar los datos de scraper.py
"""


import pandas as pd
import plotly.graph_objects as go


def main():

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


if __name__ == "__main__":

    main()
