import ccxt.pro as ccxt
import os
from dotenv import load_dotenv
import pandas as pd
import traceback
import ta
import datetime
import asyncio
from ccxt import NetworkError, ExchangeError, InsufficientFunds
import time




async def mean_reversion_strategy(exchange, symbol,  volume_threshold, min_data_length, order_timeout):
    close_prices = []
    last_prices = []
    mean_value = 0
    strategy_data = pd.DataFrame(columns=['Timestamp', 'Symbol', 'Strategy', 'Position','RSI', 'SMA',
                                          'Upper Band', 'Middle Band', 'Lower Band', 'Last Price', 
                                          'Entry Price', 'Exit Price', 'Order Filled', 'Profit'])
   
   
    print('\rBot Started...')
    
    
    while True:
        try:

            # Load real-time data
            orderbook = await exchange.watch_order_book(symbol)
            ticker = await exchange.watch_ticker(symbol)
            trading_volume = await exchange.watch_trades(symbol)
            ohlcv = await exchange.watch_ohlcv(symbol, '1m')
            

            # Extract relevant features from the data
            bid_price = orderbook['bids'][0][0] if orderbook['bids'] else None
            bid_volume = orderbook['bids'][0][1] if orderbook['bids'] else None
            ask_price = orderbook['asks'][0][0] if orderbook['asks'] else None
            ask_volume = orderbook['asks'][0][1] if orderbook['asks'] else None
            last_price = ticker['last'] if 'last' in ticker else None
            vwap = ticker['vwap'] if 'vwap' in ticker else None
            trade_price = trading_volume[-1]['price'] if trading_volume else None
            trade_volume = trading_volume[-1]['amount'] if trading_volume else None
            total_volume = trading_volume[0]['info']['q']
            open_price = ohlcv[-1][1] if ohlcv else None
            high_price = ohlcv[-1][2] if ohlcv else None
            low_price = ohlcv[-1][3] if ohlcv else None
            close_price = ohlcv[-1][4] if ohlcv else None
            
            

            # Accumulate close prices
            #close_prices.append(close_price)
            last_prices.append(close_price)
            

            # Check if the minimum data length is reached
            if len(last_prices) >= min_data_length:
                
                print('\rSufficient data collected. Starting analysis...', end='', flush=True)
                
                # Convert close_prices to a pandas Series
                prices_series = pd.Series(last_prices)
                
                # Calculate the mean value
                mean_value = prices_series.mean()

                # Calculate additional indicators
                # Moving Averages
                sma = ta.trend.sma_indicator(prices_series, window=30)
                ema = ta.trend.ema_indicator(prices_series, window=20)
                
                # Calculate MACD
                macd = ta.trend.MACD(prices_series)
                macd_line = macd.macd()
                signal_line = macd.macd_signal()
                
                # Calculate Bollinger Bands
                bb = ta.volatility.BollingerBands(prices_series, window=20, window_dev=2)
                upper_band = bb.bollinger_hband()
                middle_band = bb.bollinger_mavg()
                lower_band = bb.bollinger_lband()

                # Calculate RSI
                rsi = ta.momentum.RSIIndicator(prices_series, window=14)
                rsi_value = rsi.rsi()

                # Get the last values of indicators
                last_sma = sma.iloc[-1]
                last_ema = ema.iloc[-1]
                last_upper_band = upper_band.iloc[-1]
                last_middle_band = middle_band.iloc[-1]
                last_lower_band = lower_band.iloc[-1]
                last_rsi_value = rsi_value.iloc[-1]
                last_macd_line = macd_line.iloc[-1]
                last_signal_line = signal_line.iloc[-1]
                
               
                
                # Check for mean reversion opportunities
                if (
                    last_price > last_sma and
                    last_rsi_value > 70 and 
                    last_price > last_middle_band and 
                    last_price < last_upper_band and
                    last_macd_line > last_signal_line and
                    last_price < last_ema
                ):
                

                    # Mean reversion strategy - Take a short position
                    entry_price = last_price + ...  # Customize the entry price as per your preference
                    profit_target = last_price - ...  # Customize the profit target as per your preference
                    position = 'Short'
                    strategy = 'Mean Reversion'
                    
                    
                    # Place limit sell order to enter short position
                    sell_order = await exchange.create_limit_sell_order(symbol, volume_threshold, entry_price)
                    print("\nShort position sell order executed. Entry price:", entry_price)
                    
                    # Place limit buy order to exit short position
                    buy_order = await exchange.create_limit_buy_order(symbol, volume_threshold, profit_target)
                    print("Short position buy order placed. Profit target:", profit_target)
                    
                   # Wait for orders to be filled or timeout
                    start_time = datetime.datetime.now()
                    while (sell_order['status'] != 'closed' or buy_order['status'] != 'closed') and datetime.datetime.now() - start_time < order_timeout:
                        await asyncio.sleep(1)
                        sell_order = await exchange.fetch_order(sell_order['id'], symbol)
                        buy_order = await exchange.fetch_order(buy_order['id'], symbol)

                    # Check if orders were filled or timed out
                    if sell_order['status'] != 'closed' or buy_order['status'] != 'closed':
                        # Orders were not filled within the timeout period
                        if sell_order['status'] == 'closed' and buy_order['status'] != 'closed':
                            
                            # Create an order to rebalance the portfolio
                            await exchange.create_market_buy_order(symbol, volume_threshold)
                            
                            # Cancel the unfilled buy order
                            await exchange.cancel_order(buy_order['id'],symbol)
                            print("Order timeout: Buy order was not filled within the specified time. Cancelled the buy order.")
                        elif sell_order['status'] != 'closed' and buy_order['status'] == 'closed':
                            
                            # Create an order to rebalance the portfolio
                            await exchange.create_market_sell_order(symbol, volume_thresold)
                            # Cancel the unfilled sell order
                            await exchange.cancel_order(sell_order['id'], symbol)
                            print("Order timeout: Sell order was not filled within the specified time. Cancelled the sell order.")
                        else:
                            # Cancel both unfilled orders
                            await exchange.cancel_order(sell_order['id'], symbol)
                            await exchange.cancel_order(buy_order['id'], symbol)
                            print("Order timeout: Orders were not filled within the specified time. Cancelled both orders.")

                    # Record the trade details if orders were filled
                    else:
                        # Calculate profit
                        exit_price = profit_target
                        profit = (entry_price - exit_price) * volume_threshold 
                        
                       # Append data to the dataframe
                        new_row = pd.DataFrame({
                            'Timestamp': pd.Timestamp.now(),
                            'Symbol': symbol,
                            'Strategy': strategy,
                            'Position': position,
                            'RSI': last_rsi_value,
                            'SMA': last_sma_70,
                            'Upper Band': last_upper_band,
                            'Middle Band': last_middle_band,
                            'Lower Band': last_lower_band,
                            'Last Price': last_price,
                            'Entry Price': entry_price,
                            'Exit Price': exit_price,
                            'Order Filled': True,
                            'Profit': profit
                        }, index=[len(strategy_data)])

                        strategy_data = pd.concat([strategy_data, new_row])

                    
                elif (
                    last_price < last_sma and
                    last_rsi_value < 30 and
                    last_price < last_middle_band and
                    last_price > last_lower_band and
                    last_macd_line < last_signal_line and
                    last_price > last_ema 
                ):
                    
                    # Mean reversion strategy - Take a long position
                    entry_price = last_price - ... # Customize the entry price as per your preference
                    profit_target = last_price + ... # Customize the profit target as per your preference
                    position = 'Long'
                    strategy = 'Mean Reversion'
                    
                    # Place limit buy order to enter short position
                    buy_order = await exchange.create_limit_buy_order(symbol, volume_threshold, entry_price)
                    print("\nLong position buy order placed. Profit target:", entry_price)
                    
                    # Place limit buy order to exit short position
                    sell_order = await exchange.create_limit_sell_order(symbol, volume_threshold, profit_target)
                    print("Long position sell order placed. Profit target:", profit_target)
                    
                    # Wait for orders to be filled or timeout
                    start_time = datetime.datetime.now()
                    while (sell_order['status'] != 'closed' or buy_order['status'] != 'closed') and datetime.datetime.now() - start_time < order_timeout:
                        await asyncio.sleep(1)
                        sell_order = await exchange.fetch_order(sell_order['id'], symbol)
                        buy_order = await exchange.fetch_order(buy_order['id'], symbol)

                    # Check if orders were filled or timed out
                    if sell_order['status'] != 'closed' or buy_order['status'] != 'closed':
                        # Orders were not filled within the timeout period
                        if buy_order['status'] == 'closed' and sell_order['status'] != 'closed':
                            
                            # Create an order to rebalance the portfolio
                            await exchange.create_market_sell_order(symbol, volume_threshold)
                            
                            # Cancel the unfilled buy order
                            await exchange.cancel_order(sell_order['id'], symbol)
                            print("Order timeout: Buy order was not filled within the specified time. Cancelled the sell order.")
                        elif buy_order['status'] != 'closed' and sell_order['status'] == 'closed':
                            
                            # Create an order to rebalance the portfolio
                            await exchange.create_market_buy_order(symbol, volume_threshold)
                            
                            # Cancel the unfilled sell order
                            await exchange.cancel_order(buy_order['id'], symbol)
                            print("Order timeout: Sell order was not filled within the specified time. Cancelled the buy order.")
                        else:
                            # Cancel both unfilled orders
                            await exchange.cancel_order(sell_order['id'], symbol)
                            await exchange.cancel_order(buy_order['id'],symbol)
                            print("Order timeout: Orders were not filled within the specified time. Cancelled both orders.")

                    # Record the trade details if orders were filled
                    else:
                        # Calculate profit
                        exit_price = profit_target
                        profit = (exit_price - entry_price) * volume_threshold 
                        
                        # Append data to the dataframe
                        new_row = pd.DataFrame({
                            'Timestamp': pd.Timestamp.now(),
                            'Symbol': symbol,
                            'Strategy': strategy,
                            'Position': position,
                            'RSI': last_rsi_value,
                            'SMA': last_sma_70,
                            'Upper Band': last_upper_band,
                            'Middle Band': last_middle_band,
                            'Lower Band': last_lower_band,
                            'Last Price': last_price,
                            'Entry Price': entry_price,
                            'Exit Price': exit_price,
                            'Order Filled': True,
                            'Profit': profit
                        }, index=[len(strategy_data)])

                        strategy_data = pd.concat([strategy_data, new_row])

                
                    
                if len(last_prices) > min_data_length:
                    last_prices.pop(0)
            # Save strategy_data DataFrame to a CSV file
            strategy_data.to_csv('data.csv', mode='a', header=False, index=False)   
            
        except NetworkError as e:
            print('Bot failed due to a network error:', str(e))
            continue
        except ExchangeError as e:
            print('Bot failed due to exchange error:', str(e))
            continue
        except InsufficientFunds as e:
            print('Bot failed due to insufficient funds:', str(e))
            print('Waiting for 1 hour before retrying...')
            time.sleep(3600)  # Wait for 1 hour (3600 seconds)
            print('Retrying...')
            continue
            
        except Exception as e:
            print('Bot failed with:', str(e))
            traceback.print_exc()  # Print traceback information

        
async def main():
    # Load API keys from .env file
    load_dotenv('config.env')

    api_key = os.environ.get('binance_api_key')
    api_secret = os.environ.get('binance_api_secret')
    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': api_secret, 
    })

    # Specify the symbol, thresholds, and parameters
    symbol = 'BNB/USDT'  # Symbol represents the trading pair to be used, e.g., Binance Coin (BNB) against Tether (USDT).
    
    volume_threshold = 1  # Volume threshold is the minimum trading volume required to execute a trade.
    
    min_data_length = 100  # Min data length specifies the minimum number of data points required for analysis before triggering trades.
    
    order_timeout = datetime.timedelta(minutes=60)  # Order timeout defines the duration to wait for orders to be filled before considering them as timed out. In this example, the order timeout period is set to 60 minutes.

     # Run the scalping strategy
    await mean_reversion_strategy(exchange, symbol, volume_threshold, min_data_length, order_timeout)


# Run the main function in the event loop

if __name__ == "__main__":
    asyncio.run(main())
