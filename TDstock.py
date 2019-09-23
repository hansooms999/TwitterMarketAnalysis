import requests
import ssl
import json
import datetime
import time
import api_access

#File contains methods for parsing tweets

def search_tweet(data):
    
    result = "couldn't find ticker"
    upperwords = []
    words = data['text'].split()
    for word in words:
        # useful criteria = word.isupper() & (word[0] != '#') & (word != 'RT') & (word!='CEO') & (word!='AI')
        
        #  to determine any upper case tickers that may be missing
        
        if ((word[0] == '$')):
            print(word)
            if (word[1:].isalpha()):
                result = word[1:]
            
            elif (word[1:len(word)-2].isalpha()):
                result = word[1:len(word)-1]
        elif(word.isupper()):
            if(word.isalpha()):
                result = word
            elif(word[1:].isalpha()):
                result = word[1:]
            elif(word[1:len(word)-1]):
                result = word[1:len(word)-1]
    if (len(result) > 7):
        print(result)
        print(upperwords)
    else:
        
        get_time_info(20,result)

def get_stock_info(ticker):
    cont = True
    try:
        r = requests.get('https://api.tdameritrade.com/v1/marketdata/quotes?apikey='+ TD_api_key +'symbol=' + ticker)
        current_data = json.loads(r.text)
    except BaseException as e:
        print(ticker + " is not a valid ticker")
        cont=False
    if (cont == True):
        
        #if keyword found in tweet is valid ticker, prints ticker info to terminal
        time = datetime.datetime.now()
        print("\nTime- " + str(time.hour) + ":" + str(time.minute) + "::" + str(time.second))
        print("Symbol: " + ticker)
        print("Bid: " + str(current_data[ticker]['bidPrice']) + "   Ask: " + str(current_data[ticker]['askPrice']))
        print("Size: " + str(current_data[ticker]['bidSize']) + "      " + str(current_data[ticker]['askSize']) + "\n")

#TODO: printing to file instead of terminal
#TODO: get average daily volume data and compare to current days volume
#TODO: Analyze daily SMA trendline change

    #useful things timedelta, delta.total_seconds()

def get_time_info(period,ticker):
    get_stock_info(ticker)
    time.sleep(period)
    print(ticker + ": " + str(period) + " seconds later")
    get_stock_info(ticker)

