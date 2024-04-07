import requests
from bs4 import BeautifulSoup

# 發送 HTTP 請求獲取台灣證券交易所網站上的台灣 20 大股票資訊
url = 'https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX20?response=html'
response = requests.get(url)

# 使用 BeautifulSoup 解析 HTML 網頁 
soup = BeautifulSoup(response.text, 'html.parser')

# 提取表格
table = soup.find('table')

# 提取表頭
headers = [header.text.strip() for header in table.find_all('th')]

# 提取資料
data = []
for row in table.find_all('tr'):
    row_data = [cell.text.strip() for cell in row.find_all('td')]
    if row_data:
        data.append(row_data)

# 輸出結果
print(headers)
for row in data:
    print(row)
