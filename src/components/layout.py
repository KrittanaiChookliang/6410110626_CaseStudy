from dash import Dash, html

def create_layout(app: Dash) -> html.Div:
    return html.Div(className="app-div", chldren=[html.H1(app.title), html.Hr()])