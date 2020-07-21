# Data
import pandas as pd
import requests
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playbyplayv2

# Graphing
import plotly
import plotly.graph_objects as go
import datetime

# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

# Navbar
import navbar

nav = navbar.navigationbar()

header = html.H2(
    'Game Visualization'
)
nba_teams = teams.get_teams()
team_options = []
for x in range(0, 30):
    the_dict = {'label': nba_teams[x].get('full_name'), 'value': nba_teams[x].get('id')}
    team_options.append(the_dict)

season_options = []
for x in range(1995, 2020):
    the_dict2 = {'label': str(x) + '-' + str(x + 1)[2:4], 'value': str(x) + '-' + str(x + 1)[2:4]}
    season_options.append(the_dict2)

team1_dropdown = html.Div(dcc.Dropdown(
    id='team1_dropdown',
    options=team_options,
    placeholder="Select a team",
    value="1610612764"
))

team2_dropdown = html.Div(dcc.Dropdown(
    id='team2_dropdown',
    options=team_options,
    placeholder="Select a team",
    value="1610612738"
))
# may have to change to dropdown
season_select = html.Div(dcc.Dropdown(
    id="season_select",
    options=season_options,
    placeholder="Select a season",
    value="2019-20"
))

game_selector_dropdown = html.Div(dcc.Dropdown(
    id='game_selector_dropdown',
    # callback which queries games based on team1, team2, and season,
    placeholder="Select a game",
    value='0021900542'
))

# necessary?
output = html.Div(id='output', children=[])

game_graph = dcc.Graph(
    id='game_graph',
    config={'displayModeBar': False,
            'scrollZoom': False},
)




def GameVisualizer_App():
    layout = html.Div([
        nav,
        dbc.Row(header, justify='center'),
        dbc.Row(html.P()),
        dbc.Row(html.H6("Select any NBA game by specifying the two teams that played and the season that "
                        "the game was played in. A play-by-play line graph will be shown."), justify='center'),
        dbc.Row(html.H6("The upper half represents the home team while the lower half represents the away team."),
                justify='center'),
        dbc.Row(html.P()),
        dbc.Row([dbc.Col(html.H5("Team 1")), dbc.Col(html.H5("Team 2")), dbc.Col(html.H5("Season")),
                 dbc.Col(html.H5("Game"))], justify='center'),
        dbc.Row([dbc.Col(team1_dropdown), dbc.Col(team2_dropdown), dbc.Col(season_select),
                 dbc.Col(game_selector_dropdown)]),
        game_graph,
        output
    ])
    return layout


def build_graph(game_id):
    pbp = playbyplayv2.PlayByPlayV2(game_id=game_id)
    pbp = pbp.get_data_frames()[0]
    pbp = pbp.loc[(pbp['EVENTMSGTYPE'] == 1) | (pbp['EVENTMSGTYPE'] == 3)]

    ##

    pbp['secs'] = pbp['PCTIMESTRING'].str.split(":").str[0].astype(int).rsub(12).mul(60).sub(pbp['PCTIMESTRING'].str.split(":").str[1].astype(int)).add(pbp['PERIOD'].sub(1).mul(720))

    ##
    pbp.loc[(pbp['PERIOD'] > 4), 'secs'] = pbp['PCTIMESTRING'].str.split(":").str[0].astype(int).rsub(5).mul(60).sub(
        pbp['PCTIMESTRING'].str.split(":").str[1].astype(int)).add(2880).add(pbp['PERIOD'].sub(5).mul(300))

    XAXIS = pbp['secs'].floordiv(60).astype(str)
    XAXIS = XAXIS.add(":")
    XAXIS = XAXIS.add(pbp['secs'].mod(60).astype(str))

    ##

    XAXIS = pd.to_datetime(XAXIS, format="%M:%S")
    pbp['XAXIS'] = XAXIS
    pbp['SCOREMARGIN'].replace({"TIE": "0"}, inplace=True)
    pbp['SCOREMARGIN'] = pd.to_numeric(pbp['SCOREMARGIN'])
    fig = go.Figure()
    values = list(range(-40, 45))  # change
    fig.add_trace(go.Scatter(
        x=pbp['XAXIS'],
        y=pbp['SCOREMARGIN'],
        hovertemplate=
        'Time: %{x}<extra></extra><br>' +
        'Score: %{text}<br>' +
        'Score Margin: %{y}',
        text=pbp['SCORE'],
        connectgaps=True,
        mode='lines+markers',
        marker=dict(
            size=10,
            cmax=40,
            cmin=-40,
            color="#000000",
        ),
        line=dict(color='#000000', width=5)
    ))

    fig.update_layout(
        {
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })

    fig.update_layout(

        xaxis_title="First Quarter                                       Second Quarter                               "
                    "Third Quarter                                   Fourth Quarter",
        yaxis_title="Score Margin (Home-Away)",
        font=dict(
            family="Rockwell",
            size=15,
            color="#000000"
        ),
        height=750,
        dragmode=False,
        annotations=[
            dict(
                x=1.03,
                y=.9,
                xref='paper',
                yref='paper',
                text="Home",
                bordercolor='#000000',
                showarrow=False,
                font=dict(
                    family="Rockwell",
                    size=15,
                    color="#000000"
                ),
                borderwidth=5,
            ),
            dict(
                x=1.03,
                y=.1,
                xref='paper',
                yref='paper',
                text="Away",
                bordercolor='#000000',
                showarrow=False,
                font=dict(
                    family="Rockwell",
                    size=15,
                    color="#000000"
                ),
                borderwidth=5,
            )
        ]
    )

    fig.add_shape(
        # Line Horizontal
        type="line",
        x0=datetime.datetime(year=1900, month=1, day=1, minute=0, second=0),
        y0=0,
        x1=pbp['XAXIS'].iloc[-1],
        y1=0,
        line=dict(
            color="#000000",
            width=1,
        ),
    )

    fig.add_layout_image(
        dict(
            source="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcS4pDttG-zFcSxwSmFfmiKCOEzXF7y7zSfYRw&usqp=CAU",
            xref="paper", yref="paper",
            x=.05, y=.9,
            sizex=.26, sizey=.26,
            xanchor="right", yanchor="bottom"
        )
    )

    fig.update_layout(xaxis_range=[datetime.datetime(year=1900, month=1, day=1, minute=0, second=0),
                                   pbp['XAXIS'].iloc[-1] + datetime.timedelta(minutes=2, seconds=0)])

    fig.update_xaxes(ticks="inside")

    fig.update_layout(xaxis=dict(tickformat='%M:%S'))

    fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=datetime.datetime(year=1900, month=1, day=1, minute=12, second=0),
            y0=pbp['SCOREMARGIN'].min() - 5,
            x1=datetime.datetime(year=1900, month=1, day=1, minute=12, second=0),
            y1=pbp['SCOREMARGIN'].max() + 5,
            line=dict(
                color="#000000",
                width=2,
                dash='dot'
            )
        )
    )

    fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=datetime.datetime(year=1900, month=1, day=1, minute=24, second=0),
            y0=pbp['SCOREMARGIN'].min() - 5,
            x1=datetime.datetime(year=1900, month=1, day=1, minute=24, second=0),
            y1=pbp['SCOREMARGIN'].max() + 5,
            line=dict(
                color="#000000",
                width=2,
                dash='dot'
            )
        )
    )

    fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=datetime.datetime(year=1900, month=1, day=1, minute=36, second=0),
            y0=pbp['SCOREMARGIN'].min() - 5,
            x1=datetime.datetime(year=1900, month=1, day=1, minute=36, second=0),
            y1=pbp['SCOREMARGIN'].max() + 5,
            line=dict(
                color="#000000",
                width=2,
                dash='dot'
            )
        )
    )

    fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=datetime.datetime(year=1900, month=1, day=1, minute=48, second=0),
            y0=pbp['SCOREMARGIN'].min() - 5,
            x1=datetime.datetime(year=1900, month=1, day=1, minute=48, second=0),
            y1=pbp['SCOREMARGIN'].max() + 5,
            line=dict(
                color="#000000",
                width=2,
                dash='dot'
            )
        )
    )

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
    )
    return fig
