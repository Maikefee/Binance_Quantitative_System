"""
币安量化回测系统配置文件
"""

# 默认回测参数
DEFAULT_CONFIG = {
    # 回测参数
    'initial_capital': 10000,  # 初始资金
    'commission': 0.001,       # 手续费率
    
    # 默认技术指标参数
    'indicators': {
        'rsi': {
            'period': 14,
            'oversold': 30,
            'overbought': 70
        },
        'kdj': {
            'k_period': 9,
            'd_period': 3,
            'j_period': 3,
            'buy_threshold': 20,
            'sell_threshold': 80
        },
        'bollinger_bands': {
            'period': 20,
            'std_dev': 2
        },
        'ema': {
            'short_period': 12,
            'long_period': 26
        },
        'sma': {
            'short_period': 20,
            'long_period': 50
        },
        'macd': {
            'fast_period': 12,
            'slow_period': 26,
            'signal_period': 9
        },
        'stochastic': {
            'k_period': 14,
            'd_period': 3
        },
        'atr': {
            'period': 14
        }
    },
    
    # 数据获取参数
    'data': {
        'timeframe': '1d',
        'limit': 1000,
        'retry_count': 3,
        'retry_delay': 1
    },
    
    # 图表配置
    'charts': {
        'height': 600,
        'width': 800,
        'theme': 'plotly_white'
    }
}

# 支持的交易对
SUPPORTED_SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT',
    'DOT/USDT', 'LINK/USDT', 'LTC/USDT', 'XRP/USDT',
    'BCH/USDT', 'EOS/USDT', 'TRX/USDT', 'XLM/USDT'
]

# 支持的时间周期
TIMEFRAMES = {
    '1分钟': '1m',
    '5分钟': '5m',
    '15分钟': '15m',
    '30分钟': '30m',
    '1小时': '1h',
    '4小时': '4h',
    '1天': '1d',
    '1周': '1w'
}

# 策略模板
STRATEGY_TEMPLATES = {
    'RSI策略': {
        'description': '基于RSI超买超卖的简单策略',
        'indicators': ['rsi'],
        'params': {
            'rsi_oversold': 30,
            'rsi_overbought': 70
        }
    },
    'KDJ策略': {
        'description': '基于KDJ金叉死叉的策略',
        'indicators': ['kdj'],
        'params': {
            'kdj_buy_threshold': 20,
            'kdj_sell_threshold': 80
        }
    },
    '布林带策略': {
        'description': '基于布林带突破的策略',
        'indicators': ['boll'],
        'params': {
            'bb_period': 20,
            'bb_std': 2
        }
    },
    'EMA交叉策略': {
        'description': '基于EMA短期长期线交叉的策略',
        'indicators': ['ema'],
        'params': {
            'ema_short': 12,
            'ema_long': 26
        }
    },
    'MACD策略': {
        'description': '基于MACD金叉死叉的策略',
        'indicators': ['macd'],
        'params': {
            'macd_fast': 12,
            'macd_slow': 26,
            'macd_signal': 9
        }
    },
    '综合策略': {
        'description': '结合多个指标的复合策略',
        'indicators': ['rsi', 'kdj', 'boll', 'ema'],
        'params': {
            'rsi_oversold': 30,
            'rsi_overbought': 70,
            'kdj_buy_threshold': 20,
            'kdj_sell_threshold': 80,
            'bb_period': 20,
            'bb_std': 2,
            'ema_short': 12,
            'ema_long': 26
        }
    }
}

# 性能指标阈值
PERFORMANCE_THRESHOLDS = {
    'excellent': {
        'annual_return': 20,
        'sharpe_ratio': 1.5,
        'max_drawdown': -10,
        'win_rate': 60
    },
    'good': {
        'annual_return': 10,
        'sharpe_ratio': 1.0,
        'max_drawdown': -20,
        'win_rate': 50
    },
    'fair': {
        'annual_return': 5,
        'sharpe_ratio': 0.5,
        'max_drawdown': -30,
        'win_rate': 40
    }
}
