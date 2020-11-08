#import dependencies
from datetime import timedelta
import os
import os.path
import pandas as pd
from pathlib import Path
import dateutil.parser as dparser
import yfinance as yf
import csv
import matplotlib.pyplot as plt


#Data on desired timestamps
time_dict = {
    "1 mth":{"abriv":"1 mth","name":"1 month","startdelta":0,"enddelta":30},
    "6 mth":{"abriv":"6 mth","name":"6 months","startdelta":0,"enddelta":180},
    "1 yr":{"abriv":"1 yr","name":"1 year","startdelta":0,"enddelta":365},
    "2 yr":{"abriv":"2 yr","name":"2 years","startdelta":0,"enddelta":730},
}

#Pull dataframe from custom pre-cleaned csv file - only good dates and working ticker symbols included
#NOTE: this will need some work to re-integrate to the original raw csv
df_master = pd.read_csv("spills.csv")


#Modify "Dates" column into a single start date for each disaster 
for index, row in df_master.iterrows():         
    rawDoubleSplit = row.Dates.split(" - ")
    newdate = dparser.parse(rawDoubleSplit[0]).strftime('%Y-%m-%d')
    df_master.at[index, "Dates"] = newdate


#STOCK DATA
for index, row in df_master.iterrows():
    spillName = row["Spill"]
    tradingName = row["Trading Name"]
    ownerName = row["Owner"]  
    eventdateraw = dparser.parse(row["Dates"])

    x = "2 yr"
    dateStartDelta = eventdateraw - timedelta(days=time_dict[x]["startdelta"])
    dateEndDelta = eventdateraw + timedelta(days=(time_dict[x]["enddelta"]+20))

    dateStart = dateStartDelta.strftime('%Y-%m-%d')
    dateEnd = dateEndDelta.strftime('%Y-%m-%d')
    eventdate = eventdateraw.strftime('%Y-%m-%d')
    full_title = "{} ({})".format(spillName,eventdate)

    #attempt to download the data from yfinance
    print(x,spillName)
    dataTicker = yf.Ticker(tradingName)
    data = dataTicker.history(start=dateStart, end=dateEnd)[["Close"]]
    datarange = max(data["Close"]) - min(data["Close"]) 
    data.plot(figsize=(18,12),label=tradingName)
    plt.title(ownerName)
    plt.suptitle(full_title)
    plt.ylabel("Stock Price")
    
    #Vertical lines and line labels 
    for x in time_dict:
        linedate = eventdateraw + timedelta(days=time_dict[x]["enddelta"])
        plt.axvline(x=linedate, color='r')
        plt.annotate(time_dict[x]["abriv"],(linedate,(min(data["Close"])+(datarange/10))))
    
    #This displays the chart in a new popup window. Delete if desired. 
    plt.show()
    
    #This grayed section can save the chart to the desired directory. The spill names are shortened to 12 values. 
    #Remove the three quotes from the top and bottom to activate.
    '''
    pngTarget = f"/home/fred/Desktop/oil/pics/{spillName[:12]} - {abriv}.png"
    plt.savefig(pngTarget)
    '''

    #This removes the chart from memory, otherwise, making dozens of these in one Python session would tax the computer.
    plt.close()