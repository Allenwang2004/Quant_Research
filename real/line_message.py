from realtime_class import RealTimeKLine    
from utils import line_print

symbol = 'BTCUSDT'.lower()
interval = '1h'
realtime_kline = RealTimeKLine(symbol, interval)

timeformat = '%Y-%m-%d %H:%M:%S'
for data in realtime_kline.update_data():
    latest_close = data['close'].iloc[-1]
    latest_time = data.index[-1].strftime(timeformat)
    line_print(f"\n{symbol}\n Time: {latest_time}\n Close: {latest_close}")