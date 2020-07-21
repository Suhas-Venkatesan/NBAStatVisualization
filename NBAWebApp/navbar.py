import dash_bootstrap_components as dbc


def navigationbar():
    nav = dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("About", href="/about")),
            dbc.NavItem(dbc.NavLink("Players", href="/players")),
            dbc.NavItem(dbc.NavLink("Games",  href="/games")),
        ],
        fill=True,
        pills=True

    )
    return nav


