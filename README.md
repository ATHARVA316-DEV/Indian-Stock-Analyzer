# Indian Stock Market Analyzer 📈

A powerful Streamlit web application that analyzes Nifty 50 stocks to identify top performers based on popular investment strategies. This tool provides real-time data analysis, technical indicators, and strategic stock filtering to help make informed investment decisions.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

- **Real-time Nifty 50 Data**: Automatically fetches current Nifty 50 stock list from NSE
- **Multiple Investment Strategies**: 
  - Quality Investing
  - Growth Investing  
  - Value Investing
  - Technical Momentum
- **Technical Indicators**: SMA (50, 200), RSI, Price Analysis
- **Interactive Charts**: Price charts with moving averages, RSI indicators, and volume analysis
- **Customizable Filters**: Adjust criteria based on your investment preferences
- **Detailed Stock Analysis**: Deep dive into individual stock performance
- **Data Caching**: Optimized performance with smart caching mechanisms

## 🚀 Live Demo

To run the application locally, follow the installation instructions below.

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- Internet connection for real-time data fetching

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ATHARVA316-DEV/Indian-Stock-Analyzer.git
   cd Indian-Stock-Analyzer
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install streamlit pandas yfinance requests
   ```

4. **Run the application**
   ```bash
   streamlit run stock.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - The application will automatically open in your default browser

## 📋 Requirements

Create a `requirements.txt` file with the following dependencies:

```txt
streamlit>=1.28.0
pandas>=1.3.0
yfinance>=0.2.18
requests>=2.25.0
```

## 🔧 Usage Guide

### 1. Strategy Selection

Choose from four investment strategies in the sidebar:

#### **Quality Investing** 🏛️
- **Focus**: Financially healthy companies with stable performance
- **Customizable Parameters**:
  - Maximum Debt to Equity Ratio (default: 1.5)
  - Minimum Return on Equity (default: 12%)
- **Sorting**: By ROE (descending)

#### **Growth Investing** 🚀
- **Focus**: Companies with strong revenue and earnings growth
- **Criteria**: Revenue Growth > 15%
- **Sorting**: By Revenue Growth (descending)

#### **Value Investing** 💰
- **Focus**: Undervalued stocks trading below intrinsic value
- **Criteria**: P/E Ratio < 25, P/B Ratio < 3
- **Sorting**: By P/E Ratio (ascending)

#### **Technical Momentum** 📊
- **Focus**: Stocks in strong uptrend
- **Criteria**: 
  - Current Price > 50-Day SMA
  - 50-Day SMA > 200-Day SMA
  - RSI < 75 (avoid overbought)
- **Sorting**: By RSI (descending)

### 2. Running Analysis

1. Select your preferred strategy from the sidebar
2. Adjust strategy-specific parameters (if available)
3. Click **"Run Analysis"** button
4. Wait for the progress bar to complete data fetching

### 3. Viewing Results

- **Top Stocks Table**: Shows up to 15 stocks meeting your criteria
- **Raw Data Expander**: View unfiltered data for debugging filters
- **Detailed Stock View**: Select individual stocks for comprehensive analysis

### 4. Individual Stock Analysis

- **Price Charts**: Interactive charts with moving averages
- **Technical Indicators**: RSI trends and analysis
- **Volume Analysis**: Trading volume patterns
- **Company Information**: Fundamental data and ratios

## 🏗️ Project Structure

```
Indian-Stock-Analyzer/
├── stock.py                 # Main Streamlit application
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
└── .streamlit/             # Streamlit configuration (optional)
    └── config.toml
```

## ⚙️ Key Functions

### Data Fetching
```python
@st.cache_data(ttl=3600)
def get_nifty50_symbols():
    """Fetches current Nifty 50 stock symbols from NSE"""
    
@st.cache_data(ttl=600)
def get_stock_data(symbol):
    """Fetches fundamental and technical data for stock"""
```

### Technical Analysis
```python
def calculate_technical_indicators(df):
    """Calculates SMA and RSI indicators"""
```

## 🛡️ Error Handling

The application includes robust error handling:

- **Fallback Stock List**: Uses predefined Nifty 50 list if NSE download fails
- **Data Validation**: Handles missing or invalid stock data gracefully  
- **Network Issues**: Continues analysis even if some stocks fail to load
- **User Feedback**: Clear error messages and warnings

## 🔍 Technical Details

### Data Sources
- **Stock Data**: Yahoo Finance API via `yfinance`
- **Nifty 50 List**: NSE India official archives
- **Real-time Updates**: Cached for optimal performance

### Performance Optimization
- **Caching Strategy**: 
  - Nifty 50 list cached for 1 hour
  - Individual stock data cached for 10 minutes
- **Progress Tracking**: Real-time progress bars during data fetching
- **Session State**: Persistent results across app interactions

### Technical Indicators
- **SMA (Simple Moving Average)**: 50-day and 200-day periods
- **RSI (Relative Strength Index)**: 14-day period
- **Price Analysis**: Current vs historical price comparisons

## 🎯 Investment Strategy Details

### Quality Investing Metrics
- **Return on Equity (ROE)**: Measures profitability efficiency
- **Debt to Equity**: Assesses financial leverage and risk
- **Stability Indicators**: Focus on consistent performers
- <img width="720" height="724" alt="image" src="https://github.com/user-attachments/assets/c2e6013d-364f-4e55-b6b6-ff4e2cc055b0" />


### Growth Investing Metrics  
- **Revenue Growth**: Year-over-year revenue increase
- **Market Expansion**: Companies with expanding business
- **Future Potential**: High-growth trajectory stocks
- <img width="607" height="877" alt="image" src="https://github.com/user-attachments/assets/56ff5cce-1ced-41f5-bd9d-dc909a77bbdf" />


### Value Investing Metrics
- **P/E Ratio**: Price-to-Earnings valuation metric
- **P/B Ratio**: Price-to-Book value assessment
- **Undervaluation**: Stocks trading below intrinsic value
- <img width="602" height="872" alt="image" src="https://github.com/user-attachments/assets/e6e53758-94a6-47dc-ad66-3059a20f0be8" />


### Technical Momentum Metrics
- **Moving Averages**: Trend direction indicators
- **RSI**: Momentum and overbought/oversold conditions
- **Price Action**: Current price relative to averages
- <img width="601" height="878" alt="image" src="https://github.com/user-attachments/assets/7dcac893-083a-4534-b64b-fabc43b67989" />


## 🚨 Important Disclaimers

⚠️ **Investment Risk Warning**: 
- This tool is for educational and informational purposes only
- Past performance does not guarantee future results
- Always consult with a qualified financial advisor
- Perform your own due diligence before making investment decisions
- Stock market investments carry inherent risks

## 🛠️ Customization

### Adding New Strategies

```python
elif strategy == "Your Custom Strategy":
    st.info("Description of your strategy")
    # Add your filtering logic
    filtered_df = df[your_custom_criteria].copy()
    sorted_df = filtered_df.sort_values(by="your_metric", ascending=False)
    display_cols = ['Symbol', 'Company Name', 'your_metrics']
```

### Modifying Technical Indicators

```python
def calculate_technical_indicators(df):
    # Add your custom indicators
    df['Your_Indicator'] = your_calculation_logic
    return df
```

## 🐛 Troubleshooting

### Common Issues

1. **"Could not download Nifty 50 list"**
   - **Solution**: Application will use fallback list automatically
   - **Cause**: NSE server connectivity issues

2. **"No stocks met the criteria"**
   - **Solution**: Relax filter parameters in sidebar
   - **Cause**: Too restrictive filtering criteria

3. **Slow data loading**
   - **Solution**: Wait for caching to complete on first run
   - **Cause**: Initial data fetching from multiple sources

4. **Module not found errors**
   - **Solution**: Ensure all requirements are installed: `pip install -r requirements.txt`

### Performance Tips

- **First Run**: May take 2-3 minutes to fetch all Nifty 50 data
- **Subsequent Runs**: Much faster due to caching
- **Internet Connection**: Stable connection required for real-time data
- **Browser**: Use modern browsers for best experience

## 📊 Sample Output

### Quality Investing Results
```
Top Stocks based on Quality Investing Strategy
Symbol | Company Name | Current Price | ROE | Debt to Equity | P/E Ratio | Market Cap
TCS    | Tata Consultancy Services | ₹3,245 | 42.5% | 0.12 | 24.8 | ₹11.8 Cr
INFY   | Infosys Limited | ₹1,456 | 31.2% | 0.08 | 22.1 | ₹6.2 Cr
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Add new investment strategies
   - Improve technical indicators
   - Enhance UI/UX
   - Fix bugs or optimize performance

4. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```

5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add docstrings to new functions
- Test with different market conditions
- Ensure mobile responsiveness
- Update documentation for new features

## 🗺️ Roadmap

### Version 2.0 (Upcoming)
- [ ] **Multi-timeframe Analysis**: 1D, 1W, 1M, 1Y views
- [ ] **More Technical Indicators**: MACD, Bollinger Bands, Stochastic
- [ ] **Sector Analysis**: Industry-wise performance comparison
- [ ] **Export Functionality**: CSV/Excel export of results
- [ ] **Email Alerts**: Automated stock alerts based on criteria

### Version 2.1 (Future)
- [ ] **Portfolio Tracking**: Personal portfolio management
- [ ] **Backtesting**: Historical strategy performance
- [ ] **Options Analysis**: Options chain and Greeks
- [ ] **News Integration**: Stock-specific news sentiment
- [ ] **Mobile App**: React Native mobile version

## 📈 Usage Analytics

The application tracks:
- Strategy popularity
- Most analyzed stocks  
- Performance metrics
- User engagement patterns

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ATHARVA316-DEV/Indian-Stock-Analyzer/issues)
- **Documentation**: This README and inline code comments
- **Community**: [GitHub Discussions](https://github.com/ATHARVA316-DEV/Indian-Stock-Analyzer/discussions)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Streamlit](https://streamlit.io/)**: Amazing framework for data apps
- **[yfinance](https://github.com/ranaroussi/yfinance)**: Reliable Yahoo Finance API wrapper  
- **[NSE India](https://www.nseindia.com/)**: Official Nifty 50 data source
- **[Pandas](https://pandas.pydata.org/)**: Powerful data manipulation library
- **Indian Stock Market Community**: For inspiration and feedback

---

## 🌟 Star the Repository

If you find this project helpful, please consider giving it a star ⭐ on GitHub!

---

<div align="center">

**Made by [ATHARVA316-DEV](https://github.com/ATHARVA316-DEV)**

</div>

---

**Disclaimer**: This application is for educational purposes only. Always do your own research and consult with financial advisors before making investment decisions. The stock market involves risks, and past performance does not guarantee future results.
