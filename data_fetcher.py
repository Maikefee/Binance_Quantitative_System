import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import time

class BinanceDataFetcher:
    """币安数据获取器"""
    
    def __init__(self):
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot'
            }
        })
    
    def get_available_symbols(self):
        """获取可用的交易对"""
        try:
            markets = self.exchange.load_markets()
            # 过滤出USDT交易对
            usdt_pairs = [symbol for symbol in markets.keys() if symbol.endswith('/USDT')]
            return sorted(usdt_pairs)
        except Exception as e:
            print(f"获取交易对失败: {e}")
            return []
    
    def fetch_ohlcv(self, symbol, timeframe='1d', limit=1000, since=None):
        """
        获取K线数据
        
        Args:
            symbol: 交易对，如 'BTC/USDT'
            timeframe: 时间周期，如 '1m', '5m', '1h', '1d'
            limit: 获取数量
            since: 开始时间戳
        """
        try:
            # 转换时间格式
            if since:
                if isinstance(since, str):
                    since = int(datetime.strptime(since, '%Y-%m-%d').timestamp() * 1000)
                elif isinstance(since, datetime):
                    since = int(since.timestamp() * 1000)
            
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            
            # 转换为DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            print(f"获取数据失败: {e}")
            return pd.DataFrame()
    
    def fetch_historical_data(self, symbol, start_date, end_date, timeframe='1d'):
        """
        获取历史数据
        
        Args:
            symbol: 交易对
            start_date: 开始日期
            end_date: 结束日期
            timeframe: 时间周期
        """
        try:
            # 转换日期格式
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            elif isinstance(start_date, date):
                start_date = datetime.combine(start_date, datetime.min.time())
            elif not isinstance(start_date, datetime):
                start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
                
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            elif isinstance(end_date, date):
                end_date = datetime.combine(end_date, datetime.min.time())
            elif not isinstance(end_date, datetime):
                end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
            
            # 计算时间戳
            since = int(start_date.timestamp() * 1000)
            end_timestamp = int(end_date.timestamp() * 1000)
            
            all_data = []
            current_since = since
            
            while current_since < end_timestamp:
                # 获取数据
                ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, current_since, 1000)
                
                if not ohlcv:
                    break
                
                all_data.extend(ohlcv)
                
                # 更新时间戳
                current_since = ohlcv[-1][0] + 1
                
                # 避免请求过于频繁
                time.sleep(0.1)
            
            if not all_data:
                return pd.DataFrame()
            
            # 转换为DataFrame
            df = pd.DataFrame(all_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # 过滤日期范围
            df = df[(df.index >= start_date) & (df.index <= end_date)]
            
            return df
            
        except Exception as e:
            print(f"获取历史数据失败: {e}")
            return pd.DataFrame()
    
    def get_current_price(self, symbol):
        """获取当前价格"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except Exception as e:
            print(f"获取当前价格失败: {e}")
            return None
