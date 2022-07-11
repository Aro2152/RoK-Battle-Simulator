#!/usr/bin/env python3

from asyncio import selector_events
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import json
import os


# Define options:
# Civilizations
_ = json.load(open('rss/troop_special_stats.json'))
civs = list(_.keys())

# Troop Count
min_troop_count =  0
max_troop_count = 500000

# Troop Tier
_ = json.load(open("rss/troop_tier_stats.json"))
troop_tiers = list(_.keys())

# Troop Type
troop_types = [
    "Infantry",
    "Cavalry",
    "Archer",
    "Siege"
]

# Commanders
_ = os.listdir("rss/commanders")
commanders = [c.replace("_", " ").replace(".json", "") for c in _]

# VIPs
_ = json.load(open("rss/vip_buffs.json")) 
_ = list(_.keys())
vips = [int(val) for val in _]

# Commander View
_ = json.load(open("rss/commander_view.json"))
_ = list(_.keys())
commander_view = [c.replace("_", " ").capitalize() for c in _] + ["None"]

# Commander Level
min_level = 1
max_level = 60

# Military Buildings
_ = json.load(open("rss/military_buildings.json"))
buildings = list(_.keys())
buildings_levels = {}
for bld in buildings:
    buildings_levels[f"{bld}_min"] = list(_[bld].keys())[0]
    buildings_levels[f"{bld}_max"] = list(_[bld].keys())[-1]

app = Dash(__name__,external_stylesheets=[dbc.themes.SUPERHERO])

app.layout = html.Div([

########################################################
######################## ARMY 1 ########################
########################################################
dbc.CardHeader("Rise Of Kingdoms - Battle Simulator",style={"align": "center","text-decoration": "underline"}),
    html.Div(
        children=[
        dbc.CardHeader("Army 1"),
        html.Br(),

        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Civilization"),
                dbc.CardBody(
                    [
                        dcc.Dropdown(civs, civs[0],style={"color": "black"})
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("VIP Level"),
                dbc.CardBody(
                    [
                        dcc.Slider(
                            vips[0],
                            vips[-1],
                            1,
                            value=vips[5],
                            id='vips-a1'
                        )
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Troop Type"),
                dbc.CardBody(
                    [
                        dcc.Dropdown(troop_types, troop_types[0],style={"color": "black"})
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Troop Tier"),
                dbc.CardBody(
                    [
                        dcc.Dropdown(troop_tiers, troop_tiers[-1],style={"color": "black"})
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Troop Count"),
                dbc.CardBody(
                    [
                         dcc.Input(
                            type='number',
                            value=100000,
                            min=min_troop_count,
                            max=max_troop_count,
                            step=1000
                        ),
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("War Frenzy"),
                dbc.CardBody(
                    [
                        dcc.RadioItems(['Yes', 'No'], 'No',  labelStyle={'display': 'block'}),
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Barracks Level"),
                dbc.CardBody(
                    [
                        dcc.Slider(
                            int(buildings_levels[f"{buildings[0]}_min"]),
                            int(buildings_levels[f"{buildings[0]}_max"]),
                            1,
                            value=int(buildings_levels[f"{buildings[0]}_max"]),
                        ),
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Stable Level"),
                dbc.CardBody(
                    [
                        dcc.Slider(
                            int(buildings_levels[f"{buildings[0]}_min"]),
                            int(buildings_levels[f"{buildings[0]}_max"]),
                            1,
                            value=int(buildings_levels[f"{buildings[0]}_max"]),
                        ),
                    ],
                ),
            ], 
        ),

        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Archery Range Level"),
                dbc.CardBody(
                    [
                        dcc.Slider(
                            int(buildings_levels[f"{buildings[0]}_min"]),
                            int(buildings_levels[f"{buildings[0]}_max"]),
                            1,
                            value=int(buildings_levels[f"{buildings[0]}_max"]),
                        ),
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Primary Commander"),
                dbc.CardBody(
                    [
                        dcc.Dropdown(
                            commanders,
                            commanders[0],
                            id='primary-commander-a1',
                            style={"color": "black"}
                        ),
                        html.Br(),
                        html.Label("Level "),
                        dcc.Input(
                            type='number',
                            value=60,
                            min=min_level,
                            max=max_level,
                            step=1
                        ),
                        
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Commander View"),
                dbc.CardBody(
                    [
                        dcc.RadioItems(
                            commander_view,
                            commander_view[-1],
                            id="commander-view-c1-a1",
                            labelStyle={'display': 'block'}
                        ),
                        
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Secondary Commander"),
                dbc.CardBody(
                    [
                        dcc.Dropdown(
                            commanders+['None'],
                            commanders[1],
                            id='secondary-commander-a1',
                            style={"color": "black"}
                        ),
                        html.Br(),
                        html.Label("Level ",id='level-label-c2-a1'),
                        dcc.Input(
                            type='number',
                            value=60,
                            min=min_level,
                            max=max_level,
                            step=1,
                            id='level-c2-a1'
                        ),
                        
                    ],
                ),
                dbc.CardHeader("Commander View", id='commander-view-label-c2-a1'),
                dbc.CardBody(
                    [
                        dcc.RadioItems(
                            commander_view,
                            commander_view[-1],
                            id="commander-view-c2-a1",
                            labelStyle={'display': 'block'}
                        )
                        
                    ],
                ),
            ], 
        ),
    ],
    style={'padding': 50, 'flex': 1}),
    
########################################################
######################## ARMY 2 ########################
########################################################
    html.Div(children=[
        dbc.CardHeader("Army 2"),
        html.Br(),

        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Civilization"),
                dbc.CardBody(
                    [
                        dcc.Dropdown(civs, civs[0])
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("VIP Level"),
                dbc.CardBody(
                    [
                        dcc.Slider(
                            vips[0],
                            vips[-1],
                            1,
                            value=vips[5],
                            id='vips-a2'
                        )
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Troop Type"),
                dbc.CardBody(
                    [
                        dcc.Dropdown(troop_types, troop_types[0],style={"color": "black"})
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Troop Tier"),
                dbc.CardBody(
                    [
                        dcc.Dropdown(troop_tiers, troop_tiers[-1],style={"color": "black"})
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Troop Count"),
                dbc.CardBody(
                    [
                         dcc.Input(
                            type='number',
                            value=100000,
                            min=min_troop_count,
                            max=max_troop_count,
                            step=1000
                        ),
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("War Frenzy"),
                dbc.CardBody(
                    [
                        dcc.RadioItems(['Yes', 'No'], 'No',  labelStyle={'display': 'block'}),
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Barracks Level"),
                dbc.CardBody(
                    [
                        dcc.Slider(
                            int(buildings_levels[f"{buildings[0]}_min"]),
                            int(buildings_levels[f"{buildings[0]}_max"]),
                            1,
                            value=int(buildings_levels[f"{buildings[0]}_max"]),
                        ),
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Stable Level"),
                dbc.CardBody(
                    [
                        dcc.Slider(
                            int(buildings_levels[f"{buildings[0]}_min"]),
                            int(buildings_levels[f"{buildings[0]}_max"]),
                            1,
                            value=int(buildings_levels[f"{buildings[0]}_max"]),
                        ),
                    ],
                ),
            ], 
        ),

        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Archery Range Level"),
                dbc.CardBody(
                    [
                        dcc.Slider(
                            int(buildings_levels[f"{buildings[0]}_min"]),
                            int(buildings_levels[f"{buildings[0]}_max"]),
                            1,
                            value=int(buildings_levels[f"{buildings[0]}_max"]),
                        ),
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Primary Commander"),
                dbc.CardBody(
                    [
                        dcc.Dropdown(
                            commanders,
                            commanders[0],
                            id='primary-commander-a2',
                            style={"color": "black"}
                        ),
                        html.Br(),
                        html.Label("Level "),
                        dcc.Input(
                            type='number',
                            value=60,
                            min=min_level,
                            max=max_level,
                            step=1
                        ),
                        
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Commander View"),
                dbc.CardBody(
                    [
                        dcc.RadioItems(
                            commander_view,
                            commander_view[-1],
                            id="commander-view-c1-a2",
                            labelStyle={'display': 'block'}
                        ),
                        
                    ],
                ),
            ], 
        ),
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader("Secondary Commander"),
                dbc.CardBody(
                    [
                        dcc.Dropdown(
                            commanders+['None'],
                            commanders[1],
                            id='secondary-commander-a2',
                            style={"color": "black"}
                        ),
                        html.Br(),
                        html.Label("Level ",id='level-label-c2-a2'),
                        dcc.Input(
                            type='number',
                            value=60,
                            min=min_level,
                            max=max_level,
                            step=1,
                            id='level-c2-a2'
                        ),
                        
                    ],
                ),
                dbc.CardHeader("Commander View", id='commander-view-label-c2-a2'),
                dbc.CardBody(
                    [
                        dcc.RadioItems(
                            commander_view,
                            commander_view[-1],
                            id="commander-view-c2-a2",
                            labelStyle={'display': 'block'}
                        )
                        
                    ],
                ),
            ], 
        ),

    ],
    style={'padding': 50, 'flex': 1}),

], style={
    'display': 'flex',
    'flex-direction': 'row',
    })

########################################################
################### Callbacks ARMY 1 ###################
########################################################

@app.callback(
    Output('secondary-commander-a1', 'options'),
    Output('secondary-commander-a1', 'value'),
    Input('primary-commander-a1', 'value'))
def set_secondary_commander_option(selected_primary):
    return [{'label': i, 'value': i} for i in [c for c in commanders if c != selected_primary]+['None']], 'None'


@app.callback(
    Output('commander-view-c2-a1', 'value'),
    Input('commander-view-c1-a1', 'value'),
    Input('commander-view-c2-a1', 'value'))
def set_commander_view_2_value(selected_view_1, selected_view_2):
    if (selected_view_2 != 'None') and (selected_view_1 == selected_view_2):
        return 'None'
    else:
        return selected_view_2

@app.callback(
   Output('level-label-c2-a1', 'style'),
   Output('level-c2-a1', 'style'),
   Output('commander-view-label-c2-a1', 'style'),
   Output('commander-view-c2-a1', 'style'),
   Input('secondary-commander-a1', 'value'))
def show_hide_element(selected_secondary):
    if selected_secondary == 'None':
        return [{'display': 'none'}]*4
    else:
        return [
            {'display': 'inline-block'},
            {'display': 'inline-block'},
            {'display': 'block'},
            {'display': 'block'}
        ]


########################################################
################### Callbacks ARMY 2 ###################
########################################################

@app.callback(
    Output('secondary-commander-a2', 'options'),
    Output('secondary-commander-a2', 'value'),
    Input('primary-commander-a2', 'value'))
def set_secondary_commander_option(selected_primary):
    return [{'label': i, 'value': i} for i in [c for c in commanders if c != selected_primary]+['None']], 'None'


@app.callback(
    Output('commander-view-c2-a2', 'value'),
    Input('commander-view-c1-a2', 'value'),
    Input('commander-view-c2-a2', 'value'))
def set_commander_view_2_value(selected_view_1, selected_view_2):
    if (selected_view_2 != 'None') and (selected_view_1 == selected_view_2):
        return 'None'
    else:
        return selected_view_2

@app.callback(
   Output('level-label-c2-a2', 'style'),
   Output('level-c2-a2', 'style'),
   Output('commander-view-label-c2-a2', 'style'),
   Output('commander-view-c2-a2', 'style'),
   Input('secondary-commander-a2', 'value'))
def show_hide_element(selected_secondary):
    if selected_secondary == 'None':
        return [{'display': 'none'}]*4
    else:
        return [
            {'display': 'inline-block'},
            {'display': 'inline-block'},
            {'display': 'block'},
            {'display': 'block'}
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
