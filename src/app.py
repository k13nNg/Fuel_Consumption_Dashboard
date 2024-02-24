# Import packages
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Incorporate data
# df = pd.read_csv('./dataset.csv')
url = 'https://raw.githubusercontent.com/k13nNg/Fuel_Consumption_Analysis/main/src/dataset.csv'
df = pd.read_csv(url, encoding='latin1')

# Initialize the app
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# shows a pie chart of different vehicle classes in the dataset, and their portion 
# with respect to the number of cars in the dataset
def graph_vehicle_classes(): 
    data_dict = {}
    for i in df['Vehicle class'].unique():
        data_dict[i] = len(df[df['Vehicle class']==i])

    fig = go.Figure(go.Pie(
        name="",
        values=list(data_dict.values()),
        labels=list(data_dict.keys()),
        hovertemplate="Class: %{label} <br>Number of models: %{value}",

    ))
    fig.update_layout(
        title_text = "Vehicle Classes in the dataset",
        title_x = 0.5,
        legend_title_text="Vehicle Classes<br>"
    )

    return fig

# shows a stacked bar charts of the number of vehicles for each vehicle class, grouped by
# manufactureres
def graph_vehicle_classes_and_manufacturers():
    vehicle_classes = df['Vehicle class'].unique()
    manufacturers = df['Make'].unique()
    data_dict = {}
    for i in manufacturers:
        temp_dict = {}
        for j in vehicle_classes:
            temp_df = df[(df['Make'] == i) & (df['Vehicle class'] == j)]
            temp_dict[j] = len(temp_df)
        
        data_dict[i] = temp_dict

    makes = []
    car_quantities = []
    for i in data_dict:
        makes.append(i)
        car_quantities.append(list(data_dict[i].values()))

    fig = go.Figure()

    for i in range (len(makes)):
        fig.add_trace(
            go.Bar(
                name=makes[i],
                x = car_quantities[i],
                y = vehicle_classes,
                orientation='h',
                hovertemplate= 
                f"Manufacturer: {makes[i]}<br>"+\
                "Number of models: %{x}"+\
                "<extra></extra>" 
            )
        )

    fig.update_layout(barmode='stack', 
                      title = "Number of Cars based on Vehicle Class and Manufacturers", 
                      legend_title_text='Manufacturers <br>',
                      title_x=0.5)
    fig.update_yaxes(title_text="Vehicle Class")
    fig.update_xaxes(title_text="Number of cars")
    return fig

# shows a scatter plot of number of car models being analyzed in the dataset divided into years
def graph_models_vs_year():
    years = df['Model year'].unique()
    models_per_year = []

    for i in years:
        models_per_year.append(len(df[df['Model year']==i]))
    
    fig= go.Figure()

    fig.add_trace(
        go.Scatter(
            x = years,
            y = models_per_year,
            hovertemplate="Year: %{x}<br>"+
                            "Number of models: %{y}"+
                            "<extra></extra>"
        )
    )

    fig.update_yaxes(title_text="Number of Models (per year)")
    fig.update_xaxes(title_text="Year")
    fig.update_layout(
        title_text="Number of car models included in the dataset based on year",
        title_x = 0.5,
    )

    return fig

# App layout
app.layout = html.Div([
    html.Br(),
    html.H1(
        children='Fuel Consumption Analysis of Plug-in Hybrid Cars from 2012 to 2024',
        style={
            'textAlign': 'center'
        }),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.Graph(id='vehicle_classes',
                  figure=graph_vehicle_classes(), 
                    hoverData={'points': [{'customdata': 'Mid-size'}]}
                )
    ], style={'width': '49%', 'display': 'inline-block', 'padding':'0 50'}),
    html.Div([
        dcc.Graph(id='manufacturer_shares'),
    ], style={'display': 'inline-block', 'width': '49%'}),
    
    html.Div([dcc.Graph(figure=graph_models_vs_year())],
              style={'width': '80%', 'padding-left':'10%', 'padding-right':'10%'}),
    html.Div([
        dcc.Graph(figure=graph_vehicle_classes_and_manufacturers())
    ], style={'width': '80%', 'padding-left':'10%', 'padding-right':'10%'}),
    html.Br(),

    html.Div([
        html.H6(children="Top 5 Car Models with Least Fuel Consumption Ratings",
                style={
                    'textAlign':'center'
                }),
        html.P(children = "Driving Condition",
               style={
                   'textAlign':'center',
                   'width': '49%', 
                   'display': 'inline-block', 
               }),
        html.P(children="Vehicle Class",
               style={'textAlign':'center', 
                      'display': 'inline-block', 
                      'width': '40%'}),
        html.Div([dcc.Dropdown(['City', 'Highway', 'Combined'], 'City', id='driving_condition')], 
                 style={
                     'width': '39%', 'display': 'inline-block', 'padding-left':'5%', 'padding-right':'5%'
                 }),
        html.Div([dcc.Dropdown(df['Vehicle class'].unique(), 'Sport utility vehicle: Small', id='vehicle_class_1')],
         style={'display': 'inline-block', 'width': '39%'}),
        dcc.Graph(id='fuel_consumption_graph'),
        html.P(children="Model Year",
               style={'textAlign':'center'}),
        html.Div([dcc.Slider(min = df['Model year'].min(), 
                             max=df['Model year'].max(), 
                             step=None, 
                             value=df['Model year'].max(),
                             marks = {str(year): str(year) for year in df['Model year'].unique()},
                             id='model_year_1')], 
                    style={'width': '80%','padding-left':'10%', 'padding-right':'10%'})
    ], style={'width':'49%', 'display': 'inline-block', 'padding':'0 50'}),

    html.Div([
        html.H6(children="Top 5 Car Models with Longest Range",
                style={
                    'textAlign':'center'
                }),
        html.P(children = "Fuel Option",
                style={
                    'textAlign':'center',
                    'width': '49%', 
                    'display': 'inline-block', 
                }),
        html.P(children="Vehicle Class",
                style={'textAlign':'center', 
                        'display': 'inline-block', 
                        'width': '40%'}),
        html.Div([dcc.Dropdown(["Battery Only", "Gasoline Only"], "Battery Only", id='fuel_type')], 
                    style={
                        'width': '39%', 'display': 'inline-block', 'padding-left':'10%', 'padding-right':'5%'
                    }),
        html.Div([dcc.Dropdown(df['Vehicle class'].unique(), 'Sport utility vehicle: Small', id='vehicle_class_2')],
            style={'display': 'inline-block', 'width': '39%'}),
        dcc.Graph(id='range_graph'),
        html.P(children="Model Year",
                style={'textAlign':'center'}),
        html.Div([dcc.Slider(min = df['Model year'].min(), 
                                max=df['Model year'].max(), 
                                step=None, 
                                value=df['Model year'].max(),
                                marks = {str(year): str(year) for year in df['Model year'].unique()},
                                id='model_year_2')], 
                    style={'width': '80%','padding-left':'10%', 'padding-right ':'10%'})
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
        html.H6(children="Average Fuel Consumption of Car Models from Different Manufacturers through Years",
                style={
                    'textAlign':'center'
                }),

        html.Div([dcc.Dropdown(df['Vehicle class'].unique(), 'Sport utility vehicle: Small', id='vehicle_class_3')],
                 style={'width':'49%', 'display': 'inline-block', 'padding': '0 20'}),
        html.Div([dcc.Dropdown(['City', 'Highway', 'Combined'], 'City', id='driving_condition_2')],
                 style={'width':'49%', 'display': 'inline-block'}),
        dcc.Graph(id='fuel_consumption_over_years')
    ], style={'width':'80%', 'padding-left':'10%', 'padding-right':'10%'}),

])

@callback(
    Output('manufacturer_shares', 'figure'),
    Input('vehicle_classes', 'hoverData')
)
# shows the bar chart displaying number of unique car models (models with the same name, but from different years are not unique),
# grouped by manufacturers and vehicle classes
def graph_shares(hoverData):

    if ('customdata' in hoverData['points'][0]):
        vehicle_class = hoverData['points'][0]['customdata']
    else:
        vehicle_class = hoverData['points'][0]['label']
    temp_df = df[df['Vehicle class']==vehicle_class]
    temp_arr=temp_df['Make'].unique()

    car_num = []

    for i in temp_arr:
        car_num.append(len(temp_df[temp_df['Make']==i]['Model'].unique()))

    fig = go.Figure(go.Bar(
        x=car_num,
        y=temp_arr,
        orientation='h',
    ))
    fig.update_layout(
        title_text = f"Unique Models from Each Manufacturer <br> <br> {vehicle_class}",
        title_x = 0.5,
    )
    fig.update_traces(
        hovertemplate="Manufacturer: %{y}<br>"+"Number of Unique Models: %{x}"+"<extra></extra>"
    )
    fig.update_xaxes(title_text="Number of Unqiue Models")
    fig.update_yaxes(title_text="Manufacturers")
    return fig

@callback(
    Output('fuel_consumption_graph', 'figure'),
    Input('driving_condition', 'value'),
    Input('model_year_1', 'value'),
    Input('vehicle_class_1', 'value')
)
# shows a bar chart of the fuel consumption ratings of the top 5 car models that has the least fuel consumption rating
# in each vehicle class and driving condition
def graph_fuel_consumption(dc, my, vc):
    dc += ' (L/100 km)'

    temp= df[(df['Vehicle class']==vc) & (df['Model year']==my)]
    temp = temp.sort_values(dc)

    d = temp.nsmallest(5, dc)
    models = d[["Make", "Model"]]
    consump = d[dc]

    fig = go.Figure()
    
    if (len(models["Model"])> 0):
        fig.add_trace(
            go.Bar(
                x=models["Model"],

                y=consump,
                customdata=models['Make'],
                hovertemplate=
                    "Model: %{x} <br>"+
                    "Manufacturer: %{customdata} <br>"+
                    "Fuel Consumption: %{y} L/100 km"+
                    "<extra></extra>"
                
            )
        )
    else:
        fig.update_layout(
            {
                "xaxis": {
            "visible": False
        },
        "yaxis": {
            "visible": False
        },
        "annotations": [
            {
                "text": "No matching data found :(",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 28
                }
            }
        ]
            }
        )

    fig.update_xaxes(title_text="Models")
    fig.update_yaxes(title_text="Fuel Consumption (L/100 km)")
    
    return fig

@callback(
    Output('range_graph', 'figure'),
    Input('fuel_type', 'value'),
    Input('model_year_2', 'value'),
    Input('vehicle_class_2', 'value')
)
# shows a bar chart of the range of the top 5 car models that has the longest range
# in each vehicle class and fuel type
def graph_range(ft, my, vc):
    rng = ""
    if (ft == "Battery Only"):
        rng = "Range 1 (km)"
    else:
        rng = "Range 2 (km)"

    temp = df[(df['Vehicle class']==vc) & (df["Model year"]==my)]


    d = temp.nlargest(5, rng)
    models = d[["Make", "Model"]]
    rngs = d[rng]

    fig = go.Figure()

    if (len(models["Model"])>0):
        fig.add_trace(
            go.Bar(
                x=models["Model"],
                y=rngs,
                marker_color='rgb(168, 221, 181)',
                customdata=models['Make'],
                hovertemplate=
                    "Model: %{x} <br>"+
                    "Manufacturer: %{customdata} <br>"+
                    "Range: %{y} km"+
                    "<extra></extra>"
                
            )
        )
    
    else:
        fig.update_layout(
            {
                "xaxis": {
            "visible": False
        },
        "yaxis": {
            "visible": False
        },
        "annotations": [
            {
                "text": "No matching data found :(",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 28
                }
            }
        ]
            }
        )
    
    fig.update_xaxes(title_text="Models")
    fig.update_yaxes(title_text="Range (km)")
    
    return fig

@callback(
    Output('fuel_consumption_over_years', 'figure'),
    Input('vehicle_class_3', 'value'),
    Input('driving_condition_2', 'value')
)
# shows a scatter plot comparing the models' average fuel consumption of different manufacturers from
# 2012 to 2024, varied by vehicle class and driving condition.
def graph_fuel_consumption_over_years(vc, dc):
    dc += ' (L/100 km)'

    models = df[df['Vehicle class'] == vc] # Select all vehicles with the vehicle class 'vc'
    manufacturers = models['Make'].unique()
    years = df['Model year'].unique()

    data_dict = {} # data_dict = {Make: {Year: Average fuel consumption}}


    avg_fuel_consmp = []

    for i in manufacturers:
        temp_dict = {}
        for j in years:
            temp_df = models[(models['Make'] == i) & (models['Model year'] == j)]
            temp_dict[j] = round(temp_df[dc].mean(), 2)
        
        data_dict[i] = temp_dict
    
    for i in data_dict:
        avg_fuel_consmp.append(list(data_dict[i].values()))
    
    fig = go.Figure()

    for i in range (len(manufacturers)):
        fig.add_trace(
            go.Scatter(
                name = manufacturers[i],
                x = years,
                y = avg_fuel_consmp[i],
                hovertemplate=f"Manufacturer {manufacturers[i]} <br>"+ 
                                "Average Fuel Consumption of Models: %{y}<br>" + 
                                "Models' Year: %{x}<br>"+
                                "<extra></extra>"
            )
        )

    fig.update_xaxes(title_text="Years")
    fig.update_yaxes(title_text="Average Fuel Consumption (L/100 km)")
    

    return fig



# Run the app
if __name__ == '__main__':
    app.run(debug=False)


