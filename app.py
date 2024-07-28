from alpha_vantage.timeseries import TimeSeries


class StockPortfolio:
    def __init__(self, api_key):
        self.portfolio = {}
        self.api_key = api_key
        self.ts = TimeSeries(key=self.api_key, output_format='pandas')

    def add_stock(self, ticker, shares, purchase_price):
        if ticker in self.portfolio:
            self.portfolio[ticker]['shares'] += shares
            self.portfolio[ticker]['purchase_price'] = purchase_price
        else:
            self.portfolio[ticker] = {'shares': shares, 'purchase_price': purchase_price}

    def remove_stock(self, ticker, shares):
        if ticker in self.portfolio:
            if self.portfolio[ticker]['shares'] > shares:
                self.portfolio[ticker]['shares'] -= shares
            elif self.portfolio[ticker]['shares'] == shares:
                del self.portfolio[ticker]
            else:
                print("Error: Not enough shares to remove")
        else:
            print("Error: Stock not found in portfolio")

    def fetch_stock_price(self, ticker):
        data, meta_data = self.ts.get_quote_endpoint(ticker)
        return float(data['05. price'][0])

    def update_portfolio(self):
        for ticker in self.portfolio:
            self.portfolio[ticker]['current_price'] = self.fetch_stock_price(ticker)

    def portfolio_value(self):
        self.update_portfolio()
        total_value = 0
        for ticker in self.portfolio:
            stock_info = self.portfolio[ticker]
            total_value += stock_info['shares'] * stock_info['current_price']
        return total_value

    def portfolio_performance(self):
        self.update_portfolio()
        performance = {}
        total_profit_loss = 0
        for ticker in self.portfolio:
            stock_info = self.portfolio[ticker]
            current_value = stock_info['shares'] * stock_info['current_price']
            purchase_value = stock_info['shares'] * stock_info['purchase_price']
            profit_loss = current_value - purchase_value
            total_profit_loss += profit_loss
            performance[ticker] = {
                'current_value': current_value,
                'purchase_value': purchase_value,
                'profit_loss': profit_loss
            }
        performance['total_profit_loss'] = total_profit_loss
        return performance


# Example usage
api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'
portfolio = StockPortfolio(api_key)
portfolio.add_stock('AAPL', 10, 150)
portfolio.add_stock('MSFT', 5, 250)
print("Portfolio Value: $", portfolio.portfolio_value())
print("Portfolio Performance: ", portfolio.portfolio_performance())
