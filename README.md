# 📊 Vendor Performance Data Analytics (End-to-End Project)

## 🚀 Overview

This project delivers a complete **end-to-end data analytics solution** for analyzing vendor performance in the retail liquor industry.

It transforms raw transactional data into actionable business insights using **SQL, Python, and Power BI**.

---

## 🧰 Tech Stack

* **Python** (Pandas, SQLAlchemy)
* **MySQL**
* **Power BI**
* **Jupyter Notebook**
* **Statistics (Hypothesis Testing, Confidence Intervals)**

---

## 📂 Project Structure

```
├── data/                          # Raw CSV files
├── logs/                          # Pipeline logs
├── ingestion_db.py                # Data ingestion script
├── get_vendor_summary.py          # ETL + KPI creation
├── ExploratoryDataAnalysis.ipynb  # EDA notebook
├── VendorPerformanceDataAnalysis.ipynb  # Analysis + stats
├── Vendor_sales_summary.csv       # Final dataset
├── VendorPerformanceDashboard.pbix # Power BI dashboard
├── Vendor_Performance_Report.pdf  # Final report
```

---

## ⚙️ Project Pipeline

### 1️⃣ Data Ingestion

* Loaded 6 CSV files (~15M records) into MySQL
* Automated using Python scripts
* Logging implemented for tracking

### 2️⃣ Data Transformation (ETL)

* Built using SQL (CTEs)
* Created `vendor_sales_summary` table
* Engineered KPIs:

  * Gross Profit
  * Profit Margin
  * Stock Turnover
  * Sales-to-Purchase Ratio

### 3️⃣ Exploratory Data Analysis

* Identified outliers and missing values
* Correlation analysis
* Vendor-level deep dives

### 4️⃣ Statistical Analysis

* Confidence Intervals (95%)
* Welch’s t-test for profit margin comparison

### 5️⃣ Visualization

* Interactive Power BI dashboard
* KPI cards, charts, and filters for business insights

---

## 📊 Dashboard Preview
<img width="1110" height="673" alt="image" src="https://github.com/user-attachments/assets/c54b08f1-5e9c-4c0a-9ed0-add7901cacfa" />



---

## 📈 Key Insights

* 💰 **$441M total sales** and **$134M gross profit**
* 🏆 Top 10 vendors contribute **~65.7% of total purchases**
* 📦 **$2.71M capital locked** in unsold inventory
* 📉 Bulk purchasing reduces unit cost by **~72%**
* 📊 Low-volume vendors have **higher profit margins (~41%)**

---

## 💡 Business Recommendations

* Strengthen relationships with top vendors
* Promote high-margin low-volume products
* Optimize bulk purchasing strategies
* Reduce slow-moving inventory
* Diversify vendor base to reduce risk

---

## 📊 Key Metrics

| Metric           | Value    |
| ---------------- | -------- |
| Total Sales      | $441.41M |
| Total Purchase   | $307.34M |
| Gross Profit     | $134.07M |
| Profit Margin    | 38.72%   |
| Unsold Inventory | $2.71M   |

---

## 🧠 What I Learned

* Building **end-to-end ETL pipelines**
* Writing **advanced SQL (CTEs, joins)**
* Performing **statistical analysis**
* Creating **business-focused dashboards**
* Translating data into **actionable insights**

---

## 📌 How to Run

1. Clone the repository
2. Place CSV files in `/data` folder
3. Run:

```bash
python ingestion_db.py
python get_vendor_summary.py
```

4. Open Power BI dashboard

---

## 👤 Author

**Anish Basnet**
Data Analytics Enthusiast

---

## ⭐ If you like this project

Give it a star ⭐ and feel free to connect!
