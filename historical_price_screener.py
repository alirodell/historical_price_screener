#!/usr/bin/python3

import requests
import datetime


    # This script queries from Yahoo Finance using their YQL protocol.
    #
    # The YQL request returns a dictionary object of one entry 'query'.
    # This query is also a dictionary object with five list objects in it:
    #    diagnostics
    #    results
    #    lang
    #    created
    #    count
    #
    # We are interested in the results dictionary which then has a 'quotes'
    # key where the value is a list of dictionaries corresponding to each trading day. 
    # This is what we are passing into the "Security" object in the init method.
    ##################################################
    
    # Where we are:
    #  - We are inserting the stock symbol into the YQL statement and then executing it and parsing out results.
    #  - We've got the Security object mostly set up, still need to set up the "set methods"
    #  - The "TradingDay" object is set up and working well, all get/set methods are written and we can sort a list of them.
    #  - We're calculating the 10 day SMA for a security as of the last trading day we have. See Questions on this one.
    #
    ###################################################
    
    
    # Things to do.
    # 1. Need to be able to programatically insert the date ranges into the YQL statement based on trailing days back from today.
    # 2. Need to write the EMA20 and EMA30 methods. -> need to figure out how to do this with previous EMA's not available.
    # 3. Need to turn the SMA10 calcs into a method. -> DONE
    # 4. Need to spot check the math to ensure I'm iterating correctly.
    #
    ###################################################
    
    # Questions:
    #  - I'm not sure I should be calculating the SMA in the Security object instead of doing it for each trading day and then just taking the last value.
    #
    #
    #
    #
    ###################################################
    
    
    
     

class TradingDay:
    def __init__(self, sec_trading_data = None):
        self._data = sec_trading_data      
 
        # Assign the day's data to object properties.
        if self._data != None:
            self._symbol = self._data['Symbol']
            self._open = float(self._data['Open'])
            self._close = float(self._data['Close'])
            self._volume = int(self._data['Volume'])
            self._adj_close = float(self._data['Adj_Close'])
            self._low = float(self._data['Low'])
            self._high = float(self._data['High'])
            date_parts = self._data['Date'].split('-')
            self._date = datetime.date(int(date_parts[0]),int(date_parts[1]),int(date_parts[2]))
    
    # Set this so that you can just call .sort() on a list of these objects and sort them by date.
    def __lt__(self,other):           
        return self.get_date() < other.get_date()
        
    def get_symbol(self):
        return self._symbol
        
    def get_open(self):
        return self._open
        
    def get_close(self):
        return self._close
        
    def get_volume(self):
        return self._volume
        
    def get_adj_close(self):
        return self._adj_close
        
    def get_low(self):
        return self._low
        
    def get_high(self):
        return self._high
        
    def get_date(self):
        return self._date
    
    def set_symbol(self, s):
        self._symbol = s
        
    def set_open(self, s):
        self._open = s
        
    def set_close(self, s):
        self._close = s
        
    def set_volume(self, s):
        self._volume = s
        
    def set_adj_close(self, s):
        self._close = s
        
    def set_low(self, s):
        self._low = s
        
    def set_high(self, s):
        self._high = s
        
    def set_date(self, d):
        self._date = d
        


class Security:
    def __init__(self, security_data_list = None):
        
        # security_data_list is a list of dictionary objects containing historical prices for the security.
        self._data = security_data_list      
        self._10_day_sma = 0.0
        self._20_day_ema = 0.0
        self._30_day_ema = 0.0
        self._current_day_volume = 0
        self._current_day_adj_close = 0.0
        
        
        # make sure that the list was passed in and that it has 30 days of security prices.
        # Right now we are selecting 124 days of historical data, need to change the date parsing in the query generation process.
        # Still need to add the 30 day compare and build out assigning variables.  Moving out to parsing out the Yahoo query first so we can loop back in.
                
        self._trading_day_list = []
        
        # Each iteration of i will be a dictionary object holding a days trading data which will be passed in with the init function of the TradingDay object..
        if self._data != None:
            for i in self._data:
                #print(i)
                day = TradingDay(i)
               
                self._trading_day_list.append(day)
                
        # This sorts the trading days by date.        
        self._trading_day_list.sort()
        
        num_trd = len(self._trading_day_list)
        
        print("This is the total number of trading days - {}".format(num_trd))    
        # Now we are ready to start calculating moving averages.
           
               
        # Calculate and assign the moving averages
        self._10_day_sma = self.calc_simple_moving_average(10, num_trd)
        self._20_day_ema = self.calc_exp_moving_average(20, num_trd)
        self._30_day_ema = self.calc_exp_moving_average(30, num_trd)
        
        # Assign the other values - these are all for the current trading day only.
        # We are running this script after the market closes. 
        self._current_day_adj_close = self._trading_day_list[num_trd - 1].get_adj_close()
        
        print(self._trading_day_list[num_trd - 1].get_date())
       
        

        
            
        #print("This is the SMA10 value {}".format(self.get_10_day_sma()))    
            #print("Stock symbol {} and date {}".format(trading_day.get_symbol(), trading_day.get_date()))
    
    def calc_exp_moving_average(self, period = 0, num_trd_days = 0):
                
        ema = 0.0
        
        if period > 0 and num_trd_days > 0:
            # need to calculate the previous days EMA in order to return the EMA.  Need to think on how to do this.
            # -> use the 20 day SMA for that value and do this outside the function.
            # EMA Formula is (Close - EMA(previous day)) * multiplier + EMA(previous day)
            # If there is no EMA from before then you use the SMA.
            
            def calc_ema(close = 0.0, previous_day_ema = 0.0):
                multiplier = 2 / (period + 1)
                return (close - previous_day_ema) * multiplier + previous_day_ema
                        
            
            # First, calculate the SMA from the first available period based on the argument "period"
            initial_sma = self.calc_earliest_simple_moving_average(period,num_trd_days)
            #print("The initial_sma for your stock is {}.".format(initial_sma))
                                  
            # Now I calculate the EMA's for the remaining days leading all the way up to today.
            remaining_days = num_trd_days - period
            
            # Need to define a dictionary of ema's mapping date to EMA value.
            ema_list = {}
            last_day = ''
            ema = 0.0
            
            # Add the dictionary entries.
            for k in range(period, num_trd_days):
                # First time through just use the initial_sma, otherwise use the previous period ema
                previous_ema = 0.0
                #print("k is {}, the period is {}, and the number_trd_Days is {}".format(k,period,num_trd_days))
                
                if k == period:
                    previous_ema = initial_sma
                else:
                    #print("Yesterdays close was {} and yesterdays ema was {}".format(self._trading_day_list[k-1].get_adj_close(),ema_list[str(self._trading_day_list[k-1].get_date())]))
                    previous_ema = ema_list[str(self._trading_day_list[k-1].get_date())]
                
                #print("The previous day's ema is {}".format(previous_ema))
                #print("The date I'm adding to the dict is {} and the {} day ema for that date is {}".format(str(self._trading_day_list[k].get_date()), period, calc_ema(self._trading_day_list[k].get_adj_close(),previous_ema)))
                #print("--------------------------------")
                ema_list[str(self._trading_day_list[k].get_date())] = calc_ema(self._trading_day_list[k].get_adj_close(),previous_ema)
                
                # Store the last date to return the final EMA.
                if k == num_trd_days-1: ema = calc_ema(self._trading_day_list[k].get_adj_close(),previous_ema)
                
                
            

            #print(last_day)
            #ema = ema_list[last_day]
            
        return ema
    
    # This method will earliest period SMA for a given period based on the trading_day_list
    # that was set in the init function. It returns a float
    # if the value returned is a zero then something went wrong.
    def calc_earliest_simple_moving_average(self, period = 0, num_trd_days = 0):
        sma_10_total = 0.0
        sma = 0.0
        if period > 0 and num_trd_days > 0:
            
            for i in range(period):
                
                #print("i is {} and the adjusted closing price on {} is {}".format(i, self._trading_day_list[i].get_date(), self._trading_day_list[i].get_adj_close()))
                
                sma_10_total += self._trading_day_list[i].get_adj_close()
                #print("initial sma total is {}".format(sma_10_total))
                sma = sma_10_total / period
        return sma    
     
    # This method will calculate the current SMA for a given period based on the trading_day_list
    # that was set in the init function. It returns a float
    # if the value returned is a zero then something went wrong.
    
    # Checked this against Fidelity reported SMA and they agree.
    def calc_simple_moving_average(self, period = 0, num_trd_days = 0):
        sma_10_total = 0.0
        sma = 0.0
        if period > 0 and num_trd_days > 0:
            
            for i in range(period):
                
                #print("i is {} and the adjusted closing price on {} is {}".format(i, self._trading_day_list[num_trd_days-(i+1)].get_date(), self._trading_day_list[num_trd_days-(i+1)].get_adj_close()))
                
                # Have to add 1 to i since ranges in Python are non-inclusive.
                sma_10_total += self._trading_day_list[num_trd_days-(i+1)].get_adj_close()
                #print("sma total is {}".format(sma_10_total))
                sma = sma_10_total / period
        return sma
    
    def get_10_day_sma(self):
        return self._10_day_sma
    
    def get_20_day_ema(self):
        return self._20_day_ema
    
    def get_30_day_ema(self):
        return self._30_day_ema
    
    def get_raw_data(self):
        return self._data
    
    def get_volume(self):
        return self._current_day_volume
    
    def get_adj_close(self):
        return self._current_day_adj_close

    # I'm not sure I want to set "set" methods here, I don't see a case when I would use them.
    # These are just a mistake waiting to happen.
    #def set_10_day_sma(self):
    #    return self._10_day_sma
    
    #def set_20_day_ema(self):
    #    return self._20_day_ema
    
    #def set_30_day_ema(self):
    #    return self._30_day_ema
    
    #def set_raw_data(self):
    #    return self._data


        

def main():

    # This list of stocks we will iterate through to select historical data from yahoo finance.
    # This list -MUST- have at least two stocks in it in order for this script to work.
    the_stocks = ("ABIL", "AMD", "MET", "GOOG", "T", "GPRO")
 
    # this is the base URL that will be used to query Yahoo finance for historical pricing data.
    # we will replace the #### string with the stock symbol when looking through the_stocks tuple.
    
    # For the purposes of development I am having the end_date be yesterday so that I can run this during the day.  Usually this will run at night so we can get the close prices.
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    # Start date is represented by @@@@ in the url.
    # Go back 100 calendar days which should give us around 70 trading days.
    start_date = end_date - datetime.timedelta(days=300)
     
    
    #print("The type of start_date is {} and the actual date is {}".format(type(start_date), start_date))
    #print("The type of end_date is {} and the actual date is {}".format(type(end_date), end_date))
    
    
    historical_data_url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22###%22%20and%20startDate%20%3D%20%22SSSS%22%20and%20endDate%20%3D%20%22EEEE%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='    
    
    historical_data_url = historical_data_url.replace('SSSS', str(start_date))
    historical_data_url = historical_data_url.replace("EEEE", str(end_date))
        
    #print(historical_data_url)
    #historical_data_url.replace("^^^^", str(end_date))
    
    for k in the_stocks:
        
        print("-----------------Starting work on stock symbol {}.------------------------".format(k))
        # Generate the YQL string.
        specific_query = historical_data_url.replace("###",k)
        
        #print(specific_query)
        # I could embed the following in a long one line assignment but I'll never remember what I did later so I'm breaking them out.       
                
        hist_resp = requests.get(specific_query)
        
        bulk_response = hist_resp.json()['query']
        
        results_dict = bulk_response['results']
        
        quote_list = results_dict['quote']
        
        if hist_resp.status_code != 200:
            # This means something went wrong.
            print("You didn't receive a 200 code from Yahoo, you received a {}.".format(hist_resp.status_code))
    
               
        my_stock = Security(quote_list)
        up_signal_generated = False
        down_signal_generated = False
        ten_day_sma = my_stock.get_10_day_sma()
        twenty_day_ema = my_stock.get_20_day_ema()
        thirty_day_ema = my_stock.get_30_day_ema()
        
        # Check for up-trend
        if ten_day_sma > twenty_day_ema or ten_day_sma > thirty_day_ema: up_signal_generated = True
        
        # Check for down-trend
        if ten_day_sma < twenty_day_ema or ten_day_sma < thirty_day_ema: down_signal_generated = True
        
        if up_signal_generated: 
            print("We have a up-trend signal from {}".format(k))
            # Check if the stock has a stored up-trend.  If so, then ignore.  
            # If not, then update the db to indicate true for up-trend, update down-trend to false, and insert the date, then notify.
            # We can have a current-trend table to store up-trend, down-trend true/false values and the date the trend began.  
            # We can have a trend history table to store the occurrence of up-trend / down-trend.
            
            
        
        
        elif down_signal_generated: 
            print("We have a down-trend signal from {}".format(k))
            # When a down-trend occurs we check if the stock has a stored down-trend. 
            # If so, we ignore, if not, then update the down-trend bit to true, update the up-trend bit to false, insert the date, then notify.
        
        
        
        else:
            print("No trend detected for {} which means the SMA and EMA are equal".format(k))
        
        
        print("Current 10 say SMA is {}, current 20 day EMA is {}, and current 30 day EMA is {}".format(my_stock.get_10_day_sma(), my_stock.get_20_day_ema(),my_stock.get_30_day_ema()))
        
        
        
        print("-----------------End work on stock symbol {}.------------------------".format(k))
        
    print("All Done.")

    
    




if __name__ == "__main__": main()