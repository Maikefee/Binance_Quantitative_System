# Binance Quantitative Backtesting Strategy System

A comprehensive quantitative backtesting system for Binance cryptocurrency trading, featuring interactive web interface, multiple technical indicators, and advanced risk management tools.

## 🚀 Features

- **🪙 Multi-Currency Support**: All Binance USDT trading pairs
- **📅 Flexible Time Range**: Customizable backtesting periods
- **📊 Technical Indicators**: RSI, KDJ, Bollinger Bands, EMA, SMA, MACD, Stochastic, ATR
- **⚙️ Customizable Parameters**: Adjustable indicator parameters
- **💰 Risk Management**: Take profit and stop loss functionality
- **📈 Interactive Charts**: Real-time visualization with Plotly
- **📋 Trade Records**: Detailed transaction history and export
- **🎯 Performance Metrics**: Comprehensive performance analysis

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd TestPro1
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python run.py
# or
streamlit run app.py
```

4. **Access the web interface**
Open your browser and navigate to `http://localhost:8501`

## 📊 Supported Technical Indicators

- **RSI**: Relative Strength Index for overbought/oversold signals
- **KDJ**: Stochastic oscillator for buy/sell signals (based on ta library)
- **Bollinger Bands**: Price volatility range analysis
- **EMA**: Exponential Moving Average for trend analysis
- **SMA**: Simple Moving Average
- **MACD**: Moving Average Convergence Divergence
- **Stochastic**: Stochastic oscillator
- **ATR**: Average True Range

## 🎯 Risk Management Features

- **Take Profit**: Automatically close positions when profit target is reached
- **Stop Loss**: Automatically close positions when loss limit is reached
- **Performance Tracking**: Monitor take profit and stop loss effectiveness
- **Risk Metrics**: Maximum drawdown, Sharpe ratio, win rate analysis

## 📁 Project Structure

```
TestPro1/
├── app.py              # Main Streamlit application
├── data_fetcher.py     # Binance data retrieval module
├── indicators.py       # Technical indicator calculations
├── backtest_engine.py  # Backtesting engine with risk management
├── chart_utils.py      # Chart visualization tools
├── config.py           # Configuration settings
├── run.py              # Application launcher
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

## 🔧 Usage

1. **Select Trading Pair**: Choose from available Binance USDT pairs
2. **Set Time Range**: Define backtesting start and end dates
3. **Choose Timeframe**: Select K-line intervals (1m to 1d)
4. **Configure Parameters**: Set initial capital, commission, and risk management
5. **Select Indicators**: Choose and configure technical indicators
6. **Run Backtest**: Execute the analysis and view results
7. **Analyze Results**: Review performance metrics and charts

## 📈 Performance Metrics

- Total Return and Annualized Return
- Maximum Drawdown Analysis
- Sharpe Ratio Calculation
- Win Rate Statistics
- Take Profit/Stop Loss Effectiveness
- Trade Record Export

## 🎨 Screenshots

### Main Interface
The system provides an intuitive web interface for configuring and running backtests.

### Technical Analysis
Interactive charts showing price data with technical indicators overlay.

### Performance Dashboard
Comprehensive performance metrics and risk analysis.

## ⚠️ Disclaimer

- This system is for educational and research purposes only
- Historical performance does not guarantee future returns
- Please adjust parameters based on actual market conditions
- Thorough testing is recommended before live trading

## 🔧 Technical Requirements

- Python 3.7+
- Streamlit
- CCXT (for Binance API)
- Pandas, NumPy
- Plotly (for charts)
- TA-Lib (for technical indicators)

## 📞 Support

For questions or issues, please open an issue in the repository.

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 Documentation

For detailed documentation, please refer to the inline comments in the source code and the configuration file.

---

## 🚀 Professional Automated Trading Strategy

### 📈 Live Trading Performance

**Our automated trading strategy is incredibly simple yet effective:**
- Continuously monitors 50+ cryptocurrencies
- Automatically executes trades when signals are detected

**Performance Results:**
- 📈 **3-day return: 133%**
- 📈 **8-day return: 242%** 
- 🔥 **Best run: 553% in 17 days**

### 📱 Contact Information

- **Telegram**: https://t.me/whogotbtc
- **Telegram Group**: https://t.me/shipanjiankong  
- **WeChat**: rggboom

---

**Note**: This system is designed for educational purposes. Always test thoroughly before using any trading strategy in live markets.
