import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Price Comparison",
    layout="wide"
)

st.title("🛒 Smart Price Comparison & Deal Recommendation System")

# LOAD DATA 
df = pd.read_csv("data/final_deals.csv")

# SIDEBAR FILTERS
st.sidebar.header("🔎 Filters")

# Function to shorten category name
def short_category(cat):
    if "|" in cat:
        return cat.split("|")[-1]
    return cat

df["short_category"] = df["category"].apply(short_category)

categories = ["All"] + sorted(df["short_category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

max_price = int(df["final_price"].max())
budget = st.sidebar.slider(
    "Select Budget (₹)",
    min_value=0,
    max_value=max_price,
    value=max_price
)

# Apply filters
filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["short_category"] == selected_category]

filtered_df = filtered_df[filtered_df["final_price"] <= budget]
filtered_df = filtered_df.sort_values(by="final_score", ascending=False)

# BEST DEAL 
st.subheader("🏆 Best Deal Recommendation")

if not filtered_df.empty:
    best = filtered_df.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Price", f"₹{int(best.final_price)}")
    col2.metric("⭐ Rating", best.rating)
    col3.metric("🔥 Discount", f"{int(best.discount_percentage)}%")
    col4.metric("📌 Decision", best.decision)

    if best.alert:
        st.warning(best.alert)

    st.success(
        f"**{best.product_name}**\n\n"
        f"Decision: **{best.decision}**\n\n"
        f"Reason: Balanced price, rating, discount, and trust score."
    )

    st.markdown(f"[🔗 View Product]({best.product_link})")

else:
    st.warning("No products match the selected filters.")

#TABLE
st.subheader("📋 Deal Comparison Table")

st.dataframe(
    filtered_df[
        [
            "product_name",
            "category",
            "final_price",
            "rating",
            "discount_percentage",
            "final_score",
            "decision",
            "alert"
        ]
    ].head(30),
    use_container_width=True
)

#PRICE TREND CHART
st.subheader("📈 Price Trend Analysis")

if not filtered_df.empty:
    trend_df = filtered_df.head(20).copy()
    trend_df = trend_df.reset_index(drop=True)
    trend_df["Rank"] = trend_df.index + 1

    st.line_chart(
        data=trend_df.set_index("Rank")["final_price"]
    )

    st.caption(
        "Price trend across top-ranked products. "
        "Lower and stable prices indicate better value."
    )
else:
    st.info("No data available for trend analysis.")
