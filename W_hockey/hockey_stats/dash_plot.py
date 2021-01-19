import pandas as pd
import os
import chart_studio.plotly as py
import chart_studio.tools
import data_display as dd
import plotly.express as px

py_user = os.getenv('pyuser')
py_pw = os.getenv('pypw')
key = os.getenv('studiokey')

def map():
    con = dd.connect_sql()
    chart_studio.tools.set_credentials_file(username=py_user, api_key=key)
    chart_studio.tools.set_config_file(world_readable=True,
                                       sharing='public')
    table_states = pd.read_sql("Select distinct hometown_region, count(*) players from rosters where Country = 'USA' group by hometown_region order by players desc;", con)

    fig = px.choropleth(
        data_frame=table_states,
        locationmode='USA-states',
        locations='hometown_region',
        scope="usa",
        color='players',
        hover_data=['hometown_region', 'players'],
        color_continuous_scale=px.colors.sequential.YlGnBu,
        labels={'hometown_region': 'State', 'players': 'Number of players'},
        template='plotly_dark'
    )
    fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})

    chart = py.plot(
        fig,
        filename='US_hockey',
        auto_open=False,
        fileopt='overwrite',
        sharing='public'
    )

#map()
