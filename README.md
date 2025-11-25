# 10 Academy – Week 1 Challenge
## Predicting Stock Price Movements Using Financial News Sentiment

This project analyzes a real-world financial news dataset to understand how **news sentiment affects stock price movements**.  
The challenge is part of **10 Academy’s Artificial Intelligence Mastery Program – Week 1**.

---

## 🚀 **Project Objectives**
1. Perform **Exploratory Data Analysis (EDA)** on financial news data.  
2. Conduct **sentiment analysis** on news headlines.  
3. Use **technical indicators** (RSI, MACD, MA) with **TA-Lib** and **PyNance**.  
4. Compute **daily stock returns** and align them with sentiment scores.  
5. Measure correlation between **sentiment** and **stock price movements**.  
6. Produce a final report with insights and recommendations.

---

## 📁 **Repository Structure**
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── unittests.yml
├── .gitignore
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
├── notebooks/
│   ├── __init__.py
│   └── README.md
├── tests/
│   ├── __init__.py
└── scripts/
    ├── __init__.py
    └── README.md

yaml
Copy code

---

## 🧰 **Technologies Used**
- **Python 3.10+**
- **Pandas, NumPy**
- **Matplotlib, Seaborn**
- **NLTK, TextBlob**
- **TA-Lib**
- **PyNance**
- **YFinance**
- **Jupyter Notebook**
- **Git + GitHub**

---

## 📊 **Task Descriptions**

### **🟦 Task 1 – Git, GitHub & EDA**
- Set up Git repository, branching strategy, and environment.
- Perform full EDA:
  - Descriptive statistics  
  - Time series analysis  
  - Publisher analysis  
  - Keyword extraction  

---

### 🔧 How to run this project (Local dev)

1. Create a virtual environment and activate it (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies from `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

3. Run unit tests:

```powershell
python -m pytest -q
```

4. Example: compute indicators for AAPL

```powershell
python -m scripts.compute_indicators --symbol AAPL
```

5. Example: compute sentiment vs returns correlation for a symbol

```powershell
python -m scripts.analyze_sentiment_returns --symbol AAPL --news data/raw_analyst_ratings.csv
```

### PyNance usage
PyNance functions and metrics can be used inside the analysis notebooks. To compute financial metrics beyond indicators, import `pynance` inside the notebooks or scripts and use it to compute metrics such as Sharpe ratio, annualized returns, and drawdowns for strategy backtests.

---
If you want, I can add a small notebook that demonstrates the entire pipeline from loading CSVs to indicators to computing correlation and plotting the results.
