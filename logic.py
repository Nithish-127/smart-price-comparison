import pandas as pd

df = pd.read_csv("data/amazon.csv")


#CLEANING PRICES
def clean_price(x):
    if pd.isna(x):
        return None
    return float(
        str(x)
        .replace("₹", "")
        .replace(",", "")
        .strip()
    )

df["actual_price"] = df["actual_price"].apply(clean_price)
df["discounted_price"] = df["discounted_price"].apply(clean_price)

# HANDLE RATINGS
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")

# Fill missing ratings with average
df["rating"].fillna(df["rating"].mean(), inplace=True)
df["rating_count"].fillna(0, inplace=True)
# CLEAN DISCOUNT PERCENTAGE
def clean_discount(x):
    if pd.isna(x):
        return 0
    return float(
        str(x)
        .replace("%", "")
        .strip()
    )

df["discount_percentage"] = df["discount_percentage"].apply(clean_discount)


#CREATE FINAL PRICE
df["final_price"] = df["discounted_price"]

# BUSINESS FILTERS
# Remove poor quality products
df = df[df["rating"] >= 3.5]

# Remove products without price
df = df.dropna(subset=["final_price"])

# SELECT BUSINESS COLUMNS
business_df = df[
    [
        "product_name",
        "category",
        "final_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
        "product_link"
    ]
]

# Save cleaned data
business_df.to_csv("data/clean_data.csv", index=False)

print("✅ Data cleaned & business-ready dataset created")
print("Total products:", len(business_df))

#SCORING ENGINE


# Reload cleaned data
df = pd.read_csv("data/clean_data.csv")

# --- NORMALIZATION HELPERS ---
def normalize(series, inverse=False):
    """Normalize values between 0 and 1"""
    if inverse:
        return 1 - (series - series.min()) / (series.max() - series.min())
    return (series - series.min()) / (series.max() - series.min())

# --- BUSINESS WEIGHTS ---
WEIGHTS = {
    "price": 0.4,
    "rating": 0.3,
    "discount": 0.2,
    "trust": 0.1
}

# --- CREATE NORMALIZED SCORES ---
df["price_score"] = normalize(df["final_price"], inverse=True)   # lower price = better
df["rating_score"] = normalize(df["rating"])
df["discount_score"] = normalize(df["discount_percentage"])
df["trust_score"] = normalize(df["rating_count"])

# --- FINAL BUSINESS SCORE ---
df["final_score"] = (
    df["price_score"] * WEIGHTS["price"] +
    df["rating_score"] * WEIGHTS["rating"] +
    df["discount_score"] * WEIGHTS["discount"] +
    df["trust_score"] * WEIGHTS["trust"]
)

# --- SORT BY BEST DEAL ---
best_deals = df.sort_values(by="final_score", ascending=False)

# Save scored data
best_deals.to_csv("data/scored_deals.csv", index=False)

print("🏆 Scoring complete!")
print("Top 5 Best Deals:")
print(
    best_deals[
        ["product_name", "final_price", "rating", "discount_percentage", "final_score"]
    ].head(5)
)

# BUY / WAIT LOGIC


# Average price (benchmark)
avg_price = df["final_price"].mean()

def buy_wait_decision(row):
    if row["rating"] < 3.5:
        return "❌ AVOID"
    elif (
        row["discount_percentage"] >= 50
        and row["rating"] >= 4.0
        and row["final_price"] < avg_price
    ):
        return "🟢 BUY NOW"
    elif row["discount_percentage"] >= 20:
        return "🟡 WAIT"
    else:
        return "🟡 WAIT"

df["decision"] = df.apply(buy_wait_decision, axis=1)

#DEAL ALERTS


def generate_alert(row):
    if row["discount_percentage"] >= 70:
        return "🔥 Huge Discount Alert!"
    elif row["rating"] >= 4.5 and row["final_price"] < avg_price:
        return "⭐ Best Value Deal"
    elif row["rating"] < 3.5:
        return "⚠️ Low Quality Product"
    else:
        return ""

df["alert"] = df.apply(generate_alert, axis=1)

# Save final dataset
df.to_csv("data/final_deals.csv", index=False)

print("🚨 Buy/Wait logic & alerts generated")
