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





'''                 
 

    except Exception as exception:

        print(f"Exception {exception} for {ownerName} for time period {dateStart} - {dateEnd}")

print("Completed.  Review errors and correct before continuing.")


#Fill in interval adjusted closing values.  If date not listed, get closest date before incident
#and then date closest after for remainder of intervals

for index, row in df_master.iterrows():
    
    ownerName = row["Owner"]
    dates = row["Dates"]
    dateSplit = dates.split(" - ")  
    dateStartDelta = (dparser.parse(dateSplit[0])) - timedelta(days=7)
    dateEndDelta = (dparser.parse(dateSplit[1])) + timedelta(days=737)   
    
    dateStart = dateStartDelta.strftime('%Y-%m-%d')
    dateEnd = dateEndDelta.strftime('%Y-%m-%d') 
    
    dayBeforeDelta = (dparser.parse(dateSplit[0])) - timedelta(days=1)
    dayBefore = dayBeforeDelta.strftime('%Y-%m-%d') 
    
    csvTarget = f"stocks/{ownerName} {dateStart} - {dateEnd}.csv"
    
    datesCSV = pd.read_csv(csvTarget, index_col=False, header=0)
    
    dates = pd.to_datetime(datesCSV["Date"])
    
    #try initial dates.  If these are after the date of the incident, it will be 
    #be apparent in the output and can be corrected.  If no data for date, choose nearest one before  
        
    dayPrior = datesCSV.loc[datesCSV["Date"] == dayBefore]["Close"].tolist()   
    
    if dayPrior == []:
        
        parsedDayBefore= pd.to_datetime(dayBefore)
        fixedDateCalc = min([i for i in dates if i < parsedDayBefore], key=lambda x: abs(x - parsedDayBefore))
        fixedDate = fixedDateCalc.strftime('%Y-%m-%d')

        #print(f"nearest date to {dayBefore} is {fixedDate}  for {csvTarget}.  Check for sanity.") 

        dayPrior = datesCSV.loc[datesCSV["Date"] == fixedDate]["Close"].tolist()
    
    df_master.at[index, "Day Prior"] = dayPrior[0]
    
    #then do the rest as the remainder do not require any supervision after initial sanity check and want nearest date after
        
    dayAfterDelta = (dparser.parse(dateSplit[0])) + timedelta(days=1)
    dayAfter = dayAfterDelta.strftime('%Y-%m-%d') 
    
    oneMonthDelta = (dparser.parse(dateSplit[0])) + timedelta(days=30)
    oneMonth = oneMonthDelta.strftime('%Y-%m-%d')         
        
    sixMonthDelta = (dparser.parse(dateSplit[0])) + timedelta(days=180)
    sixMonth = sixMonthDelta.strftime('%Y-%m-%d')         
    
    oneYearDelta = (dparser.parse(dateSplit[0])) + timedelta(days=365)
    oneYear = oneYearDelta.strftime('%Y-%m-%d') 
    
    twoYearDelta = (dparser.parse(dateSplit[0])) + timedelta(days=730)
    twoYear = twoYearDelta.strftime('%Y-%m-%d') 
    
    tryDict = {dayAfter:"Day After", oneMonth: "1 Month", sixMonth: "6 Months", oneYear: "1 Year", twoYear: "2 Years"}
           
    for key,value in tryDict.items():
       
        targetClose = datesCSV.loc[datesCSV["Date"] == key]["Close"].tolist()
        #print(f"targetClose {targetClose}")
            
        if targetClose == []:
            
            parsedDate = pd.to_datetime(key)
            
            try:
                fixedDateCalc = min([i for i in dates if i > parsedDate], key=lambda x: abs(x - parsedDate))
                fixedDate = fixedDateCalc.strftime('%Y-%m-%d')
                
                targetClose = datesCSV.loc[datesCSV["Date"] == fixedDate]["Close"].tolist()
                print(f"nearest date to {key} is {fixedDate}  for {ownerName}.  Check for sanity.") 
                             
            except:
                
                targetClose = ["NaN"]
                print(f"Date {fixedDate} not in range for {ownerName}.  NaN value placed.")
                
        else:

            targetClose = datesCSV.loc[datesCSV["Date"] == fixedDate]["Close"].tolist()

        #print(f"{tryDict[key]} will equal {targetClose} for {ownerName}.  Verify with random sample.")
        
df_master.to_csv(r"OilSpills-Production.csv", index = False, header=True)  
df_excluded.to_csv(r"OilSpills-Excluded.csv", index =False, header=True)

print("Complete.  Data scrub finished.")
'''