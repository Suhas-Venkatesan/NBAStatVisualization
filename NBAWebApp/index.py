import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from nba_api.stats.endpoints import leaguegamefinder

from GameVisualizer import GameVisualizer_App, build_graph
from players import PlayerVisualizer_App, build_basic_shotchart
from homepage import homepage

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/games':
        return GameVisualizer_App()
    elif pathname == '/about':
        return homepage()
    # change later after players page is done
    elif pathname == '/players':
        return PlayerVisualizer_App()
    else:
        return homepage()


@app.callback(
    Output('game_selector_dropdown', 'options'),
    [Input('team1_dropdown', 'value'),
     Input('team2_dropdown', 'value'),
     Input('season_select', 'value'),
     ])
def query_available_games(team1, team2, season):
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team1, vs_team_id_nullable=team2,
                                                   season_nullable=season)
    games = gamefinder.get_data_frames()[0]
    game_options = []
    for game in games.index:
        thedict = {'label': games['MATCHUP'][game] + " , " + str(games['GAME_DATE'][game]),
                   'value': games['GAME_ID'][game]}
        game_options.append(thedict)
    return game_options


@app.callback(
    Output('game_graph', 'figure'),
    [Input('game_selector_dropdown', 'value')]
)
def update_graph(game_id):
    graph_figure = build_graph(game_id)
    return graph_figure


@app.callback(
    Output('player_shotchart', 'figure'),
    [Input('player_dropdown', 'value'),
     Input('season_dropdown', 'value'),
     Input('season_type_dropdown', 'value')
    ]
)
def update_shotchart(player, season, season_type):
    shotchart_figure = build_basic_shotchart(player, season, season_type)
    return shotchart_figure


if __name__ == '__main__':
    app.run_server(debug=False,port=3000)
