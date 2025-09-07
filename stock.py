import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import io

# Set the page configuration for the Streamlit app
st.set_page_config(layout="wide", page_title="Indian Stock Market Analyzer")

st.title("Indian Stock Market Analyzer 📈")
st.write("This tool analyzes Nifty 50 stocks to identify top performers based on common investment strategies. Select a strategy and click 'Run Analysis' to begin.")

@st.cache_data(ttl=3600) # Cache the data for 1 hour to avoid re-downloading
def get_nifty50_symbols():
    """
    Fetches the list of Nifty 50 stock symbols from the NSE India website.
    Includes a fallback list in case the download fails.
    """
    try:
        url = "https://archives.nseindia.com/content/indices/ind_nifty50list.csv"
        # Use a user-agent to avoid being blocked
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
        csv_file = io.StringIO(response.text)
        nifty50_df = pd.read_csv(csv_file)
        symbols = nifty50_df['Symbol'].tolist()
        # Append '.NS' for compatibility with yfinance
        return [symbol + ".NS" for symbol in symbols]
    except Exception as e:
        st.error(f"Could not download Nifty 50 list from NSE. Using a default list. Error: {e}")
        # Fallback list of major Nifty 50 stocks
        return [
            'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS', 
            'HINDUNILVR.NS', 'BHARTIARTL.NS', 'ITC.NS', 'SBIN.NS', 'LICI.NS',
            'BAJFINANCE.NS', 'HCLTECH.NS', 'KOTAKBANK.NS', 'MARUTI.NS', 'ASIANPAINT.NS'
        ]

def calculate_technical_indicators(df):
    """Calculates technical indicators like SMA and RSI."""
    if df.empty:
        return df
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    
    # Calculate RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

@st.cache_data(ttl=600) # Cache each stock's data for 10 minutes
def get_stock_data(symbol):
    """
    Fetches fundamental and technical data for a given stock symbol.
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Fetch historical data for technical analysis
        hist = stock.history(period="1y")
        if hist.empty:
            return None, None

        # Calculate technical indicators
        hist_with_indicators = calculate_technical_indicators(hist)
        
        # Prepare a dictionary with relevant data
        data = {
            'Symbol': symbol.replace('.NS', ''),
            'Company Name': info.get('longName', 'N/A'),
            'Current Price': info.get('currentPrice', 0),
            'P/E Ratio': info.get('trailingPE', None),
            'P/B Ratio': info.get('priceToBook', None),
            'Debt to Equity': info.get('debtToEquity', None),
            'ROE': info.get('returnOnEquity', None),
            'Revenue Growth': info.get('revenueGrowth', None),
            '52 Week High': info.get('fiftyTwoWeekHigh', 0),
            '52 Week Low': info.get('fiftyTwoWeekLow', 0),
            'Market Cap': info.get('marketCap', 0),
            'SMA_50': hist_with_indicators['SMA_50'].iloc[-1] if not hist_with_indicators.empty else None,
            'SMA_200': hist_with_indicators['SMA_200'].iloc[-1] if not hist_with_indicators.empty else None,
            'RSI': hist_with_indicators['RSI'].iloc[-1] if not hist_with_indicators.empty else None,
        }
        return data, hist_with_indicators
    except Exception:
        # Return None if there's any issue fetching data for a symbol
        return None, None

# --- UI Elements ---
st.sidebar.header("Analysis Controls")
analysis_strategy = st.sidebar.selectbox(
    "Choose an Analysis Strategy",
    ["Quality Investing", "Growth Investing", "Value Investing", "Technical Momentum"]
)

# --- Strategy-specific controls ---
if analysis_strategy == "Quality Investing":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Quality Investing Criteria")
    max_debt_equity = st.sidebar.slider("Maximum Debt to Equity Ratio", 0.0, 5.0, 1.5, 0.1)
    min_roe_pct = st.sidebar.slider("Minimum Return on Equity (ROE %)", 0, 50, 12, 1)

run_button = st.sidebar.button("Run Analysis")

# --- Initialize Session State ---
if 'analysis_run' not in st.session_state:
    st.session_state.analysis_run = False
    st.session_state.results = None
    st.session_state.quality_params = {}


# --- Analysis Logic ---
if run_button:
    symbols = get_nifty50_symbols()
    all_stock_data = []
    
    progress_bar = st.progress(0, text="Fetching data for Nifty 50 stocks...")

    for i, symbol in enumerate(symbols):
        data, _ = get_stock_data(symbol)
        if data:
            all_stock_data.append(data)
        progress_bar.progress((i + 1) / len(symbols), text=f"Analyzing {symbol}...")
    
    progress_bar.empty()

    if not all_stock_data:
        st.error("Could not fetch data for any stocks. Please try again later.")
        st.session_state.analysis_run = False
    else:
        df = pd.DataFrame(all_stock_data)
        # Clean up data for analysis
        numeric_cols = ['Current Price', 'P/E Ratio', 'P/B Ratio', 'Debt to Equity', 'ROE', 'Revenue Growth', 'Market Cap', 'SMA_50', 'SMA_200', 'RSI']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Store results in session state to persist across reruns
        st.session_state.results = df
        st.session_state.analysis_run = True
        st.session_state.strategy = analysis_strategy 
        if analysis_strategy == "Quality Investing":
            st.session_state.quality_params = {'max_de': max_debt_equity, 'min_roe': min_roe_pct / 100.0}


# --- Display Logic (runs if analysis has been performed) ---
if st.session_state.analysis_run and st.session_state.results is not None:
    df = st.session_state.results
    strategy = st.session_state.strategy
    
    st.subheader(f"Top Stocks based on {strategy} Strategy")

    # --- NEW: Expander to show raw data for debugging filters ---
    with st.expander("View Raw Data for Filtering"):
        st.info("Use this table to see the actual data and set realistic filter criteria in the sidebar.")
        if strategy == "Quality Investing":
            st.dataframe(df[['Symbol', 'Debt to Equity', 'ROE']].sort_values(by='ROE', ascending=False))
        elif strategy == "Growth Investing":
            st.dataframe(df[['Symbol', 'Revenue Growth']].sort_values(by='Revenue Growth', ascending=False))
        elif strategy == "Value Investing":
            st.dataframe(df[['Symbol', 'P/E Ratio', 'P/B Ratio']].sort_values(by='P/E Ratio', ascending=True))
        else:
            st.dataframe(df[['Symbol', 'Current Price', 'SMA_50', 'SMA_200', 'RSI']].sort_values(by='RSI', ascending=False))


    # --- Apply selected strategy for filtering and sorting ---
    if strategy == "Quality Investing":
        params = st.session_state.quality_params
        st.info(f"""
        **Quality Investing:** Focuses on financially healthy companies with strong, stable performance.
        - **Your Criteria:** Debt to Equity < {params['max_de']} and Return on Equity > {params['min_roe']*100:.0f}%.
        - **Sorted by:** Return on Equity (descending).
        """)
        # Added a check to ensure the required columns exist and are not all null
        if 'Debt to Equity' in df.columns and 'ROE' in df.columns:
            filtered_df = df[
                (df['Debt to Equity'].notna()) & (df['ROE'].notna()) &
                (df['Debt to Equity'] < params['max_de']) & 
                (df['ROE'] > params['min_roe'])
            ].copy()
            sorted_df = filtered_df.sort_values(by="ROE", ascending=False)
        else:
            sorted_df = pd.DataFrame() # Create empty dataframe if columns are missing
        
        display_cols = ['Symbol', 'Company Name', 'Current Price', 'ROE', 'Debt to Equity', 'P/E Ratio', 'Market Cap']

    elif strategy == "Growth Investing":
        st.info("""
        **Growth Investing:** Focuses on companies with strong growth in revenue and earnings.
        - **Criteria:** Revenue Growth > 15%.
        - **Sorted by:** Revenue Growth (descending).
        """)
        filtered_df = df[df['Revenue Growth'] > 0.15].copy()
        sorted_df = filtered_df.sort_values(by="Revenue Growth", ascending=False)
        display_cols = ['Symbol', 'Company Name', 'Current Price', 'Revenue Growth', 'P/E Ratio', 'Market Cap']
    
    elif strategy == "Value Investing":
        st.info("""
        **Value Investing:** Focuses on finding undervalued stocks trading below their intrinsic value.
        - **Criteria:** P/E Ratio < 25, P/B Ratio < 3.
        - **Sorted by:** P/E Ratio (ascending - lower is better).
        """)
        filtered_df = df[(df['P/E Ratio'] < 25) & (df['P/E Ratio'] > 0) & (df['P/B Ratio'] < 3) & (df['P/B Ratio'] > 0)].copy()
        sorted_df = filtered_df.sort_values(by="P/E Ratio", ascending=True)
        display_cols = ['Symbol', 'Company Name', 'Current Price', 'P/E Ratio', 'P/B Ratio', 'Debt to Equity', 'Market Cap']

    elif strategy == "Technical Momentum":
        st.info("""
        **Technical Momentum:** Focuses on stocks that are in a strong uptrend.
        - **Criteria:** Current Price > 50-Day SMA, 50-Day SMA > 200-Day SMA, RSI < 75 (to avoid extremely overbought).
        - **Sorted by:** RSI (descending - higher indicates stronger momentum).
        """)
        filtered_df = df[
            (df['Current Price'] > df['SMA_50']) & 
            (df['SMA_50'] > df['SMA_200']) & 
            (df['RSI'] < 75)
        ].copy()
        sorted_df = filtered_df.sort_values(by="RSI", ascending=False)
        display_cols = ['Symbol', 'Company Name', 'Current Price', 'RSI', 'SMA_50', 'SMA_200']

    # --- Display Results ---
    if sorted_df.empty:
        st.warning("No stocks met the criteria for this strategy from the Nifty 50 list. Please try relaxing your criteria.")
    else:
        # Format numbers for better readability
        display_df = sorted_df.copy()
        display_df['Market Cap'] = display_df['Market Cap'].apply(lambda x: f"₹{x/1e7:,.2f} Cr" if pd.notnull(x) else 'N/A')
        for col in ['ROE', 'Revenue Growth']:
             if col in display_df.columns:
                display_df[col] = display_df[col].apply(lambda x: f"{x*100:.2f}%" if pd.notnull(x) else 'N/A')
        
        st.dataframe(display_df[display_cols].reset_index(drop=True).head(15))

        # --- Detailed View Expander ---
        st.subheader("Detailed Stock View")
        selected_stock_symbol = st.selectbox(
            "Select a stock from the results to view details", 
            options=sorted_df['Symbol'].tolist()
        )

        if selected_stock_symbol:
            full_symbol = selected_stock_symbol + ".NS"
            data, hist = get_stock_data(full_symbol)
            
            if data and not hist.empty:
                st.write(f"### {data['Company Name']} ({data['Symbol']})")
                
                # Display charts in columns
                col1, col2 = st.columns(2)
                with col1:
                    st.write("#### Price Chart with Moving Averages")
                    st.line_chart(hist[['Close', 'SMA_50', 'SMA_200']])
                with col2:
                    st.write("#### RSI (14-Day)")
                    st.line_chart(hist['RSI'])
                    st.write("#### Volume")
                    st.bar_chart(hist['Volume'])

