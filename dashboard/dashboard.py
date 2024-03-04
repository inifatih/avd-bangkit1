# import library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

order_reviews_df = pd.read_csv("order_reviews.csv")
order_payments_df = pd.read_csv("order_payments.csv")
rfm_df = pd.read_csv("rfm_df.csv")
rfm_merged_df = pd.read_csv("rfm_merged_df.csv")

st.title("Analisis dan Visualisasi Data E-Commerce :star:")

# Review Score dan Review Comment
st.subheader("The Number of Customer Review")
 
col1, col2 = st.columns(2)

with col1:
    # graph visualisasi
    review_score_counts = order_reviews_df.review_score.value_counts().reset_index()
    review_score_counts.columns = ['Review Index', 'Review Scores']

    fig, ax = plt.subplots(figsize=(6, 5))

    sns.barplot(
        y="Review Scores",
        x="Review Index",
        data=review_score_counts,
        palette="deep",
        ax=ax
    )
    ax.set_title("Based On Score Given", loc="center", fontsize="20")
    ax.set_ylabel("Total Score Given")
    ax.set_xlabel("Score")
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=15)
    st.pyplot(fig)

with col2:
    # graph visualisasi
    review_comment_counts = order_reviews_df.groupby(by="review_score").review_comment_message.nunique().sort_values(ascending=False).reset_index()
    review_comment_counts.columns = ['Review Index', 'Review Comments']

    fig, ax = plt.subplots(figsize=(6, 5))

    sns.barplot(
        y="Review Comments",
        x="Review Index",
        data=review_comment_counts,
        palette='deep',
        ax=ax
    )
    ax.set_title("Based On Comment Given", loc="center", fontsize="20")
    ax.set_ylabel("Total Comment Given")
    ax.set_xlabel("Score")
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=15)
    st.pyplot(fig)

# Visualisasi Bar Chart
st.subheader("Correlation Between Score and Comment")

fig, ax = plt.subplots(figsize=(6,5))
ax.scatter(x=review_score_counts, y=review_comment_counts, color='blue', alpha=0.5)

ax.set_xlabel('Review Score')
ax.set_ylabel('Review Comment')
ax.set_title('Correlation Between Score and Comment Given by Customers')
st.pyplot(fig)




# Tipe Pembayaran
st.subheader("Order Payments")
payment_counts = order_payments_df.groupby(by="payment_type").order_id.nunique().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(6,5))
colors = ['olive', 'green', 'tomato', 'orange', 'maroon']
ax.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', startangle=140, colors=colors)
ax.set_title('Distribution of Payment Type')
st.pyplot(fig)




# Total order setiap bulan
st.subheader("Order Trends Every Month")
# Mencari tren dari total order pada setiap bulan
rfm_df['order_purchase_timestamp'] = pd.to_datetime(rfm_df['order_purchase_timestamp'])

rfm_df['month'] = rfm_df['order_purchase_timestamp'].dt.to_period('M')

monthly_orders = rfm_df.groupby('month').size()

# Visualisasi
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(monthly_orders.index.astype(str), monthly_orders.values, marker='o', linestyle='-')
ax.set_title("Monthly Total Orders")
ax.set_xlabel('Month')
ax.set_ylabel('Number of Orders')
ax.tick_params(axis='x', rotation=45)
ax.grid(True)
plt.tight_layout()
st.pyplot(fig)



# Analisis RFM
st.subheader("Customer Segmentation Based on RFM Analysis")
n_clusters = 3

# Visualisasi
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for cluster in range(n_clusters):
    cluster_data = rfm_merged_df[rfm_merged_df['cluster'] == cluster]
    ax.scatter(cluster_data['recency'], cluster_data['frequency'], cluster_data['monetary'], alpha=0.5, label=f'Cluster {cluster + 1}')

ax.set_xlabel('Recency')
ax.set_ylabel('Frequency')
ax.set_zlabel('Monetary')
plt.title('RFM Clustering with K-Means - 3D Scatter Plot')
plt.legend()
st.pyplot(fig)