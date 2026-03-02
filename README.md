# RSI MACD Trading Bot

An algorithmic trading bot built using Python that generates buy and sell signals based on two popular technical indicators: Relative Strength Index (RSI) and Moving Average Convergence Divergence (MACD).

This project demonstrates algorithmic trading strategy development, financial data analysis, and automation using Python.

---

## Overview

The bot analyzes historical price data and applies RSI and MACD indicators to identify potential trading opportunities. It helps traders make data-driven decisions by automatically detecting buy and sell signals.

---

## Features

- RSI indicator calculation
- MACD indicator calculation
- Automated buy/sell signal generation
- Historical data analysis
- Modular and reusable code
- Easy to extend with new strategies

---

## Tech Stack

- Python
- Pandas
- NumPy
- Financial Data Analysis

---

## Indicators Used

### RSI (Relative Strength Index)

- Measures momentum
- Range: 0–100
- Signal conditions:
  - RSI < 30 → Oversold → Buy Signal
  - RSI > 70 → Overbought → Sell Signal

### MACD (Moving Average Convergence Divergence)

- Trend-following indicator
- Uses:
  - MACD Line
  - Signal Line

Signal conditions:
- MACD crosses above Signal Line → Buy
- MACD crosses below Signal Line → Sell

---
