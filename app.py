import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# 导入自定义模块
from data_fetcher import BinanceDataFetcher
from indicators import TechnicalIndicators
from backtest_engine import BacktestEngine
from chart_utils import ChartUtils

# 设置页面配置
st.set_page_config(
    page_title="币安量化回测系统",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 页面标题
st.title("🚀 币安量化回测策略系统")
st.markdown("---")

# 初始化数据获取器
@st.cache_resource
def get_data_fetcher():
    return BinanceDataFetcher()

data_fetcher = get_data_fetcher()

# 侧边栏配置
st.sidebar.header("📊 回测配置")

# 1. 币种选择
st.sidebar.subheader("币种选择")
available_symbols = data_fetcher.get_available_symbols()
if available_symbols:
    # 过滤出主要币种
    main_symbols = [s for s in available_symbols if any(coin in s for coin in ['BTC', 'ETH', 'BNB', 'ADA', 'DOT', 'LINK', 'LTC', 'XRP'])]
    selected_symbol = st.sidebar.selectbox(
        "选择交易对",
        main_symbols,
        index=0 if main_symbols else 0
    )
else:
    st.sidebar.error("无法获取交易对列表")
    selected_symbol = "BTC/USDT"

# 2. 时间范围设置
st.sidebar.subheader("时间范围")
col1, col2 = st.sidebar.columns(2)

with col1:
    start_date = st.date_input(
        "开始日期",
        value=datetime.now() - timedelta(days=365),
        max_value=datetime.now()
    )

with col2:
    end_date = st.date_input(
        "结束日期",
        value=datetime.now(),
        max_value=datetime.now()
    )

# 3. 时间周期选择
timeframe_options = {
    "1分钟": "1m",
    "5分钟": "5m", 
    "15分钟": "15m",
    "1小时": "1h",
    "4小时": "4h",
    "1天": "1d"
}

selected_timeframe = st.sidebar.selectbox(
    "时间周期",
    list(timeframe_options.keys()),
    index=5  # 默认选择1天
)

# 4. 回测参数
st.sidebar.subheader("回测参数")
initial_capital = st.sidebar.number_input(
    "初始资金 (USDT)",
    min_value=100,
    max_value=1000000,
    value=10000,
    step=1000
)

commission = st.sidebar.slider(
    "手续费率 (%)",
    min_value=0.0,
    max_value=1.0,
    value=0.1,
    step=0.01
) / 100

# 止盈止损设置
st.sidebar.subheader("止盈止损")
use_take_profit = st.sidebar.checkbox("启用止盈", value=False)
use_stop_loss = st.sidebar.checkbox("启用止损", value=False)

take_profit_pct = None
stop_loss_pct = None

if use_take_profit:
    take_profit_pct = st.sidebar.slider(
        "止盈百分比 (%)",
        min_value=1.0,
        max_value=50.0,
        value=10.0,
        step=0.5
    ) / 100

if use_stop_loss:
    stop_loss_pct = st.sidebar.slider(
        "止损百分比 (%)",
        min_value=1.0,
        max_value=20.0,
        value=5.0,
        step=0.5
    ) / 100

# 5. 技术指标选择
st.sidebar.subheader("技术指标")
indicators = {}

# RSI
if st.sidebar.checkbox("RSI", value=True):
    col1, col2 = st.sidebar.columns(2)
    with col1:
        rsi_period = st.number_input("RSI周期", min_value=5, max_value=50, value=14)
    with col2:
        rsi_oversold = st.number_input("超卖线", min_value=10, max_value=40, value=30)
    
    col3, col4 = st.sidebar.columns(2)
    with col3:
        rsi_overbought = st.number_input("超买线", min_value=60, max_value=90, value=70)
    
    indicators['rsi'] = True
    indicators['rsi_period'] = rsi_period
    indicators['rsi_oversold'] = rsi_oversold
    indicators['rsi_overbought'] = rsi_overbought

# KDJ
if st.sidebar.checkbox("KDJ"):
    col1, col2 = st.sidebar.columns(2)
    with col1:
        kdj_k_period = st.number_input("K周期", min_value=5, max_value=20, value=9)
    with col2:
        kdj_d_period = st.number_input("D周期", min_value=2, max_value=10, value=3)
    
    col3, col4 = st.sidebar.columns(2)
    with col3:
        kdj_j_period = st.number_input("J周期", min_value=2, max_value=10, value=3)
    with col4:
        kdj_buy_threshold = st.number_input("买入阈值", min_value=10, max_value=30, value=20)
    
    col5, col6 = st.sidebar.columns(2)
    with col5:
        kdj_sell_threshold = st.number_input("卖出阈值", min_value=70, max_value=90, value=80)
    
    indicators['kdj'] = True
    indicators['kdj_k_period'] = kdj_k_period
    indicators['kdj_d_period'] = kdj_d_period
    indicators['kdj_j_period'] = kdj_j_period
    indicators['kdj_buy_threshold'] = kdj_buy_threshold
    indicators['kdj_sell_threshold'] = kdj_sell_threshold

# 布林带
if st.sidebar.checkbox("布林带"):
    col1, col2 = st.sidebar.columns(2)
    with col1:
        bb_period = st.number_input("布林带周期", min_value=10, max_value=50, value=20)
    with col2:
        bb_std = st.number_input("标准差倍数", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
    
    indicators['boll'] = True
    indicators['bb_period'] = bb_period
    indicators['bb_std'] = bb_std

# EMA
if st.sidebar.checkbox("EMA"):
    col1, col2 = st.sidebar.columns(2)
    with col1:
        ema_short = st.number_input("短期EMA", min_value=5, max_value=20, value=12)
    with col2:
        ema_long = st.number_input("长期EMA", min_value=20, max_value=50, value=26)
    
    indicators['ema'] = True
    indicators['ema_periods'] = [ema_short, ema_long]
    indicators['ema_short'] = ema_short
    indicators['ema_long'] = ema_long

# SMA
if st.sidebar.checkbox("SMA"):
    col1, col2 = st.sidebar.columns(2)
    with col1:
        sma_short = st.number_input("短期SMA", min_value=10, max_value=30, value=20)
    with col2:
        sma_long = st.number_input("长期SMA", min_value=30, max_value=100, value=50)
    
    indicators['sma'] = True
    indicators['sma_periods'] = [sma_short, sma_long]

# MACD
if st.sidebar.checkbox("MACD"):
    col1, col2 = st.sidebar.columns(2)
    with col1:
        macd_fast = st.number_input("MACD快线", min_value=5, max_value=20, value=12)
    with col2:
        macd_slow = st.number_input("MACD慢线", min_value=20, max_value=50, value=26)
    
    col3, col4 = st.sidebar.columns(2)
    with col3:
        macd_signal = st.number_input("MACD信号线", min_value=5, max_value=20, value=9)
    
    indicators['macd'] = True
    indicators['macd_fast'] = macd_fast
    indicators['macd_slow'] = macd_slow
    indicators['macd_signal'] = macd_signal

# 随机指标
if st.sidebar.checkbox("随机指标"):
    col1, col2 = st.sidebar.columns(2)
    with col1:
        stoch_k_period = st.number_input("%K周期", min_value=5, max_value=20, value=14)
    with col2:
        stoch_d_period = st.number_input("%D周期", min_value=2, max_value=10, value=3)
    
    indicators['stoch'] = True
    indicators['stoch_k_period'] = stoch_k_period
    indicators['stoch_d_period'] = stoch_d_period

# ATR
if st.sidebar.checkbox("ATR"):
    atr_period = st.number_input("ATR周期", min_value=5, max_value=30, value=14)
    indicators['atr'] = True
    indicators['atr_period'] = atr_period

# 广告位
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='background: linear-gradient(135deg, #ff6b6b, #ffd93d); padding: 15px; border-radius: 10px; margin: 10px 0; text-align: center;'>
        <h4 style='color: #2c3e50; margin: 0 0 10px 0;'>🚀 盯盘狗量化</h4>
        <p style='color: #2c3e50; font-size: 14px; margin: 5px 0; font-weight: bold;'>17天收益553%</p>
        <p style='color: #2c3e50; font-size: 12px; margin: 5px 0;'>自动监控50+币种</p>
        <p style='color: #2c3e50; font-size: 11px; margin: 5px 0;'>微信: rggboom</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 运行回测按钮
st.sidebar.markdown("---")
run_backtest = st.sidebar.button("🚀 运行回测", type="primary")

# 主界面
if run_backtest:
    with st.spinner("正在获取数据..."):
        # 获取历史数据
        df = data_fetcher.fetch_historical_data(
            selected_symbol,
            start_date,
            end_date,
            timeframe_options[selected_timeframe]
        )
        
        if df.empty:
            st.error("无法获取数据，请检查网络连接或选择其他时间范围")
        else:
            st.success(f"成功获取 {len(df)} 条数据")
            
            # 计算技术指标
            with st.spinner("正在计算技术指标..."):
                df_with_indicators = TechnicalIndicators.calculate_all_indicators(df, indicators)
            
            # 运行回测
            with st.spinner("正在运行回测..."):
                engine = BacktestEngine(initial_capital, commission, take_profit_pct, stop_loss_pct)
                results = engine.run_backtest(df_with_indicators, indicators)
            
            if results:
                # 显示回测结果
                st.header("📊 回测结果")
                
                # 性能指标
                metrics = engine.get_performance_metrics()
                
                # 创建指标展示
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("总收益率", metrics['总收益率'])
                with col2:
                    st.metric("年化收益率", metrics['年化收益率'])
                with col3:
                    st.metric("最大回撤", metrics['最大回撤'])
                with col4:
                    st.metric("夏普比率", metrics['夏普比率'])
                
                col5, col6, col7, col8 = st.columns(4)
                with col5:
                    st.metric("胜率", metrics['胜率'])
                with col6:
                    st.metric("总交易次数", metrics['总交易次数'])
                with col7:
                    st.metric("止盈次数", metrics['止盈次数'])
                with col8:
                    st.metric("止损次数", metrics['止损次数'])
                
                col9, col10, col11, col12 = st.columns(4)
                with col9:
                    st.metric("正常卖出次数", metrics['正常卖出次数'])
                with col10:
                    st.metric("初始资金", metrics['初始资金'])
                with col11:
                    st.metric("最终资金", metrics['最终资金'])
                
                # 图表展示
                st.header("📈 图表分析")
                
                # 创建标签页
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["技术分析", "权益曲线", "回撤分析", "交易点位", "交易记录"])
                
                with tab1:
                    # 技术分析图
                    selected_indicators = [k for k in indicators.keys() if k not in ['rsi_period', 'rsi_oversold', 'rsi_overbought', 
                                                                                   'kdj_k_period', 'kdj_d_period', 'kdj_j_period', 
                                                                                   'kdj_buy_threshold', 'kdj_sell_threshold',
                                                                                   'bb_period', 'bb_std', 'ema_periods', 'ema_short', 
                                                                                   'ema_long', 'sma_periods', 'macd_fast', 'macd_slow', 
                                                                                   'macd_signal', 'stoch_k_period', 'stoch_d_period', 'atr_period']]
                    
                    tech_chart = ChartUtils.create_technical_chart(
                        df_with_indicators, 
                        selected_indicators,
                        f"{selected_symbol} 技术分析"
                    )
                    st.plotly_chart(tech_chart, use_container_width=True)
                
                with tab2:
                    # 权益曲线
                    equity_chart = ChartUtils.create_equity_chart(
                        results['equity_curve'],
                        f"{selected_symbol} 权益曲线"
                    )
                    st.plotly_chart(equity_chart, use_container_width=True)
                
                with tab3:
                    # 回撤分析
                    drawdown_chart = ChartUtils.create_drawdown_chart(
                        results['equity_curve'],
                        f"{selected_symbol} 回撤分析"
                    )
                    st.plotly_chart(drawdown_chart, use_container_width=True)
                
                with tab4:
                    # 交易点位图
                    trade_chart = ChartUtils.create_trade_chart(
                        df_with_indicators,
                        results['trades'],
                        f"{selected_symbol} 交易点位"
                    )
                    st.plotly_chart(trade_chart, use_container_width=True)
                
                with tab5:
                    # 交易记录
                    if not results['trades'].empty:
                        st.dataframe(results['trades'], use_container_width=True)
                        
                        # 导出交易记录
                        csv = results['trades'].to_csv(index=False)
                        st.download_button(
                            label="📥 下载交易记录",
                            data=csv,
                            file_name=f"{selected_symbol.replace('/', '_')}_trades.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("暂无交易记录")
                
                # 策略参数总结
                st.header("⚙️ 策略参数")
                st.json(indicators)
                
            else:
                st.error("回测运行失败，请检查参数设置")

else:
    # 显示欢迎信息
    st.markdown("""
    ## 🎯 使用说明
    
    1. **选择币种**: 在侧边栏选择要回测的交易对
    2. **设置时间范围**: 选择回测的开始和结束日期
    3. **选择时间周期**: 选择K线的时间周期（1分钟到1天）
    4. **配置回测参数**: 设置初始资金和手续费率
    5. **选择技术指标**: 勾选要使用的技术指标并设置参数
    6. **运行回测**: 点击"运行回测"按钮开始分析
    
    ## 📊 支持的技术指标
    
    - **RSI**: 相对强弱指数，用于判断超买超卖
    - **KDJ**: 随机指标，用于判断买卖点（基于ta库）
    - **布林带**: 用于判断价格波动范围
    - **EMA**: 指数移动平均线，用于趋势判断
    - **SMA**: 简单移动平均线
    - **MACD**: 移动平均收敛发散指标
    - **随机指标**: 随机振荡器
    - **ATR**: 平均真实波幅
    
    ## ⚠️ 注意事项
    
    - 本系统仅用于学习和研究目的
    - 历史表现不代表未来收益
    - 请根据实际情况调整参数
    - 建议在实盘交易前充分测试
    """)
    
    # 显示当前市场信息
    st.header("📈 市场概览")
    
    try:
        # 获取主要币种当前价格
        main_coins = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT']
        price_data = []
        
        for coin in main_coins:
            price = data_fetcher.get_current_price(coin)
            if price:
                price_data.append({
                    '币种': coin,
                    '当前价格': f"${price:,.2f}"
                })
        
        if price_data:
            price_df = pd.DataFrame(price_data)
            st.dataframe(price_df, use_container_width=True)
        else:
            st.info("无法获取当前价格信息")
            
    except Exception as e:
        st.info("市场数据暂时不可用")

# 广告推广
st.markdown("---")
st.markdown(
    """
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin: 20px 0;'>
        <div style='color: white; text-align: center;'>
            <h3 style='color: #FFD700; margin-bottom: 15px;'>🚀 盯盘狗量化策略</h3>
            <p style='font-size: 16px; margin-bottom: 10px;'>我们这个策略其实就是靠自动化在炒币，整个流程非常简单：</p>
            <p style='font-size: 16px; margin-bottom: 15px;'>它会一直监控市面上 50 多个币种，一旦发现有开仓信号，就会自动下单开仓</p>
            <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 15px 0;'>
                <p style='font-size: 18px; font-weight: bold; color: #00ff88; margin: 5px 0;'>📈 3天收益 133%</p>
                <p style='font-size: 18px; font-weight: bold; color: #00ff88; margin: 5px 0;'>📈 8天收益 242%</p>
                <p style='font-size: 20px; font-weight: bold; color: #FFD700; margin: 5px 0;'>🔥 最猛那轮，17天收益飙到 553%</p>
            </div>
            <div style='margin-top: 20px;'>
                <p style='font-size: 16px; margin: 10px 0;'>📱 <strong>Telegram:</strong> <a href='https://t.me/whogotbtc' style='color: #FFD700; text-decoration: none;'>https://t.me/whogotbtc</a></p>
                <p style='font-size: 16px; margin: 10px 0;'>📱 <strong>Telegram群:</strong> <a href='https://t.me/shipanjiankong' style='color: #FFD700; text-decoration: none;'>https://t.me/shipanjiankong</a></p>
                <p style='font-size: 16px; margin: 10px 0;'>💬 <strong>微信联系:</strong> <span style='color: #FFD700; font-weight: bold;'>rggboom</span></p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>币安量化回测系统 | 仅供学习和研究使用</p>
    </div>
    """,
    unsafe_allow_html=True
)
