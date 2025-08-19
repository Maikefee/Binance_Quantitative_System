import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class BacktestEngine:
    """回测引擎"""
    
    def __init__(self, initial_capital=10000, commission=0.001, take_profit=None, stop_loss=None):
        """
        初始化回测引擎
        
        Args:
            initial_capital: 初始资金
            commission: 手续费率
            take_profit: 止盈百分比，如 0.1 表示10%
            stop_loss: 止损百分比，如 0.05 表示5%
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.reset()
    
    def reset(self):
        """重置回测状态"""
        self.capital = self.initial_capital
        self.position = 0
        self.avg_buy_price = 0  # 平均买入价格
        self.trades = []
        self.equity_curve = []
        self.current_price = 0
    
    def calculate_signals(self, df, strategy_params):
        """
        计算交易信号
        
        Args:
            df: 包含技术指标的DataFrame
            strategy_params: 策略参数字典
        """
        signals = pd.Series(0, index=df.index)
        
        # RSI策略
        if 'rsi' in strategy_params and 'RSI' in df.columns:
            rsi_oversold = strategy_params.get('rsi_oversold', 30)
            rsi_overbought = strategy_params.get('rsi_overbought', 70)
            
            # RSI超卖买入信号
            rsi_buy = (df['RSI'] < rsi_oversold) & (df['RSI'].shift(1) >= rsi_oversold)
            # RSI超买卖出信号
            rsi_sell = (df['RSI'] > rsi_overbought) & (df['RSI'].shift(1) <= rsi_overbought)
            
            signals[rsi_buy] = 1
            signals[rsi_sell] = -1
        
        # KDJ策略
        if 'kdj' in strategy_params and all(col in df.columns for col in ['K', 'D', 'J']):
            kdj_buy_threshold = strategy_params.get('kdj_buy_threshold', 20)
            kdj_sell_threshold = strategy_params.get('kdj_sell_threshold', 80)
            
            # KDJ金叉买入
            kdj_buy = (df['K'] > df['D']) & (df['K'].shift(1) <= df['D'].shift(1)) & (df['K'] < kdj_buy_threshold)
            # KDJ死叉卖出
            kdj_sell = (df['K'] < df['D']) & (df['K'].shift(1) >= df['D'].shift(1)) & (df['K'] > kdj_sell_threshold)
            
            signals[kdj_buy] = 1
            signals[kdj_sell] = -1
        
        # 布林带策略
        if 'boll' in strategy_params and all(col in df.columns for col in ['BB_upper', 'BB_middle', 'BB_lower']):
            # 价格触及下轨买入
            boll_buy = df['close'] <= df['BB_lower']
            # 价格触及上轨卖出
            boll_sell = df['close'] >= df['BB_upper']
            
            signals[boll_buy] = 1
            signals[boll_sell] = -1
        
        # EMA策略
        if 'ema' in strategy_params:
            ema_short = strategy_params.get('ema_short', 12)
            ema_long = strategy_params.get('ema_long', 26)
            
            if f'EMA_{ema_short}' in df.columns and f'EMA_{ema_long}' in df.columns:
                # 短期EMA上穿长期EMA买入
                ema_buy = (df[f'EMA_{ema_short}'] > df[f'EMA_{ema_long}']) & \
                         (df[f'EMA_{ema_short}'].shift(1) <= df[f'EMA_{ema_long}'].shift(1))
                # 短期EMA下穿长期EMA卖出
                ema_sell = (df[f'EMA_{ema_short}'] < df[f'EMA_{ema_long}']) & \
                          (df[f'EMA_{ema_short}'].shift(1) >= df[f'EMA_{ema_long}'].shift(1))
                
                signals[ema_buy] = 1
                signals[ema_sell] = -1
        
        # MACD策略
        if 'macd' in strategy_params and all(col in df.columns for col in ['MACD', 'MACD_signal']):
            # MACD金叉买入
            macd_buy = (df['MACD'] > df['MACD_signal']) & (df['MACD'].shift(1) <= df['MACD_signal'].shift(1))
            # MACD死叉卖出
            macd_sell = (df['MACD'] < df['MACD_signal']) & (df['MACD'].shift(1) >= df['MACD_signal'].shift(1))
            
            signals[macd_buy] = 1
            signals[macd_sell] = -1
        
        return signals
    
    def run_backtest(self, df, strategy_params):
        """
        运行回测
        
        Args:
            df: 包含技术指标的DataFrame
            strategy_params: 策略参数字典
        """
        self.reset()
        
        # 计算交易信号
        signals = self.calculate_signals(df, strategy_params)
        
        # 执行回测
        for i, (timestamp, row) in enumerate(df.iterrows()):
            self.current_price = row['close']
            
            # 检查止盈止损
            if self.position > 0 and self.avg_buy_price > 0:
                current_return = (self.current_price - self.avg_buy_price) / self.avg_buy_price
                
                # 止盈检查
                if self.take_profit and current_return >= self.take_profit:
                    # 触发止盈
                    revenue = self.position * self.current_price * (1 - self.commission)
                    self.capital += revenue
                    
                    self.trades.append({
                        'timestamp': timestamp,
                        'action': 'TAKE_PROFIT',
                        'price': self.current_price,
                        'shares': self.position,
                        'revenue': revenue,
                        'capital': self.capital,
                        'position': 0,
                        'return_pct': current_return * 100
                    })
                    
                    self.position = 0
                    self.avg_buy_price = 0
                    continue
                
                # 止损检查
                if self.stop_loss and current_return <= -self.stop_loss:
                    # 触发止损
                    revenue = self.position * self.current_price * (1 - self.commission)
                    self.capital += revenue
                    
                    self.trades.append({
                        'timestamp': timestamp,
                        'action': 'STOP_LOSS',
                        'price': self.current_price,
                        'shares': self.position,
                        'revenue': revenue,
                        'capital': self.capital,
                        'position': 0,
                        'return_pct': current_return * 100
                    })
                    
                    self.position = 0
                    self.avg_buy_price = 0
                    continue
            
            # 更新权益曲线
            current_equity = self.capital + self.position * self.current_price
            self.equity_curve.append({
                'timestamp': timestamp,
                'equity': current_equity,
                'capital': self.capital,
                'position': self.position,
                'price': self.current_price
            })
            
            # 处理交易信号
            if i > 0:  # 跳过第一个数据点
                signal = signals.iloc[i]
                
                if signal == 1 and self.position == 0:  # 买入信号
                    # 计算可买入数量
                    available_capital = self.capital * 0.95  # 保留5%现金
                    shares = int(available_capital / self.current_price)
                    
                    if shares > 0:
                        cost = shares * self.current_price * (1 + self.commission)
                        if cost <= self.capital:
                            self.position = shares
                            self.capital -= cost
                            self.avg_buy_price = self.current_price  # 记录买入价格
                            
                            self.trades.append({
                                'timestamp': timestamp,
                                'action': 'BUY',
                                'price': self.current_price,
                                'shares': shares,
                                'cost': cost,
                                'capital': self.capital,
                                'position': self.position
                            })
                
                elif signal == -1 and self.position > 0:  # 卖出信号
                    # 卖出所有持仓
                    revenue = self.position * self.current_price * (1 - self.commission)
                    self.capital += revenue
                    
                    self.trades.append({
                        'timestamp': timestamp,
                        'action': 'SELL',
                        'price': self.current_price,
                        'shares': self.position,
                        'revenue': revenue,
                        'capital': self.capital,
                        'position': 0
                    })
                    
                    self.position = 0
                    self.avg_buy_price = 0
        
        # 最后一天强制平仓
        if self.position > 0:
            revenue = self.position * self.current_price * (1 - self.commission)
            self.capital += revenue
            
            self.trades.append({
                'timestamp': df.index[-1],
                'action': 'SELL',
                'price': self.current_price,
                'shares': self.position,
                'revenue': revenue,
                'capital': self.capital,
                'position': 0
            })
        
        return self.get_results()
    
    def get_results(self):
        """获取回测结果"""
        if not self.equity_curve:
            return {}
        
        equity_df = pd.DataFrame(self.equity_curve)
        trades_df = pd.DataFrame(self.trades) if self.trades else pd.DataFrame()
        
        # 计算收益率
        initial_equity = self.initial_capital
        final_equity = equity_df['equity'].iloc[-1]
        total_return = (final_equity - initial_equity) / initial_equity * 100
        
        # 计算年化收益率
        days = (equity_df['timestamp'].iloc[-1] - equity_df['timestamp'].iloc[0]).days
        annual_return = (final_equity / initial_equity) ** (365 / days) - 1 if days > 0 else 0
        
        # 计算最大回撤
        equity_df['peak'] = equity_df['equity'].expanding().max()
        equity_df['drawdown'] = (equity_df['equity'] - equity_df['peak']) / equity_df['peak'] * 100
        max_drawdown = equity_df['drawdown'].min()
        
        # 计算夏普比率
        equity_df['daily_return'] = equity_df['equity'].pct_change()
        sharpe_ratio = equity_df['daily_return'].mean() / equity_df['daily_return'].std() * np.sqrt(252) if equity_df['daily_return'].std() > 0 else 0
        
        # 计算胜率和止盈止损统计
        if not trades_df.empty:
            # 计算止盈止损次数
            take_profit_count = len(trades_df[trades_df['action'] == 'TAKE_PROFIT'])
            stop_loss_count = len(trades_df[trades_df['action'] == 'STOP_LOSS'])
            normal_sell_count = len(trades_df[trades_df['action'] == 'SELL'])
            
            # 计算每笔交易的收益
            buy_trades = trades_df[trades_df['action'] == 'BUY']
            sell_trades = trades_df[trades_df['action'].isin(['SELL', 'TAKE_PROFIT', 'STOP_LOSS'])]
            
            if len(buy_trades) > 0 and len(sell_trades) > 0:
                trade_returns = []
                for i in range(min(len(buy_trades), len(sell_trades))):
                    buy_price = buy_trades.iloc[i]['price']
                    sell_price = sell_trades.iloc[i]['price']
                    trade_return = (sell_price - buy_price) / buy_price
                    trade_returns.append(trade_return)
                
                win_rate = sum(1 for r in trade_returns if r > 0) / len(trade_returns) * 100 if trade_returns else 0
            else:
                win_rate = 0
        else:
            win_rate = 0
            take_profit_count = 0
            stop_loss_count = 0
            normal_sell_count = 0
        
        return {
            'initial_capital': initial_equity,
            'final_equity': final_equity,
            'total_return': total_return,
            'annual_return': annual_return * 100,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'total_trades': len(trades_df) // 2 if trades_df is not None else 0,
            'take_profit_count': take_profit_count,
            'stop_loss_count': stop_loss_count,
            'normal_sell_count': normal_sell_count,
            'equity_curve': equity_df,
            'trades': trades_df
        }
    
    def get_performance_metrics(self):
        """获取性能指标"""
        results = self.get_results()
        
        metrics = {
            '总收益率': f"{results.get('total_return', 0):.2f}%",
            '年化收益率': f"{results.get('annual_return', 0):.2f}%",
            '最大回撤': f"{results.get('max_drawdown', 0):.2f}%",
            '夏普比率': f"{results.get('sharpe_ratio', 0):.2f}",
            '胜率': f"{results.get('win_rate', 0):.2f}%",
            '总交易次数': results.get('total_trades', 0),
            '止盈次数': results.get('take_profit_count', 0),
            '止损次数': results.get('stop_loss_count', 0),
            '正常卖出次数': results.get('normal_sell_count', 0),
            '初始资金': f"${results.get('initial_capital', 0):,.2f}",
            '最终资金': f"${results.get('final_equity', 0):,.2f}"
        }
        
        return metrics
