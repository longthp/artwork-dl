from dash import html
import dash
import dash_bootstrap_components as dbc
from .components import info_table


def create_layout(app: dash.Dash) -> dbc.Container:
    return dbc.Container(
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        children=html.H1(app.title),
                        style={
                            "text-align": "center"
                        }
                    ),
                    dbc.Col(
                        children=html.H3("by longthp")
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        children=dbc.Input(
                            type="url",
                            placeholder="Please paste the song's url..."
                        ),
                    ),
                    dbc.Col(
                        children=[
                            dbc.Button(
                                type="button",
                                children="Search",
                                id="search-button",
                            ),
                            dbc.Button(
                                type="download",
                                children="Download",
                            )
                        ]
                    ),
                    html.Br(),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        children=html.H3("artwork"),
                    ),
                    dbc.Col(
                        children=html.H3("song's information")
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardImg(
                                src="https://placehold.co/1400x1400",
                                style={
                                    "width": "100%",
                                    "height": "100%",
                                    "object-fit": "cover",
                                }
                            ),
                            outline=False
                        ),
                        width={
                            "size": 6
                        }
                    ),
                    dbc.Col(
                        info_table.render(app)
                    )
                ]
            ),
        ],
        fluid=False
    )
