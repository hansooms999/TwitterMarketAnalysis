import requests
import ssl
import json
import datetime
import time
import api_access
import re

MAX_TICKER_LENGTH = 5
TIME_INTERVAL_SECONDS = 20

#File contains methods for parsing tweets

#searches tweet for a Stock ticker, takes in pre-loaded json data
def search_tweet(data):
    
    result = "couldn't find ticker\n"
    upperwords = []

    #TODO:: change to REGEX
    #grabs data from tweet's text field and splits into a list, text seperated by whitespace
    words = data['text'].split()

    for word in words:
        # useful criteria = word.isupper() & (word[0] != '#') & (word != 'RT') & (word!='CEO') & (word!='AI')
        
        #common notation to precede tickers in tweets with cash tag
        if ((word[0] == '$')):
            if (word[1:].isalpha()):
                result = word[1:]

            #covering multiple punctuation marks at end TODO:: make this better
            elif (word[1:-2].isalpha()):
                result = word[1:-1]

        #lowercase ticker names uncommon and poor practice, will not consider them.
        elif(word.isupper()):
            if(word.isalpha()):
                if((word != "RT") & (word != "CEO") & (word != "AI") & (word != "USMCA")):
                    result = word

            #checking if everything after first char is alphabetical
            elif(word[1:].isalpha()):
                result = word[1:]

            #checking if deduction of first and last char is alphabetical
            elif(word[1:-1].isalpha()):
                result = word[1:-1]
    #if result is beginning error message it prints error to terminal
    if (len(result) > MAX_TICKER_LENGTH):
        print(result)
    else:

        output = open("output/" + result + "info.txt", "a")
        print("Found Ticker\n")
        get_time_info(result, output)

def get_stock_info(ticker, output):
    cont = True
    try:
        quote = requests.get('https://api.tdameritrade.com/v1/marketdata/' + ticker + '/quotes?apikey=' + api_access.TD_api_key)
        
    except BaseException as e:
        output.write("Could not access Quote for:: " + ticker + "\n")
        output.write("Error is:: " + str(e) + "\n")
        cont=False
    
    try:
        fund = requests.get('https://api.tdameritrade.com/v1/instruments?apikey=' + api_access.TD_api_key + '&symbol=' + ticker + '&projection=fundamental')
        
    except BaseException as e:
        output.write("Could not access Fundamentals for:: " + ticker + "\n")
        output.write("Error is:: " + str(e) + "\n")
        cont=False

    if (cont == True):

        quote_data = json.loads(quote.text)
        fund_data = json.loads(fund.text)
        #if keyword found in tweet is valid ticker, prints ticker info to terminal
        time = datetime.datetime.now()

        output.write("Time- " + str(time.hour) + ":" + str(time.minute) + "::" + str(time.second) + "\n")
        output.write("Symbol: " + ticker +  "\n")

        #In case where get API request passes and ticker is valid, but equity data is not retrievable (uncommon but not rare)
        try:
        
            output.write("Bid: " + str(quote_data[ticker]['bidPrice']) + "   Ask: " + str(quote_data[ticker]['askPrice']) + "\n")
            output.write("Size: " + str(quote_data[ticker]['bidSize']) + "      " + str(quote_data[ticker]['askSize']) + "\n")
            output.write("Average Vol (10-Day): " + str(fund_data[ticker]["fundamental"]["vol10DayAvg"]) + "\n\n")
        
        except BaseException as e:
            output.write("Equity Data is inaccessable for:: " + ticker + "\n")
            output.write("Error is:: " + str(e))
        
        

#TODO: get average daily volume data and compare to current days volume
#TODO: Analyze daily SMA trendline change


def get_time_info(ticker,output):
    get_stock_info(ticker, output)
    time.sleep(TIME_INTERVAL_SECONDS)
    output.write(ticker + " :: " + str(TIME_INTERVAL_SECONDS) + " seconds later" + "\n")
    get_stock_info(ticker, output)

    #close output file and thread terminates
    output.close()