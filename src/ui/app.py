import dash
import dash_bootstrap_components as dbc
from . import layout


def main() -> None:
    app = dash.Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "./assets/styles.css",
        ],
        external_scripts=[

        ]
    )
    app.index_string = """
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%css%}
            <link rel='icon' type='image/x-icon' href='https://img.icons8.com/fluency/48/mona-lisa.png'>
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    """
    app.title = "artwork-dl"
    app.layout = layout.create_layout(app)

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
