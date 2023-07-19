# Mean Reversion Trading Bot

This repository contains a Python script for a mean reversion trading bot that uses the Binance API to execute trades on the Binance exchange. The bot implements a simple mean reversion strategy based on various technical indicators such as RSI, moving averages, and Bollinger Bands.

## Prerequisites

Before running the script, make sure you have the following prerequisites:

- Python 3.x installed on your machine
- `ccxt` library installed. You can install it using `pip install ccxt`
- `pandas`, `traceback`, `ta`, and `dotenv` libraries installed. You can install them using `pip install pandas traceback ta dotenv`

## Getting Started

1. Clone this repository to your local machine or download the code as a ZIP file.
2. Install the required libraries as mentioned in the Prerequisites section.
3. Create an account on Binance and obtain your API key and secret.
4. Rename the `config.env.example` file to `config.env`.
5. Open the `config.env` file and replace `YOUR_API_KEY` with your actual Binance API key and `YOUR_API_SECRET` with your actual Binance API secret.
6. Open a terminal or command prompt and navigate to the directory where you cloned or downloaded the code.
7. Run the script using the command `python filename.py`, where `filename.py` is the name of the Python script.

## Customization

You can customize the bot's behavior by modifying the following variables in the script:

- `symbol`: The trading pair symbol (e.g., 'BNB/USDT').
- `volume_threshold`: The volume threshold for executing trades.
- `min_data_length`: The minimum number of data points required before starting the analysis.
- `order_timeout`: The duration to wait for orders to be filled before considering them as timed out.

You can also modify the trading strategy by adjusting the conditions in the `mean_reversion_strategy` function.

## Data Collection

The bot establishes a WebSocket connection with Binance to stream the latest market data, ensuring real-time updates for accurate analysis. The collected data is then stored in a CSV file named data.csv, allowing for further analysis, backtesting, and performance evaluation.

## Error Handling

The bot incorporates error handling to handle network errors, exchange errors, and insufficient funds. Any errors encountered during the execution of the bot will be logged in the console output.

## Disclaimer

Please note that this trading bot is provided for educational purposes only. Trading cryptocurrencies involves risk, and past performance is not indicative of future results. Use this bot at your own risk.

## Contributions

Contributions to improve the functionality or fix issues with the trading bot are welcome. If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code for personal or commercial purposes.

If you use this work, please cite:
- Repository
- Author: guldo111

## References

- [ccxt library](https://github.com/ccxt/ccxt)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/spot/en/)
- [pandas library](https://pandas.pydata.org/)
- [ta library](https://github.com/bukosabino/ta)
- [dotenv library](https://github.com/theskumar/python-dotenv)
