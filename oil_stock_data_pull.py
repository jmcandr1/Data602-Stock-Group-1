#Needed libraries
import pandas
import yfinance as yf

#Dictionary of desired stock tickers
stockdict = {
  "RDS-OLD" : {
    "ticker" : "RDS",
    "name" : "Royal Dutch Shell - Old ('00-'17)"},
  "RDS-New" : {
    "ticker" : "RDS-A",
    "name" : "Royal Dutch Shell - Now ('05-'20)"},
  "BP" : {
    "ticker" : "BP",
    "name" : "BP"},
  "Exxon" : {
    "ticker" : "XOM",
    "name" : "ExxonMobil"},
  "Total SE" : {
    "ticker" : "TOT",
    "name" : "Total SE"},  
  "Chevron" : {
    "ticker" : "CVX",
    "name" : "Chevron Corp"},
  "Marathon" : {
    "ticker" : "MPC",
    "name" : "Marathon Petroleum Corp"},
  "Conoco" : {
    "ticker" : "COP",
    "name" : "ConocoPhillips"},
  "TC Energy" : {
    "ticker" : "TRP",
    "name" : "TC Energy"},
  "Sunoco" : {
    "ticker" : "SUN",
    "name" : "Sunoco LP"}
}

#Address of computer folder to store data in CSVs
fileaddress = "/home/fred/Desktop/stock"

#Loop code runs through every company in stockdict
for x in stockdict:

	#Pulls ticker code from stockdict
	tickercode = stockdict[x]["ticker"]

	#Date range formatted to catches a stock's entire history. Start date is arbitrarily old; Yahoo Finance will include earliest avaiable data
	startvalue = "1930-01-01"
	endvalue = "2020-10-10"

	print(x)

	#Accesses this ticker
	tickerData = yf.Ticker(tickercode)

	#Pulls historical prices for this ticker
	tickerDf = tickerData.history(start=startvalue, end=endvalue)

	#Prints preview of data
	print(tickerDf)
	input()

	#Combines fileaddress string with unqiue file name and csv extension
	target = fileaddress+"/"+stockdict[x]["name"]+".csv"
	print(target)

	#Turns yfinance dataframe into a CSV at target folder on your computer
	tickerDf.to_csv(target)