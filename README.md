# Stock Market Analysis System

# Description

A desktop GUI application built in Python that fetches real-time financial market data and provides technical analysis visualization. The application allows users to search for any valid stock ticker to view historical closing prices along with short-term and medium-term moving average indicators over a 6-month timeline.

# Project Overview

Analyzing historical stock market trends requires clear visual metrics to identify potential momentum shifts. This project fetches financial data directly using `yfinance` and dynamically calculates technical indicators using `pandas`.

The core feature is an embedded Matplotlib canvas within a Tkinter interface, configured in dark mode for optimal data visualization. The system automatically calculates 20-day and 50-day Simple Moving Averages (SMA) to help highlight price trends, support/resistance zones, and potential crossover points.

# Tech Stack

* Language: Python 3.x
* GUI Framework: Tkinter / ttk
* Financial Data API: yfinance (Yahoo Finance API wrapper)
* Data Processing: Pandas
* Visualization Engine: Matplotlib (embedded via `FigureCanvasTkAgg`)

# Key Features

* Dynamic Market Data Fetching: Retrieves the past 6 months of historical stock prices for any valid ticker symbol (e.g., AAPL, MSFT, GOOGL).
* Moving Average Calculations: Automatically calculates 20-day (SMA20) and 50-day (SMA50) trendlines.
* Interactive Charting: Renders embedded Matplotlib plots complete with date formatting, legends, and high-contrast dark theme styling.
* Real-Time Summary Display: Displays the exact dollar values for the latest closing price and moving average metrics.
* Input Validation & Error Handling: Handles invalid ticker symbols, missing market data, and network connection issues with informative warning dialogs.
