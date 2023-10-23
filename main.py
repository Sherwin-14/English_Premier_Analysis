import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dash
import dash_table
from dash import dcc, html
from dash.dependencies import Output,Input
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc

"""
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
"""


df=pd.read_csv('Dataset/EPL_20_21.csv')

Total_Goals=df['Goals'].sum()
Total_penalty_Goals=df['Penalty_Goals'].sum()
Total_assists=df['Assists'].sum()
Total_Matches=df.shape[0]

nationality_counts = df['Nationality'].value_counts().reset_index()
nationality_counts.columns = ['Country', 'Count']
fig = px.choropleth(
    nationality_counts,
    locations='Country',
    locationmode='ISO-3',
    color='Count',
    color_continuous_scale='viridis',
    hover_name='Country',
    hover_data=['Count'],
)
fig.update_layout(
    title={
        'text': 'Distribution of Nationalities',  # Add your title
        'y':0.96,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
            size=20  # Adjust this value to change the title size
        )
    },
    width=1245,
    height=600,
    plot_bgcolor='rgba(10, 10, 40, 1)',
    paper_bgcolor='#00BFFF',
    margin=dict(l=50, r=50, b=50, t=50, pad=4)
)

squad_size=df['Club'].value_counts().nsmallest(10).plot(kind='barh',color=sns.color_palette('plasma'))

Under20=df[df['Age']<=20]
age20_25=df[(df['Age']>20) & (df['Age'])<=25]
age25_30=df[(df['Age']>25) & (df['Age'])<=30]
age30=df[df['Age']>30]

data = pd.DataFrame({'Age Group': ["Less than 20","Between 20 and 25","Between 25 and 30","Greater than 30"],
                     'Count': [Under20['Name'].count(), age20_25['Name'].count(), age25_30['Name'].count(), age30['Name'].count()]})

figure1 = px.pie(data, values='Count', names='Age Group')

# Update the layout
figure1.update_layout(


    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='#FFD700',
    width=780,
title={
        'text': "Age Distribution of Premier League Players",
        'y':0.94 ,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)






players_under_20 = df[df['Age'] < 20]


colors = ['blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue',]


trace = go.Bar(
    x=players_under_20['Club'],
    y=players_under_20['Club'].value_counts(),
    marker={'color': colors}  # Set the colors of the bars
)

data = [trace]

layout = go.Layout(
    title={
        'text': 'Total under 20 players in each club',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
            size=20  # Adjust this value to change the title size
        )
    },
    xaxis={'title': 'Clubs'},
    yaxis={'title': 'Counts'},
    plot_bgcolor='white',  # Set the plot background color to black
    paper_bgcolor='#00FFFF'  # Set the paper background color to black
)

figure2 = go.Figure(data=data, layout=layout)

top_10_goals=df[['Name','Club','Matches','Goals']].nlargest(n=10,columns='Goals')

figure3 = px.sunburst(
    top_10_goals,
    path=['Club', 'Name'],
    values='Goals',
    color='Goals',
    color_continuous_scale='Rainbow'
)

figure3.update_layout(
      title={
        'text': 'Top Scorers in Premier League',
        'y':0.96,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
            size=20  # Adjust this value to change the title size
        )
    },
    width=710,
    height=500,
    paper_bgcolor='#FFFF00'
)

top_player_assists=df[['Name','Club','Assists','Matches']].nlargest(n=10,columns='Assists')


figure4 = px.treemap(
    top_player_assists,
    path=['Club', 'Name'],
    values='Assists',
    color='Assists',
    color_continuous_scale='RdBu'
)

layout = go.Layout(
    autosize=True,
    margin=go.layout.Margin(
        l=0,  # left margin
        r=0,  # right margin
        b=0,  # bottom margin
        t=0,  # top margin
        pad=0  # padding
    )
)


figure4.update_traces(
    marker=dict(line=dict(width=0)),
    hovertemplate='<b>%{label}</b><br>Assists: %{value}<br>',
    textinfo='label+text+value',
)

figure4.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),
    treemapcolorway=['#636efa', '#EF553B', '#00cc96'],
    plot_bgcolor='white',
    paper_bgcolor='#FF4500',
    width=1750
)

figure4.update_xaxes(rangeslider_visible=False)

Assist_by_clubs=pd.DataFrame(df.groupby('Club',as_index=False)['Assists'].sum())

figure5 = px.bar(Assist_by_clubs.sort_values(by='Assists'),
             x='Assists',
             y='Club',
             orientation='h',
             labels={'Assists':'Assists', 'Club':'Club'},
             color='Assists',
             color_continuous_scale='inferno')

figure5.update_layout(
    title={
        'text': 'Plot of Clubs vs Total Assists',
        'y': 0.96,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
            size=20  # Adjust this value to change the title size
        )
    },
    autosize=True,
    paper_bgcolor='#50C878',
    width=1520
)

df_2= df[['Name','Nationality','Yellow_Cards','Red_Cards']].groupby('Nationality').agg({'Yellow_Cards':'sum','Red_Cards':'sum','Name':'count'}).sort_values(by=['Yellow_Cards','Red_Cards'],ascending=False).head(15)
df_2['Total']=df_2['Yellow_Cards']+df_2['Red_Cards']

df_2=df_2.reset_index()

Yellow=go.Bar(x=df_2['Nationality'],y=df_2['Yellow_Cards'])

Red=go.Bar(x=df_2['Nationality'],y=df_2['Red_Cards'])

data=[Yellow,Red]

layout=go.Layout(
        title={
        'text': 'Total Cards Obtained by Nationalities',  # Add your title
        'y':0.96,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
            size=20  # Adjust this value to change the title size
        )
    },
     xaxis={'title':'Nationality'},
     yaxis={'title':'Cards'},
     paper_bgcolor='#FF00FF',
     plot_bgcolor='lightgray',)

figure6=go.Figure(data=data,layout=layout)

Goals_by_clubs=pd.DataFrame(df.groupby('Club',as_index=False)['Goals'].sum())

figure7 = px.bar(Goals_by_clubs.sort_values(by='Goals'),
             x='Goals',
             y='Club',
             orientation='h',
             labels={'Goals':'Goals', 'Club':'Club'},
             color='Goals',
             color_continuous_scale='rainbow')

figure7.update_layout(
       title={
        'text': 'Plot of Clubs vs Goals',
        'y':0.96,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
            size=20  # Adjust this value to change the title size
        )
    },
    width=490,
    height=500,
    paper_bgcolor='#FF00FF'
)

figure8 = px.box(df, x="Club", y="Age")
figure8.update_layout(
    autosize=False,
    title={
        'text': 'Average Squad Age in the League',
        'y': 0.96,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
            size=20  # Adjust this value to change the title size
        )
    },
    width=1240,
    height=500,
    paper_bgcolor='#ADD8E6'

)

options=[
    {'label':'All','value':'All'},
    {'label':'Yellow Cards','value':'Yellow Cards'},
    {'label':'Red Cards','value':'Red Cards'}
]

df_distribution_of_minutes=df.groupby('Age')['Mins'].sum().reset_index()

figure10=px.scatter(df_distribution_of_minutes,x='Age',y='Mins',title='Age v/s Total Minutes Played')

figure10.update_layout(scene = dict(
                    xaxis_title='Age',
                    yaxis_title='Total Minutes Played',
                    zaxis_title='Total Minutes Played',
                    ),
                    paper_bgcolor='#FFFF00',
                    plot_bgcolor='lightgray',
                    width=1290,)


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Br(),
    html.Br(),
    html.H1('Premier League Dashboard',
                style={
                    'textAlign': 'center',
                    'color': 'Black ',
                    'fontSize':'80px'

                }),

    html.Br(),
    html.Br(),

    html.Img(src='assets/vecteezy_manchester-united-football-club-logo-symbol-white-and-black_10994339.jpg',style={'height':'180px', 'width':'18%'}),
    html.Img(src='assets/vecteezy_chelsea-club-logo-black-and-white-symbol-premier-league_26135387.jpg',style={'height':'180px', 'width':'18%'}),
    html.Img(src='assets/vecteezy_premier-league-logo-symbol-with-name-black-design-england_10994265.jpg',style={'height':'180px', 'width':'18%'}),
    html.Img(src='assets/vecteezy_manchester-city-football-club-logo-symbol-black-and-white_10994299.jpg',style={'height':'160px', 'width':'16%'}),
    html.Img(src='assets/liverpool-club-logo-black-and-white-symbol-premier-league-football-abstract-design-illustration-free-vector (1).jpg',style={'height':'180px', 'width':'18%'}),

    html.Br(),
    html.Br(),
    html.Br(),

dbc.Card(
    [
        dbc.CardBody("In the 30th year of Premier League, an exploratory data analysis was conducted on the 2021/22 season dataset..This analysis delves into the intricacies of the EPL 20/21 season, shedding light on the performance metrics of teams and players. It uncovers patterns and trends in goal scoring, assists, and defense, offering a comprehensive understanding of the strategies employed and the contributions made by different teams and players. The offensive strength and efficiency of teams are gauged through goal scoring rates, while assists serve as an indicator of teamwork and coordination on the field. Defensive statistics offer insights into a team’s ability to thwart opponents from scoring. The analysis also underscores key moments and influential players of the season, bringing to the fore decisive matches or extraordinary performances. By leveraging data from the EPL dataset, this analysis provides a data-driven perspective on the season, making it an invaluable resource for enthusiasts and researchers alike."

,
            style={
                'font-family': 'Arial',  # replace with your desired font
                'height': '200px',  # replace with your desired height
                'width': '1270px',
                'color': 'black',      # replace with your desired width
            }
        ),
    ],
    color="white",
    style={"width": "81rem"},
),

    html.Br(),
    html.Br(),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Goals",className='text-black'),
                    html.H4(Total_Goals,className='text-black')
                ],className='funkyCard card-body')
            ],className='funkyCard ')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Penalty Goals",className='text-black'),
                    html.H4(Total_penalty_Goals,className='text-black')
                ],className='funkyCard1 card-body')
            ],className='funkyCard1 ')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Assists",className='text-black'),
                    html.H4(Total_assists,className='text-black')
                ],className='funkyCard2 card-body')
            ],className='funkyCard2')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Players",className='text-black'),
                    html.H4(Total_Matches,className='text-black')
                ],className='funkyCard4 card-body')
            ],className='funkyCard4')
        ],className='col-md-3')

    ],className='row'),

    html.Br(),
    html.Br(),

dbc.Container([
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig),  # replace with your map figure
            width=12
        ),
    ])
]),
    html.Br(),
html.Div([
dbc.Row([
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(figure=figure8)
            ])
        ),width=12,
        className='col-md-12 mb-4',
        style={'width': '1500px'},
    ),
]),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(figure=figure2)
                ])
            ), className='col-md-7 mb-4'
        ),
        html.Br(),
        html.Br(),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(figure=figure1)
                ])
            ), className='col-md-5 mb-4'
        )
    ], className='row')
]),


    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(figure=figure3)
                ])
            ), className='col-md-7 mb-4'
        ),
        html.Br(),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(figure=figure7)
                ])
            ), className='col-md-5 mb-4'
        )
    ], className='row')
]),
    html.Br(),
    html.Br(),
html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=figure4)
                ])
            ])
        ], width=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=figure5)
                ])
            ])
        ], width=5)
    ], className='row mb-4')
]),
    html.Br(),
    html.Br(),
dbc.Row([
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                dcc.Dropdown(id='picker', options=options, value='All'),
                html.Br(),
                dcc.Graph(id='bar')
            ])
        ), className='col-md-12 mb-4'
    )
]),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([
        html.Div([
            dcc.Graph(figure=figure10)
        ],className='col-md-12')
    ],className='row')

],className='row')
],className='container',style={'textAlign': 'center'})

@app.callback(Output(component_id='bar',component_property='figure'),
              Input(component_id='picker',component_property='value'))
def update_graph(user_selected):

    if user_selected=='All':
        df_2 = df[['Name', 'Nationality', 'Yellow_Cards', 'Red_Cards']].groupby('Nationality').agg(
            {'Yellow_Cards': 'sum', 'Red_Cards': 'sum', 'Name': 'count'}).sort_values(by=['Yellow_Cards', 'Red_Cards'],
                                                                                      ascending=False).head(15)
        df_2['Total'] = df_2['Yellow_Cards'] + df_2['Red_Cards']

        df_2 = df_2.reset_index()

        Yellow = go.Bar(x=df_2['Nationality'], y=df_2['Yellow_Cards'])

        Red = go.Bar(x=df_2['Nationality'], y=df_2['Red_Cards'])

        data = [Yellow, Red]

        layout = go.Layout(
            title={
                'text': 'Total Cards Obtained by Nationalities',  # Add your title
                'y': 0.96,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(
                    size=20  # Adjust this value to change the title size
                )
            },
            xaxis={'title': 'Nationality'},
            yaxis={'title': 'Cards'},
            paper_bgcolor='#FF00FF')

        figure6 = go.Figure(data=data, layout=layout)

        return figure6

    elif user_selected=='Red Cards':

        top_red_cards = df[['Name', 'Red_Cards']].sort_values(by='Red_Cards', ascending=False)[:10]

        figure9 = px.bar(top_red_cards, x='Name', y='Red_Cards', title='Players with most Red cards',
                     labels={'Name': 'Name', 'Red_Cards': 'Number of Red Cards'}, color_discrete_sequence=['red'])

        return figure9

    elif user_selected=="Yellow Cards":

        top_yellow_cards = df[['Name', 'Yellow_Cards']].sort_values(by='Yellow_Cards', ascending=False)[:10]

        figure10 = px.bar(top_yellow_cards, x='Name', y='Yellow_Cards', title='Players with most Yellow cards',
                     labels={'Name': 'Name', 'Yellow_Cards': 'Number of Yellow Cards'},
                     color_discrete_sequence=['yellow'])

        return figure10


if __name__ == '__main__':
    app.run_server(debug=True)
