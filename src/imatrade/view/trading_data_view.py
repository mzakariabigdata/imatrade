""" Contient les classes de vue pour afficher les données de trading """
import warnings
from plotly.subplots import make_subplots
import cufflinks as cf
import plotly.graph_objects as go
import pandas as pd

warnings.filterwarnings("ignore")
cf.set_config_file(offline=True)


class TradingDataView:
    """Classe de vue pour afficher les données de trading"""

    def __init__(self, dataf):
        self.dataf = dataf
        self.datetime = None
        self.fig = None

    def add_trace_mark(self, row, col, name, mark_y):
        """Ajouter une trace de marqueur"""
        self.fig.add_trace(
            go.Scatter(
                x=[self.datetime],
                y=[mark_y],
                mode="markers",
                marker={"symbol": "triangle-up", "size": 12, "color": "black"},
                name=name,
                hovertext="Entry Datetime",
            ),
            row=row,
            col=col,
            secondary_y=True,
        )

    def add_trace_volume(self):
        """Ajouter une trace de volume"""
        self.fig.add_trace(
            go.Bar(
                x=self.dataf["time"],
                y=self.dataf["volume"],
                name="volume",
                marker_color="lightsalmon",
            )
        )

    def add_trace_candlestick(self, row, col):
        """Ajouter une trace chandeliers japonais"""
        name = "candl"
        mark_y = list(self.dataf[self.dataf.time == self.datetime].close)[0]
        self.fig.add_trace(  # pylint: disable=expression-not-assigned
            go.Candlestick(
                x=self.dataf["time"],
                open=self.dataf["open"],
                high=self.dataf["high"],
                low=self.dataf["low"],
                close=self.dataf["close"],
                yaxis="y2",
                name="Candlestick",
            ),
            row=row,
            col=col,
            secondary_y=True,
        ).update_traces(yaxis="y2").data[0]
        # fig.update(go.Layout(
        # width=500,
        # height=600))
        self.add_trace_mark(row, col, name, mark_y)
        # self.add_trace_indicator()
        self.add_trace_volume()

    def add_trace_z_score_ma(self, row, col):
        """Ajouter une trace z_score_ma"""
        name = "z_score_ma"
        mark_y = list(self.dataf[self.dataf.time == self.datetime].z_score_ma)[0]

        self.fig.add_trace(
            go.Scatter(
                x=self.dataf["time"],
                y=self.dataf["z_score_ma"],
                mode="lines",
                name="z_score_ma",
                line={"color": "rgb(49,130,189)", "width": 2},
                connectgaps=True,
            ),
            row=row,
            col=col,
            secondary_y=False,
        )
        self.add_trace_mark(row, col, name, mark_y)

    def add_trace_z_score_std_dev(self, row, col):
        """Ajouter une trace z_score_std_dev"""
        name = "z_score_std_dev"
        mark_y = list(self.dataf[self.dataf.time == self.datetime].z_score_std_dev)[0]

        self.fig.add_trace(
            go.Scatter(
                x=self.dataf["time"],
                y=self.dataf["z_score_std_dev"],
                mode="lines",
                name="z_score_std_dev",
                line={"color": "rgb(49,130,189)", "width": 2},
                connectgaps=True,
            ),
            row=row,
            col=col,
            secondary_y=False,
        )
        self.add_trace_mark(row, col, name, mark_y)

    def add_trace_indicator(self):
        """Ajouter une trace indicateur"""
        labels = ["moving_avg", "std_dev"]
        colors = [
            "rgb(49,130,189)",
            "rgb(49,130,189)",
        ]
        line_size = [1.5, 1.5]

        for i, label in enumerate(labels):
            self.fig.add_trace(  # pylint: disable=expression-not-assigned
                go.Scatter(
                    x=self.dataf["time"],
                    y=self.dataf[label],
                    mode="lines",
                    name=label,
                    line={"color": colors[i], "width": line_size[i]},
                    connectgaps=True,
                )
            ).update_traces(yaxis="y2").data[0]

    def draw_chart(self, index):
        """Dessiner un graphique en chandeliers japonais"""

        # date = self.dataf.iloc[3]['time'].split(" ")[0]
        self.dataf["time"] = pd.to_datetime(self.dataf["time"])
        self.dataf.set_index("time", inplace=True)
        self.datetime = self.dataf.iloc[index].name
        date = str(self.datetime).split(" ", maxsplit=1)[0]
        # # Filtrer le DataFrame pour une date spécifique
        self.dataf = self.dataf.loc[date]

        self.dataf = self.dataf.reset_index()

        self.fig = make_subplots(
            rows=3,
            cols=1,
            row_heights=[0.5, 0.25, 0.25],
            specs=[
                [{"secondary_y": True}],
                [{"secondary_y": True}],
                [{"secondary_y": True}],
            ],
            shared_xaxes=True,
        )

        self.add_trace_candlestick(1, 1)

        self.add_trace_z_score_ma(2, 1)
        self.add_trace_z_score_std_dev(3, 1)

        # Add figure title
        # fig.update_layout(title_text="Candlestick Chart" + self.add_name_shart(datetime))
        self.fig.update_layout(
            title_text="Candlestick Chart" + ", time " + str(self.datetime)
        )
        # Set x-axis title
        # fig.update_xaxes(title_text="Time")
        self.fig.update_layout(
            xaxis_rangeslider_visible=False, autosize=False, width=1800, height=900
        )

        cf.iplot(self.fig)
