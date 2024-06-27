import streamlit as st
import base64
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import nltk
from datetime import datetime
from streamlit_option_menu import option_menu
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import cred
import matplotlib.pyplot as plt
import requests
import psycopg2
import plotly.graph_objs as go 
from prophet import Prophet
from prophet.plot import plot_plotly
# Function to insert a new post into the PostgreSQL database
def insert_post(username, post_text):
    conn = psycopg2.connect(
        database="st_db",
        user="postgres",
        password="password",
        host="localhost"  # or your database host
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO user_posts (username, post_text) VALUES (%s, %s)", (username, post_text))
    conn.commit()
    cur.close()
    conn.close()

# Function to retrieve all posts from the database
def get_all_posts():
    conn = psycopg2.connect(
        database="st_db",
        user="postgres",
        password="password",
        host="localhost"  # or your database host
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_posts ORDER BY post_date DESC")
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return posts
# Function to delete a post from the database
def delete_post(post_id):
    conn = psycopg2.connect(
        database="st_db",
        user="postgres",
        password="password",
        host="localhost"  # or your database host
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM user_posts WHERE id = %s", (post_id,))
    conn.commit()
    cur.close()
    conn.close()

# Function to render HTML file content
def render_html(file_path):
    with open(file_path, 'r') as html_file:
        html_content = html_file.read()
    encoded_html = base64.b64encode(html_content.encode()).decode()
    html_iframe = f'''
    <style>
    body {{
        margin: 0;
        padding: 0;
        overflow: hidden;
    }}
    iframe {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
    }}
    </style>
    <iframe src="data:text/html;base64,{encoded_html}"></iframe>
    '''
    return html_iframe

# Establish a connection to your PostgreSQL database
conn = psycopg2.connect(
    database="st_db",
    user="postgres",
    password=cred.dbpass,
    host="localhost"  # or your database host
)

# Create a cursor object using the connection
cur = conn.cursor()

# Create a table for storing user posts if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS user_posts (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50),
        post_text TEXT,
        post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

# Commit the transaction and close the connection
conn.commit()
cur.close()
conn.close()

st.set_page_config(layout="wide")

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "About", "News", "Stock Analysis", "MonteCarlo Simulations","Financial Analysis", "Community Forum"]
    )

if selected == "Home":
    st.markdown(render_html('index.html'), unsafe_allow_html=True)
elif selected == "About":
    st.markdown(render_html('about.html'), unsafe_allow_html=True)
elif selected == "News":
    st.title('Stock Dashboard')
    st.write("Welcome to our Stock Dashboard, your comprehensive platform for tracking and analyzing stocks. Stay updated with real-time stock prices, financial data, and insightful charts to make informed investment decisions")

    def display_image_and_text(title, link, text):
        col1, col2 = st.columns([2, 3])
        with col1:
            st.image(link, use_column_width=True)
        with col2:
            st.subheader(title)
            st.write(text)

    headers = {
        "X-RapidAPI-Key": cred.token,
        "X-RapidAPI-Host": "seeking-alpha.p.rapidapi.com"
    }

    url = "https://seeking-alpha.p.rapidapi.com/news/v2/list-trending"
    querystring = {"size":"20"}

    response = requests.get(url, headers=headers, params=querystring)
    trend_json = response.json()
    link_json = trend_json['data']
    
    st.header("Live Updates from the Markets")
    st.write("\n")
    
    for img in link_json[:5]:  # Display only the first 5 news items
        display_image_and_text(img['attributes']['title'], img['links']['uriImage'], img['links']['self'])
        st.write("\n")

elif selected == "Stock Analysis":
    default_date = datetime(2022, 6, 22)
    ticker = st.sidebar.text_input('Ticker', value="AAPL")
    start_date = st.sidebar.date_input('Start Date', value=default_date)
    end_date = st.sidebar.date_input('End Date')
    tickerData = yf.Ticker(ticker)
    website = tickerData.info['website']

    url = "https://seeking-alpha.p.rapidapi.com/symbols/get-summary"
    querystring = {"symbols":ticker}

    headers = {
        "X-RapidAPI-Key": cred.token1,
        "X-RapidAPI-Host": "seeking-alpha.p.rapidapi.com"
    }

    alpha_response = requests.get(url, headers=headers, params=querystring)
    alpha_json = alpha_response.json()
    info_alpha = alpha_json['data']

    for ap in info_alpha:
        st.subheader(ap['id'])
        st.write("Financials")
        st.write("PE Ratio:", ap['attributes']['peRatioFwd'])
        st.write("52 Week High:", ap['attributes']['high52'])
        st.write("52 Week Low:", ap['attributes']['low52'])

    data = yf.download(ticker, start=start_date, end=end_date)
    fig = px.line(data, x=data.index, y=data['Adj Close'])
    st.plotly_chart(fig)



    st.title('Forecasting')
    n_years = st.slider("Years of prediction:", 1, 5)
    period = n_years * 365

    def load_data(ticker):
        data = yf.download(ticker, start=start_date, end=end_date)
        data.reset_index(inplace=True)
        return data

    data = load_data(ticker)

    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
        
    plot_raw_data()

    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    symbol = ticker
    start_d = "2022-01-01"
    end_d = datetime.now().strftime("%Y-%m-%d")
    stock_data = yf.download(ticker,start=start_d,end=end_d)
    closing_price = stock_data['Close'][0]
    st.write("\n")
    st.header("News Stand")
    url = "https://mboum-finance.p.rapidapi.com/ne/news/"
    querystring = {"symbol":ticker}

    url = "https://mboum-finance.p.rapidapi.com/v2/markets/news"
    querystring = {"tickers":"AAPL","type":"ALL"}

    headers = {
        "x-rapidapi-key": cred.token2,
        "x-rapidapi-host": "mboum-finance.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data_json = response.json()
    info_json = data_json['body']

    count = 0
    for news in info_json:
        if(count<3):
            st.subheader(news['title'])
            # st.write(news['pubDate'])
            # st.write(news['description'])
            # st.write(news['link'])
            st.image(news['img'])
        count = count + 1

elif selected == "MonteCarlo Simulations":
    st.title('Monte Carlo Simulation')
    
    # Sidebar inputs
    ticker = st.sidebar.text_input('Stock', value="AAPL")
    volatility = st.sidebar.slider('Volatility', min_value=0.05, max_value=0.5, value=0.2, step=0.01)
    timesteps = st.sidebar.slider('Days (Timesteps)', min_value=10, max_value=100, value=30, step=10)

    # Download stock data
    start_date = "2022-01-01"
    end_date = datetime.now().strftime("%Y-%m-%d")
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    if stock_data.empty:
        st.error("Error: No data found for the provided ticker symbol.")
    else:
        # Calculate simulation paths
        starting_price = stock_data['Close'][0]
        max_simulation = 100

        simulations = np.zeros((max_simulation, timesteps+1))
        for i in range(max_simulation):
            random_walk = np.random.normal(0, volatility, timesteps)
            price_path = starting_price * np.exp(np.cumsum(random_walk))
            simulations[i, :] = np.insert(price_path, 0, starting_price)

        # Prepare data for Plotly Express
        simulation_columns = [f'Simulation {i}' for i in range(max_simulation)]
        df_simulations = pd.DataFrame(simulations.T, columns=simulation_columns)
        df_simulations['Day'] = range(timesteps + 1)

        # Convert columns to numeric if necessary
        df_simulations = df_simulations.apply(pd.to_numeric, errors='ignore')

        # Plotting with Plotly Express
        st.subheader('Interactive Chart')
        fig = px.line(df_simulations, x='Day', y=df_simulations.columns[:-1],
                      title='Interactive Monte Carlo Simulation',
                      labels={'value': 'Price', 'Day': 'Day'})
        fig.update_layout(height=500, width=800)
        st.plotly_chart(fig)

        # Additional plots or analysis here
        st.subheader('Additional Visualizations')

        # Histogram of final prices
        final_prices = df_simulations.iloc[-1, :-1]
        fig_hist = px.histogram(x=final_prices, nbins=30, title='Histogram of Final Prices')
        st.plotly_chart(fig_hist)


elif selected == "Financial Analysis":
    st.title('Financial Analysis')

    # Sidebar inputs
    ticker = st.sidebar.text_input('Stock', value="AAPL")
    start_date = st.sidebar.date_input('Start Date', value=datetime(2022, 1, 1))
    end_date = st.sidebar.date_input('End Date', value=datetime.now())

    # Download stock data
    tickerData = yf.Ticker(ticker)
    website = tickerData.info['website']
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    if stock_data.empty:
        st.error("Error: No data found for the provided ticker symbol.")
    else:
        # Basic stock information
        st.subheader('Basic Stock Information')
        st.write(f"Company Name: {tickerData.info['longName']}")
        st.write(f"Website: {website}")

        # Price chart
        st.subheader('Historical Stock Price')
        fig_price = px.line(stock_data, x=stock_data.index, y=stock_data['Close'], title='Historical Stock Price')
        st.plotly_chart(fig_price)

        # Financial metrics
        st.subheader('Financial Metrics')
        st.write("PE Ratio:", tickerData.info['forwardPE'])
        st.write("Market Cap:", tickerData.info['marketCap'])
        st.write("Book Value:", tickerData.info['bookValue'])

        # Dividends
        st.subheader('Dividends')
        dividends = tickerData.dividends
        if not dividends.empty:
            fig_dividends = px.line(dividends, x=dividends.index, y=dividends.values, title='Dividend History')
            st.plotly_chart(fig_dividends)
        else:
            st.write("No dividend data available for this stock.")

        # Technical analysis indicators (example: Moving Average)
        st.subheader('Technical Indicators')
        short_window = st.sidebar.slider('Short-term Moving Average Window', min_value=5, max_value=50, value=20, step=5)
        long_window = st.sidebar.slider('Long-term Moving Average Window', min_value=50, max_value=200, value=100, step=10)

        # Calculate moving averages
        stock_data['Short_Moving_Avg'] = stock_data['Close'].rolling(window=short_window).mean()
        stock_data['Long_Moving_Avg'] = stock_data['Close'].rolling(window=long_window).mean()

        # Plot moving averages
        fig_ma = go.Figure()
        fig_ma.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price'))
        fig_ma.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Short_Moving_Avg'], mode='lines', name=f'{short_window} Days Moving Avg'))
        fig_ma.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Long_Moving_Avg'], mode='lines', name=f'{long_window} Days Moving Avg'))
        fig_ma.update_layout(title='Moving Average Analysis', xaxis_title='Date', yaxis_title='Price')
        st.plotly_chart(fig_ma)

        # Additional financial analysis sections can be added as per your requirements

elif selected == "Community Forum":
    st.title('Community Forum')

    # Sidebar for posting
    st.sidebar.subheader('New Post')
    username = st.sidebar.text_input('Your Name', value='Anonymous')
    post_text = st.sidebar.text_area('Write your post here', height=150)
    if st.sidebar.button('Post'):
        if post_text:
            insert_post(username, post_text)
            st.sidebar.success('Post added successfully!')

    # Display all posts
    st.header('Recent Posts')
    posts = get_all_posts()
    for post in posts:
        post_id = post[0]  # Assuming the first column is the id
        st.subheader(post[1] + ' - ' + post[3].strftime("%Y-%m-%d %H:%M:%S"))
        st.write(post[2])
        
        # Add delete button for each post
        if st.button(f"Delete {post_id}"):
            delete_post(post_id)
            st.info("Post deleted successfully!")
            # Optionally, you may want to refresh the page or update posts list after deletion

        st.markdown('---')
