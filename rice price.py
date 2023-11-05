import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, ifft
import pandas as pd
from sklearn.preprocessing import normalize

import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

plt.figure(figsize = (8, 6))


df = pd.read_csv("data/wfp_food_prices_nga.csv")
df = df[df["unit"] == "100 KG"]
# df = df.drop(0)
df[df["commodity"]=="Rice (local)"]
df["price"] = df["price"].apply(pd.to_numeric)
df["date"] = pd.to_datetime(df["date"])
df = df[df["date"]>pd.to_datetime("2016-1-1")]
df = df[df["date"]<pd.to_datetime("2023-1-1")]

# We remove some charity markets
# for market in [ "Mai Gatari (CBM)"
#     # "Aba"
# , "Jibia (CBM)"
# , "Mai Adoua (CBM)"
# , "Illela (CBM)"
# # , "Bolori Stores"
# ]:
#     df = df[df["market"]!=market]

# df.sort_values("price", ascending=False).head(180)
# df= df.drop(
#     df[df["price"]==df["price"].max()].index[0]
#     , axis = 0
# )

# remove markets: 
# [0]
# for market in df["market"].unique():
    # market = df["market"].unique()[1]
# dfm = df.loc[df["market"]==market]
df = df[["price", "date"]]
df["price"] = df["price"].apply(pd.to_numeric)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by='date')
# # df = df.groupby(by="date").mean()

# plt.plot(df.index
#             , df["price"]
#             , 'tan')
# plt.ylabel("Price of Rice")

# plt.show()

df = df.drop(
    df[df["price"]==0].index
    , axis = 0
)

ok = pd.DataFrame()
ok["max"]=df.groupby(by="date").max()["price"]
ok["min"]=df.groupby(by="date").min()["price"]
ok["open"]=df.groupby(by="date").first()["price"]
ok["close"]=df.groupby(by="date").last()["price"]
ok["date"] = df["date"].unique()
ok["date"] = ok["date"].astype('O')

fig = go.Figure(data=[
    go.Candlestick(x=ok["date"],
    open=ok["open"],
    high=ok["max"],
    low=ok["min"],
    close=ok["close"]
    )
])


fig.update_layout(
    title='Rice Prices in Nigeria',
    yaxis_title='Naira',
    shapes = [dict(
        x0='2022-02-21', x1='2022-02-21', y0=0, y1=1, xref='x', yref='paper',
        line_width=2)],
    annotations=[dict(
        x='2022-02-21', y=0.05, xref='x', yref='paper',
        showarrow=False, xanchor='left', text='Russo-Ukraine War')],
    legend=dict(
        x=0,
        y=1,
        traceorder="reversed",
        title_font_family="Times New Roman",
        font=dict(
            family="Courier",
            size=12,
            color="black"
        ),
        bgcolor="LightSteelBlue",
        bordercolor="Black",
        borderwidth=2
    )
)

fig.write_html("riceprice.html")
fig.show()



# ["Aba"
# , "Mai Gatari (CBM)"
# , "Jibia (CBM)"
# , "Mai Adoua (CBM)"
# , "Illela (CBM)"
# , "Bolori Stores"
# ]

# Potiskum


