#Timelines: 1 day, 1 month, 6 months, 1 year, 2 years
from datetime import datetime as dt
from datetime import timedelta
import os
import os.path
import pandas as pd
from pathlib import Path
import dateutil.parser as dparser
import yfinance as yf
from datetime import datetime as dt
import csv
import matplotlib.pyplot as plt


df_raw = pd.read_csv("spills.csv", index_col=False, header=0)
df_master = df_raw[["Spill","Dates","Owner","Trading Name"]]
df_companies = pd.read_csv("companies.csv", index_col=False, header=0)

#date correction to production dataframe      
thisYear = int(dt.today().strftime("%Y"))

for index, row in df_master.iterrows():         
    rawDoubleSplit = row.Dates.split(" - ")
    rawSplitFirst = (dparser.parse(rawDoubleSplit[0]))
    newdate = rawSplitFirst.strftime('%Y-%m-%d')
    df_master.at[index, "Dates"] = newdate

#STOCK DATA
for index, row in df_master.iterrows():
    spillName = row["Spill"]
    tradingName = row["Trading Name"]
    ownerName = row["Owner"]  
    eventdateraw = dparser.parse(row["Dates"])

    dateStartDelta = eventdateraw - timedelta(days=7)
    dateEndDelta = eventdateraw + timedelta(days=7)

    dateStart = dateStartDelta.strftime('%Y-%m-%d')
    dateEnd = dateEndDelta.strftime('%Y-%m-%d')
    eventdate = eventdateraw.strftime('%Y-%m-%d')
    csvTarget = f"/home/fred/Desktop/oil/{tradingName}.csv"

    #attempt to download the data from yfinance
    if index > 7:
        break

    print(eventdate)
    try:
        dataTicker = yf.Ticker(tradingName)
        data = dataTicker.history(start=dateStart, end=dateEnd)[["Close"]]
        data.plot()
        plt.title(eventdate)
        plt.suptitle(spillName)
        plt.axvline(x=eventdate,linewidth=4, color='r')
        pngTarget = f"/home/fred/Desktop/oil/pics/{spillName[:14]} 14-days"
        plt.savefig(pngTarget)



    except Exception as exception:
        print(f"Exception {exception} for {ownerName} for time period {dateStart} - {dateEnd}")
