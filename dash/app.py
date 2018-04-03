import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.tools as tls
import cufflinks as cf
cf.go_offline()
tls.embed('https://plot.ly/~cufflinks/8')
import json
import pandas as pd

mapbox_access_token = 'pk.eyJ1IjoiYW5uYWFzY290dCIsImEiOiJjamZjbnNxNzcxbWM2MzNvZnZkaWt2ZWp0In0.sxWd3RPIn210Wub_Jk9Pwg'#"YOUR USER TOKEN"

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly' +
    '/datasets/master/2011_february_us_airport_traffic.csv')
# import data
tempDF=pd.read_csv('../data/correctedibuttontemp2016.csv', parse_dates = [0]).set_index('Date').resample('H').first()['2016-07-01':'2016-08-31']#.first()
tempDF.columns = tempDF.columns.astype(int)
filepath = '../../cityheat/Bmore/2016/'
meta = pd.DataFrame(pd.read_csv(filepath + 'data/CleanedMeta2016.csv', sep = ','))
meta = meta.set_index('sensornumber', drop = False)
meta = meta.set_index(meta.index.astype('float64'), drop = False)

app = dash.Dash()

app.layout = html.Div([
    html.Div(
        html.Pre(id='lasso', style={'overflowY': 'scroll', 'height': '100vh'}),
        className="three columns"
    ),

    html.Div(
        className="nine columns",
        children=dcc.Graph(
            id='graph',
            figure={
                'data': [{
#                    'lat': df.lat, 'lon': df.long, 'type': 'scattermapbox'
                    'lat': meta['location:Latitude'].dropna(), 'lon': meta['location:Longitude'].dropna(), 'type': 'scattermapbox','text': meta.index,
                }],
                'layout': {
                    'mapbox': {
                        'accesstoken':mapbox_access_token, 
                        'center': dict(lat= 39.315884, lon = -76.612686),
                        'zoom': 10.5,
                    },
                    'margin': {
                        'l': 0, 'r': 0, 'b': 0, 't': 0
                    },
                }
            }
        )
    ), 
    # graph container
    html.Div([
            dcc.Graph(id='basic_graph')]),
    # compare graph container
    html.Div([
            dcc.Graph(id='basic_graph_compare')]),

], className="row")


#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})


@app.callback(
    Output('lasso', 'children'),
    [Input('graph', 'selectedData')])
def display_data(selectedData):
    return json.dumps(selectedData, indent=2)
###


@app.callback( 
        Output('basic_graph', 'figure'), 
        [Input('graph', 'clickData')]) 
def plot_basin(selection): 
    if selection is None: 
        return {} 
    else: 
        ind = selection['points'][0]['pointIndex']        
        x_data = tempDF.index##.index[0:500]# np.linspace(0,500,500) 
        y_data = tempDF.iloc[:,ind] 
        data = [go.Scatter( 
                    x=x_data, 
                    y=y_data, 
                    #line={'color':'k'},# color}, 
                    #opacity=0.8, 
                    #name="Graph" 
                )] 
        layout = go.Layout( 
                    yaxis={'type': 'linear', 'title': "Value"}, 
                    #margin={'l': 60, 'b': 40, 'r': 10, 't': 10}, 
                    hovermode="False" 
                    ) 
         
        return {'data': data, 'layout': layout} 

@app.callback( 
        Output('basic_graph_compare', 'figure'), 
        [Input('graph', 'selectedData')]) 
def plot_multiple(selection): 
    if selection is None: 
        return {} 
    else: 
        ind = [x['text'] for x in selection['points']]
        print(ind)#ind = selection['points'][0]['pointIndex']        
        x_data = tempDF.index##.index[0:500]# np.linspace(0,500,500) 
        y_data = tempDF.loc[:,ind] 
        data = [go.Scatter( 
                    x=x_data, 
                    y=y_data, 
                    #line={'color':'k'},# color}, 
                    #opacity=0.8, 
                    #name="Graph" 
                )] 
        layout = go.Layout( 
                    yaxis={'type': 'linear', 'title': "Value"}, 
                    #margin={'l': 60, 'b': 40, 'r': 10, 't': 10}, 
                    hovermode="False" 
                    ) 
        return tempDF[ind].iplot(asFigure=True)  
       # return {'data': data, 'layout': layout} 
if __name__ == '__main__':
    app.run_server(debug=True)
