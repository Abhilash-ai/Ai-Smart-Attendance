import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Attendance", layout="wide")

st.title("📊 Smart Attendance Dashboard")

file = "attendance.csv"

try:
    df = pd.read_csv(file)

    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df["In Time"] = pd.to_datetime(df["In Time"], errors='coerce')
    df["Out Time"] = pd.to_datetime(df["Out Time"], errors='coerce')

    # 📊 Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Records", len(df))
    col2.metric("Total Users", df["Name"].nunique())

    # 🔍 Filter
    users = df["Name"].unique()
    selected_user = st.selectbox("Select User", ["All"] + list(users))

    if selected_user != "All":
        df = df[df["Name"] == selected_user]

    st.subheader("📄 Attendance Records")
    st.dataframe(df, use_container_width=True)

    # 📈 Graph
    st.subheader("📈 Attendance Count")
    st.bar_chart(df["Name"].value_counts())

    # ⏱ Working hours
    df["Working Hours"] = (df["Out Time"] - df["In Time"]).dt.total_seconds() / 3600

    st.subheader("⏱ Working Hours")
    st.dataframe(df[["Name", "Date", "Working Hours"]], use_container_width=True)

except:
    st.warning("No attendance data found!")