import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# --------------------------
# Step 1: Extract Tesla Stock Data (Q1)
# --------------------------
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)

# --------------------------
# Step 2: Webscrape Tesla Revenue (Q2)
# --------------------------
url_tesla = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url_tesla).text
soup = BeautifulSoup(html_data, "html.parser")
tables = soup.find_all("table")

tesla_revenue_list = []
for table in tables:
    if "Tesla Quarterly Revenue" in table.text:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                date = cols[0].text.strip()
                revenue = cols[1].text.strip()
                tesla_revenue_list.append({"Date": date, "Revenue": revenue})
        break

tesla_revenue = pd.DataFrame(tesla_revenue_list)
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(r"\$|,", "", regex=True)
tesla_revenue = tesla_revenue[tesla_revenue["Revenue"] != ""]
tesla_revenue.dropna(inplace=True)

# --------------------------
# Step 3: Extract GameStop Stock Data (Q3)
# --------------------------
gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)

# --------------------------
# Step 4: Webscrape GameStop Revenue (Q4)
# --------------------------
url_gme = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data_2 = requests.get(url_gme).text
soup_gme = BeautifulSoup(html_data_2, "html.parser")
tables_gme = soup_gme.find_all("table")

gme_revenue_list = []
for table in tables_gme:
    if "GameStop Quarterly Revenue" in table.text:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                date = cols[0].text.strip()
                revenue = cols[1].text.strip()
                gme_revenue_list.append({"Date": date, "Revenue": revenue})
        break

gme_revenue = pd.DataFrame(gme_revenue_list)
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(r"\$|,", "", regex=True)
gme_revenue = gme_revenue[gme_revenue["Revenue"] != ""]
gme_revenue.dropna(inplace=True)

# --------------------------
# Step 5: Define make_graph function
# --------------------------
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=(f"{stock} Historical Share Price", f"{stock} Historical Revenue"), vertical_spacing=0.3)
    
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    
    fig.add_trace(go.Scatter(x=stock_data_specific.Date, y=stock_data_specific.Close, name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=revenue_data_specific.Date, y=revenue_data_specific.Revenue, name="Revenue"), row=2, col=1)
    
    fig.update_layout(height=600, showlegend=False, title=stock, xaxis_rangeslider_visible=True)
    fig.show()

# --------------------------
# Step 6: Plot Tesla and GME (Q5 & Q6)
# --------------------------
make_graph(tesla_data, tesla_revenue, "Tesla")
make_graph(gme_data, gme_revenue, "GameStop")
