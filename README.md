# Finance Dashboard

Welcome to the Finance Dashboard project! This dashboard provides various financial tools and insights through a user-friendly interface.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Configure Credentials](#configure-credentials)
---

## Overview

The finance dashboard project, built on Streamlit, leverages PostgreSQL for data management. It provides users with comprehensive financial insights through tools like Monte Carlo simulations for risk assessment and interactive forecasts powered by Facebook Prophet. Users can analyze stock data with historical visualizations, access real-time financial news, and utilize forecasting capabilities to make informed investment decisions.


---

## Features

### Pages Included:

- **Home**: Overview and introduction to the dashboard.
  
  ![landing page](https://github.com/PKhetan0208/Finance-Dashboard/blob/main/Images/Landing%20Page.png)
- **About**: Information about the project and its creators.
  
  ![about](https://github.com/PKhetan0208/Finance-Dashboard/blob/main/Images/About.png)
- **News**: Latest financial news and updates.
  
  ![news](https://github.com/PKhetan0208/Finance-Dashboard/blob/main/Images/News.png)
- **Stock Analysis**: Tools for analyzing stock data and trends.
  - Analyze the performance of a selected stock using historical price data.
  - Generate visualizations and insights based on the stock's historical data.
  - Access news articles related to the selected stock for comprehensive information.
  - Use interactive graphs to forecast the stock's performance over specific time periods.
  - Forecasting powered by the Facebook Prophet library for automated time series forecasting.


  ![stock1](https://github.com/PKhetan0208/Finance-Dashboard/blob/main/Images/Stock%20Analysis_1.png)
  ![stock2](https://github.com/PKhetan0208/Finance-Dashboard/blob/main/Images/Stock%20Analysis_2.png)
- **Monte Carlo Simulator**: Simulation tool for financial scenarios.
  - The dashboard's Monte Carlo prediction graph uses stock volatility data.
  - Monte Carlo simulation estimates possible investment outcomes through historical data simulations.
  - By including volatility, users gain insights into investment risk and return potential.

  ![montecarlo](https://github.com/PKhetan0208/Finance-Dashboard/blob/main/Images/MonteCarlo.png)
- **Financial Analysis**: Detailed analysis tools and visualizations.
  - Detailed information on dividends and other financial details of specific stocks.
  - Interactive moving average graph based on user-input time periods.
  - Comprehensive analysis tools and visualizations for in-depth financial insights.

  ![fin1](https://github.com/PKhetan0208/Finance-Dashboard/blob/main/Images/Financial%20Analysis_1.png)
  ![fin2](https://github.com/PKhetan0208/Finance-Dashboard/blob/main/Images/Financial%20Analysis_2.png)
- **Community Forum**: Platform for users to discuss financial topics.
  - Open portal for discussions on various financial topics.
  - Powered by a PostgreSQL database backend.
  - Features include write and delete chat capabilities for interactive discussions.

  ![forum](https://github.com/PKhetan0208/Finance-Dashboard/blob/main/Images/Community%20Forum.png)

### Technologies Used:

- **Streamlit**: Used for creating interactive web pages.
- **Python**: Programming language used for backend logic and calculations.
- **Database**: PostgreSQL for data storage and management.
- **Libraries**: 
  - `yfinance`: Used for retrieving stock market data.
  - `facebook prophet`: Utilized for automated time series forecasting.
  - APIs: `MBOUM` and `Seeking Alpha` for integrating external financial data and insights.


---

## Installation

### Prerequisites:

- Python 3.x
- `pip` (Python package installer)

### Steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/PKhetan0208/Finance-Dashboard.git
   cd Finance-Dashboard
2. **Install Dependencies**

   Install required Python libraries using pip:

   ```bash
   pip install -r requirements.txt



## Configure Credentials

To securely use API keys and database passwords, follow these steps:

### Setting Up `cred.py`

3. **Setting Up `cred.py`**:

   1. **Create `cred.py`**:
   
      Create a file named `cred.py` in the root directory of your project.
   
   2. **Add API Keys and Password**:
   
      Open `cred.py` and add the following content:
   
      ```python
      # cred.py
      
      token1 = "your_seeking_alpha_api_key"
      token2 = "your_mboum_api_key"
      dbpass = "your_postgres_database_password"
      ```
   
   Replace `"your_seeking_alpha_api_key"`, `"your_mboum_api_key"`, and `"your_postgres_database_password"` with your actual API keys and database password. This file will securely store your credentials for accessing external services.
   
   Ensure that `cred.py` is not included in version control (add it to `.gitignore`) to protect your sensitive information.



