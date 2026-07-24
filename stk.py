import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

class StockMarketAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Market Analysis System")
        self.geometry("900x600")
        self.configure(bg="#1e1e2f")

        self.style = ttk.Style(self)
        try:
            self.style.theme_use('clam')
        except:
            pass
        self.style.configure('TButton', background="#5a5aaf", foreground="white", font=('Helvetica', 11, 'bold'))
        self.style.map('TButton', background=[('active', '#35357d')])
        self.style.configure('TLabel', background="#1e1e2f", foreground="white", font=('Helvetica', 12))
        self.style.configure('TEntry', foreground="#333", font=('Helvetica', 11))

        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Stock Market Analysis System", font=('Helvetica', 20, 'bold'), background="#1e1e2f", foreground="#a6a6ff")
        self.title_label.pack(pady=20)

        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10, fill='x', padx=20)

        ttk.Label(input_frame, text="Enter Stock Ticker (e.g. AAPL, MSFT): ").pack(side='left', padx=(0, 10))

        self.ticker_entry = ttk.Entry(input_frame, width=15)
        self.ticker_entry.insert(0, "AAPL")  # Default value
        self.ticker_entry.pack(side='left', padx=(0, 20))
        self.ticker_entry.focus()

        self.fetch_button = ttk.Button(input_frame, text="Fetch Data", command=self.fetch_data)
        self.fetch_button.pack(side='left')

        self.results_frame = ttk.Frame(self)
        self.results_frame.pack(pady=20, fill='both', expand=True, padx=20)

        self.figure, self.ax = plt.subplots(figsize=(9, 4), dpi=100)
        plt.style.use('ggplot')
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.results_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.info_label = ttk.Label(self, text="", font=('Helvetica', 12, 'italic'), background="#1e1e2f", foreground="#b0b0ff")
        self.info_label.pack(pady=10)

    def fetch_data(self):
        ticker = self.ticker_entry.get().strip().upper()
        if not ticker:
            messagebox.showerror("Input Error", "Please enter a valid stock ticker symbol.")
            return

        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=180)
            stock_data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)

            if stock_data.empty:
                messagebox.showerror("Data Error", f"No data found for ticker '{ticker}'. Please check the ticker and try again.")
                return

            stock_data['SMA20'] = stock_data['Close'].rolling(window=20).mean()
            stock_data['SMA50'] = stock_data['Close'].rolling(window=50).mean()

            self.plot_data(ticker, stock_data)
            self.show_info(stock_data)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")

    def plot_data(self, ticker, data):
        self.ax.clear()
        self.ax.set_facecolor('#1e1e2f')
        self.figure.patch.set_facecolor('#1e1e2f')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')

        self.ax.plot(data.index, data['Close'], label='Close Price', color='#66c2a5', linewidth=2)
        self.ax.plot(data.index, data['SMA20'], label='20-day SMA', color='#fc8d62', linewidth=1.8)
        self.ax.plot(data.index, data['SMA50'], label='50-day SMA', color='#8da0cb', linewidth=1.8)

        self.ax.set_title(f"{ticker} - Last 6 Months", fontsize=14, color='white', fontweight='bold')
        self.ax.set_xlabel("Date", color='white')
        self.ax.set_ylabel("Price (USD)", color='white')

        legend = self.ax.legend(facecolor='#2e2e42')
        for text in legend.get_texts():
            text.set_color('white')

        self.ax.xaxis.set_major_locator(mdates.MonthLocator())
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        self.figure.autofmt_xdate()

        self.canvas.draw()

    def show_info(self, data):
        latest_close = float(data['Close'].iloc[-1])
        sma20 = float(data['SMA20'].iloc[-1])
        sma50 = float(data['SMA50'].iloc[-1])
        summary_text = (f"Latest Closing Price: ${latest_close:.2f}    |    "
                        f"20-day SMA: ${sma20:.2f}    |    50-day SMA: ${sma50:.2f}")
        self.info_label.config(text=summary_text)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

if __name__ == "__main__":
    app = StockMarketAnalyzer()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
