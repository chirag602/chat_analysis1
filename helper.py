# helper.py
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_stats(selected_line, df):
    """
    Fetches statistics for the selected line or overall chat.
    """
    if df is None or df.empty:
        return 0
    if selected_line == "Overall":
        return df.shape[0]
    else:
        return df[df["Line"] == selected_line].shape[0]

def generate_analysis(df, st):
    """
    Generates and displays analysis of the chat data.
    """
    if df is None or df.empty:
        st.error("❌ Error: No data available for analysis. Please check the uploaded file.")
        return

    try:
        st.subheader("📊 Overall Chat Analysis")

        # Unique Users
        if "User" in df.columns:
            unique_users = df["User"].nunique()
            st.header(f"👥 Unique Users: {unique_users}")
        else:
            st.header("👥 Unique Users: N/A")

        # Total Words
        if "Message" in df.columns:
            total_words = df["Message"].str.split().str.len().sum()
            st.header(f"📚 Total Words: {total_words}")
        else:
            st.header("📚 Total Words: N/A")

        # Media Shared
        if "Message" in df.columns:
            media_count = df["Message"].str.contains("<Media omitted>", na=False).sum()
            st.header(f"🖼️ Media Shared: {media_count}")
        else:
            st.header("🖼️ Media Shared: N/A")

        # Most Active Users
        if "User" in df.columns:
            st.subheader("📈 Most Active Users")
            user_counts = df["User"].value_counts()
            st.dataframe(user_counts.rename("Message Count"))

            # Bar Chart for Most Active Users
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=user_counts.index, y=user_counts.values, ax=ax)
            plt.xticks(rotation=90)
            plt.xlabel("Users")
            plt.ylabel("Message Count")  # Ensure this line is properly indented
            plt.title("Messages Sent by Each User")
            st.pyplot(fig)

        # Individual User Analysis
        if "User" in df.columns:
            selected_user = st.sidebar.selectbox(
                "🔍 Select User for Detailed Analysis", ["Overall"] + list(df["User"].unique())
            )
            if selected_user != "Overall":
                user_df = df[df["User"] == selected_user]
                if user_df.empty:
                    st.error(f"❌ Error: No data available for user '{selected_user}'.")
                    return

                st.subheader(f"📋 Analysis for User: {selected_user}")
                st.markdown(f"**Total Messages:** {user_df.shape[0]}")
                if "Message" in user_df.columns:
                    st.markdown(f"**Total Words:** {user_df['Message'].str.split().str.len().sum()}")
                    st.markdown(f"**Media Shared:** {user_df['Message'].str.contains('<Media omitted>', na=False).sum()}")

        # Word Cloud
        if "Message" in df.columns:
            st.subheader("☁️ Word Cloud")
            words = " ".join(df["Message"])
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(words)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)

        # Message Trends Over Time
        if "Date" in df.columns:
            st.subheader("📅 Message Trends Over Time")
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            daily_messages = df.groupby(df["Date"].dt.date).size()

            fig, ax = plt.subplots()
            ax.plot(daily_messages.index, daily_messages.values, marker='o', linestyle='-')
            plt.xticks(rotation=45)
            plt.xlabel("Date")
            plt.ylabel("Message Count")  # Ensure this line is properly indented
            plt.title("Daily Message Trends")
            st.pyplot(fig)

    except Exception as e:
        # Properly aligned `except` block
        st.error(f"❌ Error during analysis: {e}")