import pandas as pd
import numpy as np
import ta

class TechnicalIndicators:
    """技术指标计算类"""
    
    @staticmethod
    def calculate_rsi(df, period=14):
        """
        计算RSI指标
        
        Args:
            df: 包含OHLCV数据的DataFrame
            period: RSI周期，默认14
        """
        try:
            rsi = ta.momentum.RSIIndicator(df['close'], window=period)
            return rsi.rsi()
        except Exception as e:
            print(f"计算RSI失败: {e}")
            return pd.Series(index=df.index)
    
    @staticmethod
    def calculate_kdj(df, k_period=9, d_period=3, j_period=3):
        """
        计算KDJ指标
        
        Args:
            df: 包含OHLCV数据的DataFrame
            k_period: K值周期，默认9
            d_period: D值周期，默认3
            j_period: J值周期，默认3
        """
        try:
            # 使用ta库的StochasticOscillator计算K和D值
            stoch = ta.momentum.StochasticOscillator(
                df['high'], 
                df['low'], 
                df['close'],
                window=k_period, 
                smooth_window=d_period
            )
            
            k = stoch.stoch()
            d = stoch.stoch_signal()
            
            # 计算J值: J = 3*K - 2*D
            j = 3 * k - 2 * d
            
            return pd.DataFrame({
                'K': k,
                'D': d,
                'J': j
            })
        except Exception as e:
            print(f"计算KDJ失败: {e}")
            return pd.DataFrame(index=df.index)
    
    @staticmethod
    def calculate_bollinger_bands(df, period=20, std_dev=2):
        """
        计算布林带指标
        
        Args:
            df: 包含OHLCV数据的DataFrame
            period: 移动平均周期，默认20
            std_dev: 标准差倍数，默认2
        """
        try:
            bb = ta.volatility.BollingerBands(df['close'], window=period, window_dev=std_dev)
            return pd.DataFrame({
                'BB_upper': bb.bollinger_hband(),
                'BB_middle': bb.bollinger_mavg(),
                'BB_lower': bb.bollinger_lband()
            })
        except Exception as e:
            print(f"计算布林带失败: {e}")
            return pd.DataFrame(index=df.index)
    
    @staticmethod
    def calculate_ema(df, period=12):
        """
        计算指数移动平均线
        
        Args:
            df: 包含OHLCV数据的DataFrame
            period: EMA周期，默认12
        """
        try:
            ema = ta.trend.EMAIndicator(df['close'], window=period)
            return ema.ema_indicator()
        except Exception as e:
            print(f"计算EMA失败: {e}")
            return pd.Series(index=df.index)
    
    @staticmethod
    def calculate_sma(df, period=20):
        """
        计算简单移动平均线
        
        Args:
            df: 包含OHLCV数据的DataFrame
            period: SMA周期，默认20
        """
        try:
            sma = ta.trend.SMAIndicator(df['close'], window=period)
            return sma.sma_indicator()
        except Exception as e:
            print(f"计算SMA失败: {e}")
            return pd.Series(index=df.index)
    
    @staticmethod
    def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
        """
        计算MACD指标
        
        Args:
            df: 包含OHLCV数据的DataFrame
            fast_period: 快线周期，默认12
            slow_period: 慢线周期，默认26
            signal_period: 信号线周期，默认9
        """
        try:
            macd = ta.trend.MACD(df['close'], window_fast=fast_period, 
                               window_slow=slow_period, window_sign=signal_period)
            return pd.DataFrame({
                'MACD': macd.macd(),
                'MACD_signal': macd.macd_signal(),
                'MACD_histogram': macd.macd_diff()
            })
        except Exception as e:
            print(f"计算MACD失败: {e}")
            return pd.DataFrame(index=df.index)
    
    @staticmethod
    def calculate_stochastic(df, k_period=14, d_period=3):
        """
        计算随机指标
        
        Args:
            df: 包含OHLCV数据的DataFrame
            k_period: %K周期，默认14
            d_period: %D周期，默认3
        """
        try:
            stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'],
                                                   window=k_period, smooth_window=d_period)
            return pd.DataFrame({
                'Stoch_K': stoch.stoch(),
                'Stoch_D': stoch.stoch_signal()
            })
        except Exception as e:
            print(f"计算随机指标失败: {e}")
            return pd.DataFrame(index=df.index)
    
    @staticmethod
    def calculate_atr(df, period=14):
        """
        计算平均真实波幅
        
        Args:
            df: 包含OHLCV数据的DataFrame
            period: ATR周期，默认14
        """
        try:
            atr = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], window=period)
            return atr.average_true_range()
        except Exception as e:
            print(f"计算ATR失败: {e}")
            return pd.Series(index=df.index)
    
    @staticmethod
    def calculate_all_indicators(df, indicator_params=None):
        """
        计算所有技术指标
        
        Args:
            df: 包含OHLCV数据的DataFrame
            indicator_params: 指标参数字典
        """
        if indicator_params is None:
            indicator_params = {}
        
        result_df = df.copy()
        
        # RSI
        if 'rsi' in indicator_params:
            rsi_period = indicator_params.get('rsi_period', 14)
            result_df['RSI'] = TechnicalIndicators.calculate_rsi(df, rsi_period)
        
        # KDJ
        if 'kdj' in indicator_params:
            k_period = indicator_params.get('kdj_k_period', 9)
            d_period = indicator_params.get('kdj_d_period', 3)
            j_period = indicator_params.get('kdj_j_period', 3)
            kdj_df = TechnicalIndicators.calculate_kdj(df, k_period, d_period, j_period)
            result_df = pd.concat([result_df, kdj_df], axis=1)
        
        # 布林带
        if 'boll' in indicator_params:
            bb_period = indicator_params.get('bb_period', 20)
            bb_std = indicator_params.get('bb_std', 2)
            bb_df = TechnicalIndicators.calculate_bollinger_bands(df, bb_period, bb_std)
            result_df = pd.concat([result_df, bb_df], axis=1)
        
        # EMA
        if 'ema' in indicator_params:
            ema_periods = indicator_params.get('ema_periods', [12, 26])
            for period in ema_periods:
                result_df[f'EMA_{period}'] = TechnicalIndicators.calculate_ema(df, period)
        
        # SMA
        if 'sma' in indicator_params:
            sma_periods = indicator_params.get('sma_periods', [20, 50])
            for period in sma_periods:
                result_df[f'SMA_{period}'] = TechnicalIndicators.calculate_sma(df, period)
        
        # MACD
        if 'macd' in indicator_params:
            fast_period = indicator_params.get('macd_fast', 12)
            slow_period = indicator_params.get('macd_slow', 26)
            signal_period = indicator_params.get('macd_signal', 9)
            macd_df = TechnicalIndicators.calculate_macd(df, fast_period, slow_period, signal_period)
            result_df = pd.concat([result_df, macd_df], axis=1)
        
        # 随机指标
        if 'stoch' in indicator_params:
            k_period = indicator_params.get('stoch_k_period', 14)
            d_period = indicator_params.get('stoch_d_period', 3)
            stoch_df = TechnicalIndicators.calculate_stochastic(df, k_period, d_period)
            result_df = pd.concat([result_df, stoch_df], axis=1)
        
        # ATR
        if 'atr' in indicator_params:
            atr_period = indicator_params.get('atr_period', 14)
            result_df['ATR'] = TechnicalIndicators.calculate_atr(df, atr_period)
        
        return result_df
