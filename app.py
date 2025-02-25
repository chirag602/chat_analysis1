import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# WhatsApp Chat Preprocessing Function
def preprocess(data):
    pattern = r'^\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}:\d{2}\s?[APM]*)\] (.*?): (.*)$'
    matches = re.findall(pattern, data, re.MULTILINE)

    if not matches:
        return pd.DataFrame(columns=["date", "time", "user", "message", "year", "month"])

    dates, times, users, messages = zip(*matches)

    df = pd.DataFrame({
        "date": pd.to_datetime(dates, format="%d/%m/%Y", errors="coerce"),
        "time": times,
        "user": users,
        "message": messages
    })

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()

    return df

# Streamlit App
st.title("📊 WhatsApp Chat Analysis")

uploaded_file = st.file_uploader("Upload WhatsApp Chat File (.txt)", type="txt")

if uploaded_file:
    chat_data = uploaded_file.getvalue().decode("utf-8")
    df = preprocess(chat_data)

    if df.empty:
        st.warning("⚠️ No valid chat data found! Please upload a valid chat file.")
    else:
        st.subheader("📌 Chat Overview")
        st.write(df.head())  # Show first few rows of the dataset

        # Display Key Stats
        total_messages = df.shape[0]
        total_words = df["message"].apply(lambda x: len(x.split())).sum()
        media_messages = df["message"].str.contains("Media omitted", case=False, na=False).sum()
        link_messages = df["message"].str.contains(r'http[s]?://|www\.', case=False, na=False).sum()

        st.markdown(f"""
        - **Total Processed Messages:** {total_messages}
        - **Total Words (excluding media messages):** {total_words}
        - **Total Media Shared:** {media_messages}
        - **Total Links Shared:** {link_messages}
        """)

        # Top Users Chart
        st.subheader("📊 Most Active Users")
        user_counts = df["user"].value_counts().head(10)
        fig, ax = plt.subplots()
        user_counts.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Top 10 Most Active Users")
        ax.set_ylabel("Message Count")
        st.pyplot(fig)

        # Word Cloud
        st.subheader("☁️ Word Cloud")
        text = " ".join(df["message"])
        if text.strip():
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.warning("⚠️ No words found in chat to generate a word cloud.")

        # Monthly Activity Chart
        st.subheader("📆 Monthly Activity")
        monthly_counts = df.groupby(["year", "month"]).size().reset_index(name="message_count")
        monthly_counts["month_year"] = monthly_counts["month"] + " " + monthly_counts["year"].astype(str)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(monthly_counts["month_year"], monthly_counts["message_count"], marker="o", color="orange", linestyle="-")
        ax.set_xticklabels(monthly_counts["month_year"], rotation=45)
        ax.set_title("Messages Sent Over Time")
        ax.set_ylabel("Message Count")
        ax.grid()
        st.pyplot(fig)

        st.success("✅ Chat Analysis Completed!")

# Instructions
st.sidebar.header("ℹ️ Instructions")
st.sidebar.write("""
1. Export your WhatsApp chat without media.
2. Upload the **.txt** file.
3. View **statistics, charts, and word clouds**!
""")

