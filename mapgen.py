import pandas as pd
import plotly
import plotly.plotly as py


plotly.tools.set_credentials_file(username='ispbs', api_key='0nU4SSsDjKAaOHYaJPKn')

df = pd.read_csv('windtype.csv')
new_df = df.drop_duplicates(['Country'], keep='last')



data = [ dict(
        type = 'choropleth',
        locations = new_df['Code'],
        z = new_df['Type'].astype(int),
        text = new_df['Country'],
        colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            )
        ),
        colorbar = dict(
            tickprefix = 'W',
            title = 'Extreme wind Type 10-min (m/s): \n W1: 0-20 \n W2: 20-31 \n W3: 31-35 \n W4: 35-45 \n W5: 45-55'

        ),
    ) ]

layout = dict(
    title = 'Extreme wind climates worldwide',
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict(data=data, layout=layout )
url = py.plot(fig, filename='d3-world-map')