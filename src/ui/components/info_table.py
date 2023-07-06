import dash
import dash_bootstrap_components as dbc
from dash import html


def render(app: dash.Dash) -> html.Div:
    row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
    row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
    row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
    row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])
    table_body = [html.Tbody([row1, row2, row3, row4])]

    # table_body = [
    #     html.Tr(
    #         [
    #             html.Td(),
    #             html.Td(),
    #         ]
    #     )
    # ]

    return html.Div(
        dbc.Table(
            table_body,
            dark=False,
        )
    )
