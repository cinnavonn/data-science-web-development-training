import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

url = 'https://github.com/cinnavonn/training20/blob/main/gapminder_clean.csv'

df = pd.read_csv(url, sep=",", index_col=[0])
df.head()

print(df.replace(r'^\s*$', np.nan, regex=True))
df.fillna(0, inplace=True)

df1 = (df.set_index(["Year", "Country Name", "continent", "pop"])
       .stack().reset_index(name='Value').rename(columns={'level_4':'Indicator Name'}))

df1.loc[df1['Value'] == 0,'Value'] = np.nan

available_indicators = df1['Indicator Name'].unique()

app.layout = html.Div([
    html.Div([
    html.H1(
        children='Explore the gap minder!!'),

        html.Div([
        html.H3('X axis'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Agriculture, value added (% of GDP)'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '38%', 'display': 'inline-block'}),

        html.Div([
        html.H3('Y axis'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='CO2 emissions (metric tons per capita)'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '38%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df1['Year'].min(),
        max=df1['Year'].max(),
        value=df1['Year'].max(),
        marks={str(year): str(year) for year in df1['Year'].unique()},
        step=None,
    )
])


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('year--slider', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df1[df1['Year'] == year_value]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                     y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                     hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
                     color=dff[dff['Indicator Name'] == yaxis_column_name]['continent'],
                     size=dff[dff['Indicator Name'] == yaxis_column_name]['pop'],
                     log_x=True, size_max=100)

    fig.update_layout(margin={'l': 150, 'b': 40, 't': 10, 'r': 150}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    return fig

if __name__ == '__main__':
        app.run_server(debug=True)
