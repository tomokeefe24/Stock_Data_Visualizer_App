from flask import Flask, render_template, request, url_for, flash, redirect, abort
from datetime import datetime
from StockService import StockService
from StockChart import StockChart
from StockExceptions import StockQueryException, StockQueryLimitException, StockEndpointException
from Utility import Utility
import csv

API_KEY = "MOGEQQ2S4EB1STVP"
app = Flask(__name__)
app.config["DEBUG"] = True
csvfile = "stocks.csv"

app.config['SECRET_KEY'] = 'your secret key'

def getStockData(ticker: str, timeSeries: int, chartType: str, startDate: datetime, endDate: datetime):
    service = StockService(API_KEY)
    

    if timeSeries == 1:
        return service.get_intraday(ticker, startDate, endDate)
    elif timeSeries == 2:
        return service.get_daily(ticker, startDate, endDate)
    elif timeSeries == 3:
        return service.get_weekly(ticker, startDate, endDate)
    elif timeSeries == 4:
        return  service.get_monthly(ticker, startDate, endDate)

def checkDates(d1,d2):   
    if d1 > d2:
        return False
    else:
        return True
    
def checkIntra(ts, d1, d2):
    dif = d2-d1
    difDays = dif.total_seconds()/86400

    if difDays > 30 and ts == 1:
        return True
    else:
        return False
    
def getSymbols():
    rows = []
    symbols = []
    with open(csvfile, "r") as theFile:
        csvreader = csv.reader(theFile)
        fields = next(csvreader)

        for row in csvreader:
            rows.append(row)
        symbols = [x[0] for x in rows]

        return symbols
    
def checkInputs(s, ts, ct):
    if not s.isupper() or not s.isalpha():
        return "Invalid Symbol"
    elif not ts.isdigit() or not ts in ["1", "2", "3", "4"]:
        return "invalid time series"
    elif not ct.isdigit() or not ct in ["1", "2"]:
        return "invalid chart type"
    else:
        return 0

    
    




    



@app.route('/', methods=('GET', 'POST'))
def index():
    chart_serv = StockChart()
    symbols = getSymbols()
    if request.method == "POST":
        symbol = request.form["symbol"]
        chartType = request.form["chartType"]
        timeSeries = request.form["timeSeries"]
        startDate = request.form["startDate"]
        endDate = request.form["endDate"]

        try:
            startDate = datetime.strptime(startDate, '%Y-%m-%d')
            endDate = datetime.strptime(endDate, '%Y-%m-%d')
        except:
            flash("invalid date")
            return render_template("index.html", symbols=symbols)
        

        #error checking
        message = checkInputs(symbol, timeSeries, chartType)
        if not message == 0:
            flash(message)
            return render_template("index.html", symbols=symbols)

        if not checkDates(startDate, endDate):
            flash("Start Date must be before End Date")
            return render_template("index.html", symbols=symbols)

        if checkIntra(timeSeries, startDate, endDate):
            flash("Intraday requests must be shorter than 30 days")
            return render_template("index.html", symbols=symbols)
        
        
        try:
            stockData = getStockData(symbol, int(timeSeries), int(chartType), startDate, endDate)
        except StockQueryLimitException:
            flash("API Limit Reached.")
            return render_template("index.html", symbols=symbols)
        except StockQueryException:
            flash("please select a valid symbol")
            return render_template("index.html", symbols=symbols)
        
            
        
        if stockData == None:
            flash("no Stock Data")
            return render_template("index.html",symbols=symbols)
        

        
        chart = chart_serv.graphData(int(chartType), stockData)
        


        return render_template("index.html", chart=chart, symbols=symbols)
        
        
    return render_template("index.html", symbols=symbols)


app.run(host="0.0.0.0")





