import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class ChartUtils:
    """图表绘制工具类"""
    
    @staticmethod
    def create_candlestick_chart(df, title="K线图"):
        """
        创建K线图
        
        Args:
            df: 包含OHLCV数据的DataFrame
            title: 图表标题
        """
        fig = go.Figure()
        
        # 添加K线图
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='K线',
            increasing_line_color='#26A69A',
            decreasing_line_color='#EF5350'
        ))
        
        # 更新布局
        fig.update_layout(
            title=title,
            xaxis_title='时间',
            yaxis_title='价格',
            xaxis_rangeslider_visible=False,
            height=600
        )
        
        return fig
    
    @staticmethod
    def create_technical_chart(df, indicators=None, title="技术分析图"):
        """
        创建技术分析图表
        
        Args:
            df: 包含技术指标的DataFrame
            indicators: 要显示的指标列表
            title: 图表标题
        """
        if indicators is None:
            indicators = []
        
        # 创建子图
        subplot_titles = ['价格和指标']
        if 'RSI' in df.columns and 'rsi' in indicators:
            subplot_titles.append('RSI')
        if all(col in df.columns for col in ['K', 'D', 'J']) and 'kdj' in indicators:
            subplot_titles.append('KDJ')
        if 'MACD' in df.columns and 'macd' in indicators:
            subplot_titles.append('MACD')
        
        fig = make_subplots(
            rows=len(subplot_titles), cols=1,
            subplot_titles=subplot_titles,
            vertical_spacing=0.1,
            row_heights=[0.6] + [0.2] * (len(subplot_titles) - 1)
        )
        
        # 主图：K线和指标
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='K线',
            increasing_line_color='#26A69A',
            decreasing_line_color='#EF5350'
        ), row=1, col=1)
        
        # 添加布林带
        if all(col in df.columns for col in ['BB_upper', 'BB_middle', 'BB_lower']) and 'boll' in indicators:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['BB_upper'],
                mode='lines', name='布林带上轨',
                line=dict(color='rgba(255, 0, 0, 0.5)', width=1)
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index, y=df['BB_middle'],
                mode='lines', name='布林带中轨',
                line=dict(color='rgba(0, 0, 255, 0.5)', width=1)
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index, y=df['BB_lower'],
                mode='lines', name='布林带下轨',
                line=dict(color='rgba(255, 0, 0, 0.5)', width=1),
                fill='tonexty', fillcolor='rgba(255, 0, 0, 0.1)'
            ), row=1, col=1)
        
        # 添加EMA
        if 'ema' in indicators:
            ema_cols = [col for col in df.columns if col.startswith('EMA_')]
            for col in ema_cols:
                period = col.split('_')[1]
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[col],
                    mode='lines', name=f'EMA({period})',
                    line=dict(width=1)
                ), row=1, col=1)
        
        # 添加SMA
        if 'sma' in indicators:
            sma_cols = [col for col in df.columns if col.startswith('SMA_')]
            for col in sma_cols:
                period = col.split('_')[1]
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[col],
                    mode='lines', name=f'SMA({period})',
                    line=dict(width=1, dash='dash')
                ), row=1, col=1)
        
        # RSI子图
        if 'RSI' in df.columns and 'rsi' in indicators:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['RSI'],
                mode='lines', name='RSI',
                line=dict(color='purple', width=2)
            ), row=2, col=1)
            
            # 添加超买超卖线
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
            fig.add_hline(y=50, line_dash="dot", line_color="gray", row=2, col=1)
        
        # KDJ子图
        if all(col in df.columns for col in ['K', 'D', 'J']) and 'kdj' in indicators:
            row_idx = 2 if 'RSI' not in df.columns or 'rsi' not in indicators else 3
            
            fig.add_trace(go.Scatter(
                x=df.index, y=df['K'],
                mode='lines', name='K',
                line=dict(color='blue', width=2)
            ), row=row_idx, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index, y=df['D'],
                mode='lines', name='D',
                line=dict(color='red', width=2)
            ), row=row_idx, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index, y=df['J'],
                mode='lines', name='J',
                line=dict(color='green', width=2)
            ), row=row_idx, col=1)
            
            # 添加超买超卖线
            fig.add_hline(y=80, line_dash="dash", line_color="red", row=row_idx, col=1)
            fig.add_hline(y=20, line_dash="dash", line_color="green", row=row_idx, col=1)
        
        # MACD子图
        if all(col in df.columns for col in ['MACD', 'MACD_signal']) and 'macd' in indicators:
            row_idx = len(subplot_titles)
            
            fig.add_trace(go.Scatter(
                x=df.index, y=df['MACD'],
                mode='lines', name='MACD',
                line=dict(color='blue', width=2)
            ), row=row_idx, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index, y=df['MACD_signal'],
                mode='lines', name='MACD Signal',
                line=dict(color='red', width=2)
            ), row=row_idx, col=1)
            
            # MACD柱状图
            colors = ['green' if val >= 0 else 'red' for val in df['MACD_histogram']]
            fig.add_trace(go.Bar(
                x=df.index, y=df['MACD_histogram'],
                name='MACD Histogram',
                marker_color=colors
            ), row=row_idx, col=1)
        
        # 更新布局
        fig.update_layout(
            title=title,
            height=800,
            showlegend=True,
            xaxis_rangeslider_visible=False
        )
        
        return fig
    
    @staticmethod
    def create_equity_chart(equity_df, title="权益曲线"):
        """
        创建权益曲线图
        
        Args:
            equity_df: 权益曲线DataFrame
            title: 图表标题
        """
        fig = go.Figure()
        
        # 权益曲线
        fig.add_trace(go.Scatter(
            x=equity_df['timestamp'],
            y=equity_df['equity'],
            mode='lines',
            name='总权益',
            line=dict(color='blue', width=2)
        ))
        
        # 资金曲线
        fig.add_trace(go.Scatter(
            x=equity_df['timestamp'],
            y=equity_df['capital'],
            mode='lines',
            name='现金',
            line=dict(color='green', width=1)
        ))
        
        # 更新布局
        fig.update_layout(
            title=title,
            xaxis_title='时间',
            yaxis_title='金额',
            height=500
        )
        
        return fig
    
    @staticmethod
    def create_drawdown_chart(equity_df, title="回撤分析"):
        """
        创建回撤分析图
        
        Args:
            equity_df: 权益曲线DataFrame
            title: 图表标题
        """
        # 计算回撤
        equity_df = equity_df.copy()
        equity_df['peak'] = equity_df['equity'].expanding().max()
        equity_df['drawdown'] = (equity_df['equity'] - equity_df['peak']) / equity_df['peak'] * 100
        
        fig = go.Figure()
        
        # 回撤曲线
        fig.add_trace(go.Scatter(
            x=equity_df['timestamp'],
            y=equity_df['drawdown'],
            mode='lines',
            name='回撤',
            line=dict(color='red', width=2),
            fill='tonexty',
            fillcolor='rgba(255, 0, 0, 0.3)'
        ))
        
        # 更新布局
        fig.update_layout(
            title=title,
            xaxis_title='时间',
            yaxis_title='回撤 (%)',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_trade_chart(df, trades_df, title="交易点位图"):
        """
        创建交易点位图
        
        Args:
            df: 价格数据DataFrame
            trades_df: 交易记录DataFrame
            title: 图表标题
        """
        fig = go.Figure()
        
        # K线图
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='K线',
            increasing_line_color='#26A69A',
            decreasing_line_color='#EF5350'
        ))
        
        # 添加买入点
        if not trades_df.empty:
            buy_trades = trades_df[trades_df['action'] == 'BUY']
            if not buy_trades.empty:
                fig.add_trace(go.Scatter(
                    x=buy_trades['timestamp'],
                    y=buy_trades['price'],
                    mode='markers',
                    name='买入',
                    marker=dict(
                        symbol='triangle-up',
                        size=10,
                        color='green'
                    )
                ))
            
            # 添加正常卖出点
            sell_trades = trades_df[trades_df['action'] == 'SELL']
            if not sell_trades.empty:
                fig.add_trace(go.Scatter(
                    x=sell_trades['timestamp'],
                    y=sell_trades['price'],
                    mode='markers',
                    name='正常卖出',
                    marker=dict(
                        symbol='triangle-down',
                        size=10,
                        color='red'
                    )
                ))
            
            # 添加止盈点
            take_profit_trades = trades_df[trades_df['action'] == 'TAKE_PROFIT']
            if not take_profit_trades.empty:
                fig.add_trace(go.Scatter(
                    x=take_profit_trades['timestamp'],
                    y=take_profit_trades['price'],
                    mode='markers',
                    name='止盈',
                    marker=dict(
                        symbol='diamond',
                        size=12,
                        color='gold'
                    )
                ))
            
            # 添加止损点
            stop_loss_trades = trades_df[trades_df['action'] == 'STOP_LOSS']
            if not stop_loss_trades.empty:
                fig.add_trace(go.Scatter(
                    x=stop_loss_trades['timestamp'],
                    y=stop_loss_trades['price'],
                    mode='markers',
                    name='止损',
                    marker=dict(
                        symbol='x',
                        size=12,
                        color='purple'
                    )
                ))
        
        # 更新布局
        fig.update_layout(
            title=title,
            xaxis_title='时间',
            yaxis_title='价格',
            xaxis_rangeslider_visible=False,
            height=600
        )
        
        return fig
    
    @staticmethod
    def create_performance_summary(metrics):
        """
        创建性能指标汇总表
        
        Args:
            metrics: 性能指标字典
        """
        # 创建表格数据
        table_data = []
        for key, value in metrics.items():
            table_data.append([key, value])
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['指标', '数值'],
                fill_color='lightblue',
                align='left',
                font=dict(size=14)
            ),
            cells=dict(
                values=[[row[0] for row in table_data], [row[1] for row in table_data]],
                fill_color='white',
                align='left',
                font=dict(size=12)
            )
        )])
        
        fig.update_layout(
            title="回测结果汇总",
            height=400
        )
        
        return fig
