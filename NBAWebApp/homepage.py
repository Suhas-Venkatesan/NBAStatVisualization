import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from navbar import navigationbar

nav = navigationbar()

body = dbc.Container(
    [
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(
            [
                html.H1("NBA Statistics Tracker")
            ], justify="center", align="center"
        ),
        dbc.Row(html.H6("A simple way to visualize and track NBA Statistics"), justify='center'),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.H6("Player Visualization: Select any current or past NBA player along with a season"
                        "and a season type in order to see a simple shot chart with made and missed shots. Available "
                        "seasons "
                        "start from 1995. Game Visualization: Select any game from 1995 and onwards by specifying the two teams that played as well as the "'season '
                        'in order to see a play by play chart showing change in score margin during the game. '
                        ''), justify='center'),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.P("Suhas Venkatesan ©2020 using Dash and Plot.ly"), justify='center', className='footer'),

    ], style={"height": "100vh"}, fluid=True

)


def homepage():
    layout = html.Div([
        nav,
        body
    ])
    return layout
