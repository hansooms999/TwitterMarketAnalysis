import requests
import ssl
import json
import datetime
import time
import api_access

#File contains methods for parsing tweets

#searches tweet for a Stock ticker, takes in pre-loaded json data
def search_tweet(data):
    
    result = "couldn't find ticker\n"
    upperwords = []

    #grabs data from tweet's text field and splits into a list, text seperated by whitespace
    words = data['text'].split()

    for word in words:
        # useful criteria = word.isupper() & (word[0] != '#') & (word != 'RT') & (word!='CEO') & (word!='AI')
        
        #common notation to precede tickers in tweets with cash tag
        if ((word[0] == '$')):
            if (word[1:].isalpha()):
                result = word[1:]

            #TODO: what case is this covering??
            elif (word[1:-2].isalpha()):
                result = word[1:-1]

        #lowercase ticker names uncommon and poor practice, will not consider them.
        elif(word.isupper()):
            if(word.isalpha()):
                if((word != "RT") & (word != "USMCA")):
                    result = word

            #checking if everything after first char is alphabetical
            elif(word[1:].isalpha()):
                result = word[1:]

            #checking if deduction of first and last char is alphabetical
            elif(word[1:-1].isalpha()):
                result = word[1:-1]
    #if result is beginning error message it prints error to terminal, length of six is too long to be any valid ticker
    if (len(result) > 6):
        print(result)
    else:

        output = open("output/" + result + "info.txt", "a")
        get_time_info(1,result, output)

def get_stock_info(ticker, output):
    cont = True
    print("got inside get_stock_info\n")
    try:
        r = requests.get('https://api.tdameritrade.com/v1/marketdata/' + ticker + '/quotes?apikey=' + api_access.TD_api_key)
        current_data = json.loads(r.text)
    except BaseException as e:
        output.write(ticker + " is not a valid ticker" + "\n")
        cont=False
    if (cont == True):
        
        #if keyword found in tweet is valid ticker, prints ticker info to terminal
        time = datetime.datetime.now()
        output.write("Time- " + str(time.hour) + ":" + str(time.minute) + "::" + str(time.second) + "\n")
        output.write("Symbol: " + ticker +  "\n")
        output.write("Bid: " + str(current_data[ticker]['bidPrice']) + "   Ask: " + str(current_data[ticker]['askPrice']) + "\n")
        output.write("Size: " + str(current_data[ticker]['bidSize']) + "      " + str(current_data[ticker]['askSize']) + "\n\n")

#TODO: printing to file instead of terminal
#TODO: get average daily volume data and compare to current days volume
#TODO: Analyze daily SMA trendline change

    #useful things timedelta, delta.total_seconds()

def get_time_info(period,ticker,output):
    get_stock_info(ticker, output)
    time.sleep(period)
    output.write(ticker + " :: " + str(period) + " seconds later" + "\n")
    get_stock_info(ticker, output)

