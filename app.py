import dash
import dash_core_components as dcc 
import dash_html_components as html 
import pandas as pd
import plotly.graph_objects as go
from bs4 import BeautifulSoup as soup
import urllib
import pandas as pd
from urllib.request import urlopen
import os, ssl

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
style1= {'backgroundColor':'purple','textAlign': 'center','color':'white'}

### begining of web scraping fo the data
def scrape():
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context
    my_urls = {'ug':'https://www.use.or.ug/content/market-snapshot','ke':'https://www.nse.co.ke/market-statistics/equity-statistics.html?view=statistics',
            'tz':"https://www.dse.co.tz/dse/market-report"}
    data = []
    for my_url in my_urls:
        uClient = urlopen(my_urls[my_url])
        html_page = uClient.read()
        uClient.close()
        soup_page = soup(html_page,"html.parser")
        containers = soup_page.findAll("tbody")
        if my_url=='ug':
            containers = containers[0].findAll("tr")
            for container in containers:
                content = container.findAll('td')
                data.append([content[0].a.text,content[1].text,content[2].text,'Uganda',3700.56])
        elif my_url=='ke':
            for container in containers[0].findAll("tr",["row1","row0"]):
                data.append([container.findAll("td")[0].text,container.findAll("td")[1].text,container.findAll("td")[2].text,'Kenya',108.54])
        else:
            for container in containers[0].findAll('tr'):
                container=container.findAll('td')
                data.append([container[0].a.text,container[1].text,container[2].text,'Tanzania',2319.70])
    return pd.DataFrame(data)

df=scrape()
# cleaning
df.columns = ['name','prev','last','country','eqv_to_usd']
df['prev']=df['prev'].apply(lambda x:x.replace(',', ''))
df['last']=df['last'].apply(lambda x:x.replace(',', ''))
df['prev']=df['prev'].astype(float)
df['last']=df['last'].astype(float)
# coverting the currencies to usd
df['prev_usd']=df['prev']/df['eqv_to_usd']
df['last_usd']=df['last']/df['eqv_to_usd']
df = df.drop(['prev','last'],axis=1)

#sorting
df=df.sort_values(by=['country', 'last_usd'])
#ploting number of listed companies in a country donut chart
n_comp = df[['name','country']].groupby(['country']).count().reset_index()
labels = list(n_comp['country'].values)
values = list(n_comp['name'].values)
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig.update_layout(title="number of listed companies by country")

#ploting avarage of listed companies in a country donut chart
av_comp = df[['last_usd','country']].groupby(['country']).mean().reset_index()
labels = list(av_comp['country'].values)
values = list(av_comp['last_usd'].values)
fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig1.update_layout(title="avarage of last value listed companies by country")

#ploting avarage of listed companies in a country donut chart
av_comp = df[['last_usd','country']].groupby(['country']).max().reset_index()
labels = list(av_comp['country'].values)
values = list(av_comp['last_usd'].values) 
animals=['giraffes', 'orangutans', 'monkeys']
fig2 = go.Figure([go.Bar(x=labels, y=values)])
fig2.update_layout(title="max of last value listed companies by country")

#### plots for companies in each country.

#kenya
kenyan_companies = list(df[df['country']=='Kenya']['name'].values)

figk = go.Figure()
figk.add_trace(go.Bar(x=kenyan_companies,
                y=list(df[df['country']=='Kenya']['prev_usd'].values),
                name='Previous',
                marker_color='rgb(55, 83, 109)'
                ))
figk.add_trace(go.Bar(x=kenyan_companies,
                y=list(df[df['country']=='Kenya']['last_usd'].values),
                name='Last',
                marker_color='rgb(26, 118, 255)'
                ))

figk.update_layout(
    title='Nairobi Security Exchange',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='USD',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
#uganda
Ugandan_companies = list(df[df['country']=='Uganda']['name'].values)

figu = go.Figure()
figu.add_trace(go.Bar(x=Ugandan_companies,
                y=list(df[df['country']=='Uganda']['prev_usd'].values),
                name='Previous',
                marker_color='rgb(55, 83, 109)'
                ))
figu.add_trace(go.Bar(x=Ugandan_companies,
                y=list(df[df['country']=='Uganda']['last_usd'].values),
                name='Last',
                marker_color='rgb(26, 118, 255)'
                ))

figu.update_layout(
    title='Uganda Security Exchange',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='USD',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

#tanzania
Tanzanian_companies = list(df[df['country']=='Tanzania']['name'].values)

figt = go.Figure()
figt.add_trace(go.Bar(x=Tanzanian_companies,
                y=list(df[df['country']=='Tanzania']['prev_usd'].values),
                name='Previous',
                marker_color='rgb(55, 83, 109)'
                ))
figt.add_trace(go.Bar(x=Tanzanian_companies,
                y=list(df[df['country']=='Tanzania']['last_usd'].values),
                name='Last',
                marker_color='rgb(26, 118, 255)'
                ))

figt.update_layout(
    title='Dar Es Salaam Security exchange',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='USD',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

app.layout = html.Div(
    children=[
        html.H1(children='East Africa Security Exchange'),
        html.Div(children='''
        Dali Codes: A web scraping application from NSE, DSE and USE.
        '''),
        html.Div(
            children=[
                html.Div(style=style1,children=[html.H1('108.54'),html.P('KSH = 1 USD')],className="four columns"),
                html.Div(style=style1,children=[html.H1('2319.70'),html.P('TSH = 1 USD')],className="four columns"),
                html.Div(style=style1,children=[html.H1('3700.56'),html.P('UGX = 1 USD')],className="four columns")
            ]
            ,className="row"),
        html.Div(
            children=[
                html.Div(dcc.Graph(figure=fig),className="four columns"),
                html.Div(dcc.Graph(figure=fig2),className="four columns"),
                html.Div(dcc.Graph(figure=fig1),className="four columns")
            ]
            ,className="row"),


        html.Div(
            children=[
                html.Div(dcc.Graph(figure=figt),className="seven columns"),
                html.Div(dcc.Graph(figure=figu),className="five columns")
            ]
            ,className="row"),
        html.Div(dcc.Graph(figure=figk),className="row"),
        ]
    )

if __name__=='__main__':
    app.run_server(debug=True) 