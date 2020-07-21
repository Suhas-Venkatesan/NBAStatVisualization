# Data
import pandas as pd
import requests
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playbyplayv2
from nba_api.stats.static import players
from matplotlib.patches import Circle, Rectangle, Arc
from nba_api.stats.endpoints import shotchartdetail

# Graphing
import plotly
import plotly.graph_objects as go

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
    'Player Visualization'
)
nba_players = players.get_players()
player_options = []

for player in nba_players:
    the_dict = {'label': player.get('full_name'), 'value': player.get('id')}
    player_options.append(the_dict)

season_options = []
for x in range(1995, 2020):
    the_dict2 = {'label': str(x) + '-' + str(x + 1)[2:4], 'value': str(x) + '-' + str(x + 1)[2:4]}
    season_options.append(the_dict2)

season_type_options = [{'label': 'Regular Season', 'value': 'Regular Season'},
                       {'label': 'Playoffs', 'value': 'Playoffs'}, {'label': 'Pre Season', 'value': 'Pre Season'},
                       {'label': 'All Star', 'value': 'All Star'}]

player_dropdown = html.Div(dcc.Dropdown(
    id='player_dropdown',
    options=player_options,
    placeholder="Select a player",
    value='201939'
))

season_dropdown = html.Div(dcc.Dropdown(
    id='season_dropdown',
    options=season_options,
    placeholder="Select a season",
    value='2019-20'
))

season_type_dropdown = html.Div(dcc.Dropdown(
    id='season_type_dropdown',
    options=season_type_options,
    placeholder="Select a season type",
    value='Regular Season'
))

output = html.Div(id='output', children=[])

player_shotchart = dcc.Graph(
    id='player_shotchart',
    config={'displayModeBar': False,
            'scrollZoom': False},
)


def PlayerVisualizer_App():
    layout = html.Div([
        nav,
        dbc.Row(header, justify='center'),
        dbc.Row(html.P()),
        dbc.Row(html.H6("Select an NBA player, a season, and a season type for a shot chart"),
                justify='center'),
        dbc.Row(html.Br()),
        dbc.Row([dbc.Col(html.H5("Player"), width=3), dbc.Col(html.H5("Season"), width=3), dbc.Col(html.H5("Season Type"), width=3),
                 ], justify='center'),
        dbc.Row([dbc.Col(player_dropdown, width=3), dbc.Col(season_dropdown, width=3), dbc.Col(season_type_dropdown, width=3)], justify='center'),
        dbc.Row(html.Br()),
        dbc.Row(player_shotchart, justify='center'),
        output
    ])
    return layout


def build_basic_shotchart(the_player, season, season_type):
    player_name = players.find_player_by_id(the_player).get('full_name')
    response = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=the_player,
        season_nullable=season,
        season_type_all_star=season_type,
        context_measure_simple='FGA')
    df = response.get_data_frames()[0]
    made_shots = df[df['SHOT_MADE_FLAG'] == 1]
    missed_shots = df[df['SHOT_MADE_FLAG'] == 0]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        # made shots
        x=made_shots['LOC_X'],
        y=made_shots['LOC_Y'],
        mode='markers',
        name='Made Shot',
        hoverinfo='skip',
        marker=dict(
            size=5,
            cmax=40,
            cmin=-40,
            color="#008000",
        ),
    ))
    fig.add_trace(go.Scatter(
        # missed shots
        x=missed_shots['LOC_X'],
        y=missed_shots['LOC_Y'],
        mode='markers',
        name='Missed Shot',
        hoverinfo='skip',
        marker=dict(
            size=5,
            cmax=40,
            cmin=-40,
            color="#FF0000",
        ),
    ))
    draw_court(fig)
    fig.update_layout(
        title={
            'text': player_name + " , " + str(season),
            'y': 1,
            'x': 0.42,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title='Basic Shot Chart',
        font=dict(
            family="Rockwell",
            size=15,
            color="#000000"
        ),
        dragmode=False
    )
    return fig


def draw_court(fig, fig_width=600, margins=10):
    import numpy as np

    # From: https://community.plot.ly/t/arc-shape-with-path/7205/5
    def ellipse_arc(x_center=0.0, y_center=0.0, a=10.5, b=10.5, start_angle=0.0, end_angle=2 * np.pi, N=200,
                    closed=False):
        t = np.linspace(start_angle, end_angle, N)
        x = x_center + a * np.cos(t)
        y = y_center + b * np.sin(t)
        path = f'M {x[0]}, {y[0]}'
        for k in range(1, len(t)):
            path += f'L{x[k]}, {y[k]}'
        if closed:
            path += ' Z'
        return path

    fig_height = fig_width * (470 + 2 * margins) / (500 + 2 * margins)
    fig.update_layout(width=fig_width, height=fig_height)

    # Set axes ranges
    fig.update_xaxes(range=[-250 - margins, 250 + margins])
    fig.update_yaxes(range=[-52.5 - margins, 417.5 + margins])

    threept_break_y = 89.47765084
    three_line_col = "#777777"
    main_line_col = "#777777"

    fig.update_layout(
        # Line Horizontal
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        shapes=[
            dict(
                type="rect", x0=-250, y0=-52.5, x1=250, y1=417.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="rect", x0=-80, y0=-52.5, x1=80, y1=137.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="rect", x0=-60, y0=-52.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="circle", x0=-60, y0=77.5, x1=60, y1=197.5, xref="x", yref="y",
                line=dict(color=main_line_col, width=1),
                # fillcolor='#dddddd',
                layer='below'
            ),
            dict(
                type="line", x0=-60, y0=137.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=1),
                layer='below'
            ),

            dict(
                type="rect", x0=-2, y0=-7.25, x1=2, y1=-12.5,
                line=dict(color="#ec7607", width=1),
                fillcolor='#ec7607',
            ),
            dict(
                type="circle", x0=-7.5, y0=-7.5, x1=7.5, y1=7.5, xref="x", yref="y",
                line=dict(color="#ec7607", width=1),
            ),
            dict(
                type="line", x0=-30, y0=-12.5, x1=30, y1=-12.5,
                line=dict(color="#ec7607", width=1),
            ),

            dict(type="path",
                 path=ellipse_arc(a=40, b=40, start_angle=0, end_angle=np.pi),
                 line=dict(color=main_line_col, width=1), layer='below'),
            dict(type="path",
                 path=ellipse_arc(a=237.5, b=237.5, start_angle=0.386283101, end_angle=np.pi - 0.386283101),
                 line=dict(color=main_line_col, width=1), layer='below'),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=220, y0=-52.5, x1=220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),

            dict(
                type="line", x0=-250, y0=227.5, x1=-220, y1=227.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=250, y0=227.5, x1=220, y1=227.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=17.5, x1=-80, y1=17.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=27.5, x1=-80, y1=27.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=57.5, x1=-80, y1=57.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=87.5, x1=-80, y1=87.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=17.5, x1=80, y1=17.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=27.5, x1=80, y1=27.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=57.5, x1=80, y1=57.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=87.5, x1=80, y1=87.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),

            dict(type="path",
                 path=ellipse_arc(y_center=417.5, a=60, b=60, start_angle=-0, end_angle=-np.pi),
                 line=dict(color=main_line_col, width=1), layer='below'),
        ]
    )
    return True
