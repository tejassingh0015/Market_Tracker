from binance.client import Client
from datetime import datetime
import pytz  # for working with time zones

API_KEY = 'co6LEXLgtMxjETwZmrN7TlpESjlFttEFet3529X2mGm0T1uqdwLAXOmp3pNnpew3'
API_SECRET = '4NyaRIuBVXFuZFQdNu4te4epmlnBr1zwtwPxBOOa9pObjEcbkH5f5dyz2KS7Ima0'

# Initialize the Binance client
client = Client(API_KEY, API_SECRET)

####################################################################################################
####################################################################################################

risk_percentage = 0.04  # 4% risk
account_balance = 14.4  # $ account balance

# Enter here : hunt the timed candles with 0.5 RR


symbol  = 'chrUSDT'       # EDIT
hour    =  10            # EDIT     # UTC, currently set to 5-minute interval
minute  =  50             # EDIT
#positionside = 'BUY'     # EDIT
positionside = 'SELL'    # EDIT 


# Date_Time
month=1       # Jan 2024 
day=23 

Decimal_qty = 0         # EDIT THIS (RARE)


################################
################################



# Define the symbol (trading pair) and the time interval for the candlestick data
symbol = symbol  # Replace with the trading pair you want to trade, e.g., 'BTCUSDT'
interval = Client.KLINE_INTERVAL_5MINUTE  # 5-minute interval

# Define the custom date and time for the candle (e.g., January 1, 2024, 15:00 UTC)
candle_time = datetime(year=2024, month=month, day=day, hour=hour, minute=minute, second=0, microsecond=0, tzinfo=pytz.utc)

# Retrieve the klines (candlestick data) for the symbol and interval
klines = client.futures_klines(symbol=symbol, interval=interval)

# Initialize variables to store high and low
high = None
low = None

# Loop through the klines and find the one that matches the custom start time
for kline in klines:
    kline_start_time = datetime.utcfromtimestamp(kline[0] / 1000).replace(tzinfo=pytz.utc)
    
    # Check if the kline's start time matches the custom time
    if kline_start_time == candle_time:
        high = float(kline[2])  # High price of the candle
        low = float(kline[3])   # Low price of the candle
        break

if high is not None and low is not None:
    # Determine the number with the longest decimal places
    decimal_places_high = len(str(high).split('.')[1])
    decimal_places_low = len(str(low).split('.')[1])
    
    # Select the maximum decimal places
    decimal_places = max(decimal_places_high, decimal_places_low)
    
    # Format the high and low values with the determined decimal places
    formatted_high = f"{high:.{decimal_places}f}"
    formatted_low = f"{low:.{decimal_places}f}"
    high = float(formatted_high)
    low = float(formatted_low)
    print("\n")
    print(f"High on {candle_time}: {high}")
    print(f"Low on {candle_time}: {low}")
    print("\n")
else:
    print(f"Candle data not found for the specified time: {candle_time}")
#########################

# Enter numbers here
Coin = symbol                  # EDIT THIS
positionside = positionside    # EDIT THIS
high = high                    # EDIT THIS
low = low                      # EDIT THIS

Decimal_qty = Decimal_qty                # EDIT THIS (RARE)




#Decimal Calculation
def count_decimal_places(number):
    if isinstance(number, (float, int)):
        # Convert the number to a string
        number_str = str(number)
        
        # Check if there's a decimal point in the string
        if '.' in number_str:
            decimal_places = len(number_str.split('.')[1])
            return decimal_places
        else:
            return 0
    else:
        raise ValueError("Input must be a floating-point number or integer")

decimal_places1 = count_decimal_places(high)
decimal_places2 = count_decimal_places(low)
highest_decimal = max(decimal_places1, decimal_places2)
Decimal_entry = highest_decimal        # Calculated from function above



#Calculation - Strategy is to hunt stoploss with 0.11 RR

risk_amount = account_balance * risk_percentage
price_gap_dif = (high - low)
qtycalc = risk_amount / price_gap_dif
qtycalc = round(qtycalc, Decimal_qty)

# Set the price based on the position side
if positionside == 'BUY':
    price = round(low - (0.1*(high-low)), highest_decimal)  # If buying, set the price to the low
    make_stoploss = round(low - (2 * price_gap_dif), highest_decimal)
    make_takeprofit = high

elif positionside == 'SELL':
    price = round(high + (0.1*(high-low)), highest_decimal)  # If selling, set the price to the high
    make_stoploss = round(high + (2 * price_gap_dif), highest_decimal)
    make_takeprofit = low


else:
    raise ValueError("Invalid positionside value")

print("Coin = " , Coin)
print("Side = " , positionside)
print("Entry = " , price)
print("Quantity = " , qtycalc)
print("Highest Decimals =", highest_decimal)
print("High =", high)
print("Low =", low)
print("\n")
print("Acc =", account_balance)
print("Candle % =", round((((high - low)/high)*100), 2))
print("\n")
print("Make StopLoss =", make_stoploss)
print("Make TakeProfit =", make_takeprofit)
print("\n")

# Define the trading parameters
symbol = Coin  # Replace with the trading pair you want to trade
side = positionside        # 'BUY' or 'SELL'
quantity = qtycalc      # Quantity of the asset you want to buy/sell
price = price     # Price at which you want to place the order
order_type = Client.ORDER_TYPE_LIMIT
timeinforce = 'GTC'  # Good Till Cancel




# Place the order
try:
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        quantity = quantity,
        price=price,
        type=order_type,
        timeInForce=timeinforce
        
    )
    print(f"Order placed successfully: {order}")
    print("\n")
except Exception as e:
    print(f"Error placing order: {e}")
    print("\n")


