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
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(html.P("Suhas Venkatesan ©2020 using Dash and Plot.ly, data from stats.nba.com"), justify='center', className='footer'),

    ], style={"height": "100vh"}, fluid=True

)


def homepage():
    layout = html.Div([
        nav,
        body
    ])
    return layout
