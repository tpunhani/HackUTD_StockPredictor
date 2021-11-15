import yfinance as yf




def fetch_data(stock):
    try:
        data, data1 = [], []
        try:
            data = yf.download(stock, start="2021-11-13", end="2021-11-14")
        except:
            pass
        try:
            data1 = yf.download(stock, start="2021-11-01", end="2021-11-02")
        except:
            pass
        if not data and data1:
            return [str(1), str(data1["Close"][0]- data1["Open"][0])]
        elif not data1 and data:
            return [str(1), str(data["Close"][0]- data["Open"][0])]
        elif not data1 and not data:
            return [str(1), str(1)]
    

        return [str(data1["Volume"][0]/data["Volume"][0]), str(data1["Close"][0] - data1["Open"][0]) - (data["Close"][0] - data["Open"][0])]
    except:
        return [str(1), str(1)]