import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///people.db')

df = pd.read_sql('SELECT * FROM inmates', engine)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Database Dashboard"),
    dcc.Dropdown(
        id='feature-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value=df.columns[0]
    ),
    dcc.Graph(id='feature-graph')
])

@app.callback(
    Output('feature-graph', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_graph(selected_feature):
    fig = px.histogram(df, x=selected_feature)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)