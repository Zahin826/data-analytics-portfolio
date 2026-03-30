# 📊 SaaS Business Performance Dashboard

## Project Overview
End-to-end dashboard project analyzing subscription business 
metrics for a simulated SaaS company (2021–2026). Built both 
a static multi-panel report and a fully interactive web dashboard.

---

## Business Questions Answered
- How is Monthly Recurring Revenue (MRR) trending?
- How fast is the customer base growing?
- What is the monthly churn rate?
- Which plan tier drives the most revenue?
- How do new customer acquisitions compare to churn?
- Which regions generate the most revenue?

---

## Tools & Libraries
- Python 3 — data generation & analysis
- Pandas + NumPy — data manipulation
- Matplotlib + Seaborn — static dashboard
- Plotly + Dash — interactive web dashboard
- Jupyter Notebook — development environment

---

## Project Structure
```
project-04-saas-dashboard/
│
├── data/                    # Generated datasets (not tracked by Git)
├── notebooks/
│   ├── 01_generate_data.ipynb       # Synthetic SaaS data generation
│   └── 02_static_dashboard.ipynb   # 6-panel static dashboard
├── dashboard/
│   └── app.py                       # Interactive Dash web app
├── images/                          # Saved dashboard screenshots
└── README.md
```

---

## Key Metrics (Simulated Business)
| Metric | Value |
|--------|-------|
| Latest MRR | $21,475 |
| Active Customers | 185 |
| Avg Monthly Churn | 7.2% |
| Total MRR Growth | 3,769% |
| Total Customers | 515 |

---

## Key Findings

### 💰 Finding 1 — Enterprise Drives Disproportionate Revenue
Enterprise customers are only 15% of the base but generate 
the highest revenue per customer ($299/month vs $29 for Basic).
Classic SaaS pattern — fewer enterprise customers, higher value.

### 📈 Finding 2 — Consistent Growth Trajectory
MRR grew from $555 to $21,475 over 48 months — a 3,769% increase.
Active customers grew steadily from 5 to 185.

### 🌍 Finding 3 — North America Dominates
North America generates $49,032 in total revenue — 3x more than 
Europe ($14,965) and 5x more than Asia Pacific ($9,414).

### 📉 Finding 4 — Churn Stabilizes Over Time
Early months show volatile churn (0-25%). By 2023 onwards,
churn stabilizes around the 7.2% monthly average.

---

## How To Run The Interactive Dashboard
1. Clone this repository
2. Install dependencies: `pip install pandas plotly dash`
3. Navigate to dashboard folder: `cd project-04-saas-dashboard/dashboard`
4. Run: `python app.py`
5. Open browser: `http://127.0.0.1:8050`