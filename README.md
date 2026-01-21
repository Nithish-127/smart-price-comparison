# 🛒 Smart Price Comparison & Deal Recommendation System

## 📌 Project Overview
This project is an end-to-end **business decision support system** that analyzes real Amazon product data to recommend the **best deals** using business logic.

Instead of just showing prices, the system:
- Cleans raw e-commerce data
- Scores products using weighted business rules
- Provides **Buy / Wait / Avoid** decisions
- Displays insights through an interactive dashboard

This project is designed to demonstrate **Business Analyst, Data Analyst, and Product Analytics skills**.

---

## 🎯 Key Features
- ✅ Real Amazon Kaggle dataset
- ✅ Data cleaning & preprocessing (prices, ratings, discounts)
- ✅ Weighted scoring engine for deal ranking
- ✅ Buy / Wait / Avoid decision logic
- ✅ Deal alerts (Huge Discount, Best Value, Low Quality)
- ✅ Category & budget-based filtering
- ✅ Interactive Streamlit dashboard
- ✅ Price trend analysis for decision support

---

## 🧠 Business Logic Explained

### 🔢 Scoring Formula
Each product is evaluated using a weighted score:
Final Score =
(Price Score × 0.4) +
(Rating Score × 0.3) +
(Discount Score × 0.2) +
(Trust Score × 0.1)


### 🟢 Buy / Wait / Avoid Rules
- **BUY NOW** → Discount ≥ 50%, Rating ≥ 4.0, Price below average
- **WAIT** → Moderate discount or average pricing
- **AVOID** → Rating < 3.5

---

## 🛠️ Tech Stack
- Python
- Pandas
- Streamlit
- Matplotlib
- Kaggle Dataset
- Git & GitHub

---

###📂 Project Structure
Price_comparison/
├── data/
│ ├── raw_data.csv # Kaggle dataset (not pushed)
│ ├── clean_data.csv
│ ├── scored_deals.csv
│ └── final_deals.csv
├── app.py # Streamlit dashboard
├── logic.py # Business logic & scoring engine
├── .gitignore


---

## ▶️ How to Run the Project

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Nithish-127/smart-price-comparison.git
cd smart-price-comparison

2️⃣ Create & activate virtual environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run business logic
python logic.

5️⃣ Launch the dashboard
streamlit run app.py

📊 Output
Ranked list of best product deals
Buy / Wait / Avoid recommendations
Automated deal alerts
Interactive dashboard with filters and charts

💼 Use Cases
E-commerce deal recommendation
Business & pricing analysis
Decision-support systems
Portfolio project for analysts & freshers

📌 Author

Nithish Srinivasan
GitHub: https://github.com/Nithish-127


---

## ✅ NEXT IMPORTANT STEP (DON’T SKIP)

After pasting README:

```bash
git add README.md
git commit -m "Add professional README"
git push
