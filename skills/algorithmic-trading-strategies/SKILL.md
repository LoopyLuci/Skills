---
name: algorithmic-trading-strategies
description: "Use when building algo trading. Backtesting, execution."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [trading, finance, backtesting, quantitative, algo-trading]
    related_skills: [banking-api-integration, financial-modeling-python]
---

# Algorithmic Trading Strategy Development

## Overview
Build, test, and deploy algorithmic trading strategies for equities, forex, crypto, and futures markets. Covers strategy design, backtesting framework, risk management, execution optimization, and performance evaluation with quantitative rigor.

## When to Use
- "Build a backtestable trading strategy"
- "Optimize trading execution"
- "Evaluate algo trading performance"
- "Design quantitative risk controls"
- "Implement portfolio rebalancing"

## Strategy Design Framework

### 1. Market Regime Classification
| Regime | Characteristics | Suitable Strategies |
|--------|----------------|-------------------|
| Trending | Strong directional momentum | Momentum, breakout |
| Mean-reverting | Price oscillates around mean | Mean reversion, pairs |
| Volatile | High variance, large swings | Options selling, volatility arbitrage |
| Quiet | Low volatility, sideways | Market making, range trading |

### 2. Strategy Components
```python
class TradingStrategy:
    def __init__(self, symbol, lookback=20):
        self.symbol = symbol
        self.lookback = lookback
        self.position = 0  # -1=short, 0=flat, 1=long
        
    def calculate_signals(self, market_data):
        """Generate buy/sell/hold signals"""
        prices = market_data['close']
        moving_avg = prices.rolling(self.lookback).mean()
        std_dev = prices.rolling(self.lookback).std()
        
        # Bollinger Band mean reversion
        upper_band = moving_avg + (std_dev * 2)
        lower_band = moving_avg - (std_dev * 2)
        
        if prices.iloc[-1] > upper_band.iloc[-1]:
            return -1  # Short signal
        elif prices.iloc[-1] < lower_band.iloc[-1]:
            return 1  # Long signal
        else:
            return 0  # Hold

    def risk_management(self, capital, portfolio):
        """Position sizing and risk controls"""
        max_position = 0.1  # Max 10% per trade
        risk_per_trade = capital * 0.02  # 2% risk per trade
        
        if self.position != 0:
            # Check stop loss, take profit, time decay
            current_value = self.get_position_value(portfolio)
            if (self.entry_price - current_value) / self.entry_price > 0.05:
                return "stop_loss"  # 5% stop loss triggered
        return "hold"
```

### 3. Backtesting Engine Pattern
```python
import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, strategy, data, initial_capital=100000):
        self.strategy = strategy
        self.data = data
        self.capital = initial_capital
        self.portfolio = {"cash": initial_capital, "positions": {}}
        self.trades = []
        
    def run(self):
        for i in range(len(self.data)):
            bar = self.data.iloc[:i+1]
            signal = self.strategy.calculate_signals(bar)
            
            if signal != 0:
                self.execute_trade(signal, bar.iloc[-1])
                
        return self.generate_performance_report()
    
    def execute_trade(self, signal, market_data):
        """Execute simulated trade with slippage and commissions"""
        price = market_data['close'] * (1 + np.random.normal(0, 0.001))  # Slippage
        commission = max(1.0, price * 0.001)  # $1 or 0.1%
        
        trade_value = self.portfolio['cash'] * 0.1  # 10% allocation
        shares = int((trade_value - commission) / price)
        
        self.portfolio['cash'] -= trade_value
        self.portfolio['positions'][self.strategy.symbol] = {
            'shares': shares * signal,
            'entry_price': price,
            'timestamp': market_data.name
        }
        self.trades.append({
            'timestamp': market_data.name,
            'signal': signal,
            'price': price,
            'shares': shares,
            'commission': commission
        })

    def generate_performance_report(self):
        """Calculate performance metrics"""
        final_value = self.portfolio['cash'] + self.get_position_value()
        total_return = (final_value - self.capital) / self.capital
        sharpe_ratio = self.calculate_sharpe_ratio()
        max_drawdown = self.calculate_max_drawdown()
        
        return {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'num_trades': len(self.trades),
            'win_rate': self.calculate_win_rate()
        }
```

### 4. Risk Management Controls
- **Portfolio-level exposure limits** — max 50% sector exposure, 10% single asset
- **Stop-loss enforcement** — hard stops at 3-5% below entry
- **Drawdown limits** — auto-pause trading if daily loss exceeds 2%
- **Position sizing models** — Kelly Criterion, fixed fractional, volatility targeting
- **Correlation analysis** — avoid simultaneous losses across correlated assets

## Key Performance Metrics
| Metric | Formula | Target |
|--------|---------|--------|
| Sharpe Ratio | (Return - Risk-free) / Std Dev | >1.0 |
| Sortino Ratio | (Return - Risk-free) / Downside Deviation | >2.0 |
| Max Drawdown | Peak to trough decline | <15% |
| Calmar Ratio | Annual Return / Max Drawdown | >2.0 |
| Win Rate | Winners / Total Trades | >50% |
| Profit Factor | Gross Profit / Gross Loss | >1.5 |

## Execution Optimization
1. **VWAP execution** — split large orders across time to minimize market impact
2. **Iceberg orders** — show only small portion to hide true order size
3. **TWAP algorithms** — time-weighted average price for passive execution
4. **POV (Percentage of Volume)** — execute as % of market volume
5. **Implementation shortfall** — measure difference between expected and actual price

## Common Pitfalls
1. **Look-ahead bias** — using future data in backtests (e.g., today's close at 9 AM)
2. **Survivorship bias** — only backtesting assets that survived (delisted stocks excluded)
3. **Overfitting** — strategy works only on historical data, fails live
4. **Ignoring transaction costs** — commissions + slippage eat profitability
5. **No out-of-sample testing** — validating on same data used for optimization
6. **Ignoring market regime changes** — strategy that worked in 2020 may fail in 2022
7. **Not stress-testing** — strategies should survive market crashes
8. **Emotional intervention** — manually overriding automated systems breaks edge

## Verification Checklist
- [ ] Backtest on out-of-sample data (20% holdout)
- [ ] Walk-forward optimization applied
- [ ] Transaction costs included in backtest
- [ ] Slippage modeled realistically
- [ ] Strategy survives 2020 crash scenario
- [ ] Position sizing and risk controls tested
- [ ] No look-ahead or survivorship bias detected
- [ ] Sharpe ratio > 1.0 on full backtest period
- [ ] Max drawdown < 15% in stress scenarios
- [ ] Execution algorithm tested with paper trading