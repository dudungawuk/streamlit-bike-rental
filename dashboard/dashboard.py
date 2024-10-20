import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "../data/hour.csv")
df_hour = pd.read_csv(file_path)
df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])

with st.sidebar:
    st.title("Filter")

    start_date = st.date_input(
        label="Start date:",
        value=df_hour["dteday"].min(),
        min_value=df_hour["dteday"].min(),
        max_value=df_hour["dteday"].max()
    )

    end_date = st.date_input(
        label="End date:",
        value=df_hour["dteday"].max(),
        min_value=df_hour["dteday"].min(),
        max_value=df_hour["dteday"].max()
    )

    df_filtered = df_hour[(df_hour["dteday"] >= pd.to_datetime(start_date)) & (df_hour["dteday"] <= pd.to_datetime(end_date))]

    user_type = st.radio("Select User Type:", ('All User', 'Registered', 'Casual'))

    if user_type == 'All User':
        df_filtered["user_type"] = df_filtered['cnt']
    elif user_type == 'Registered':
        df_filtered["user_type"] = df_filtered['registered']
    else:
        df_filtered["user_type"] = df_filtered['casual']

    workingday_type = st.radio("Select Day Type:", ("All Day","Workingday", "No Workingday"))

    if workingday_type == "Workingday":
        df_filtered = df_filtered[df_filtered["workingday"] == 1]
    elif workingday_type == "No Workingday":
        df_filtered = df_filtered[df_filtered["workingday"] == 0]
    else:
        pass

st.header("Bike Sharing Visualization")

st.subheader(f"Jumlah Pengguna Sepeda Berdasarkan Jenis Pengguna ({user_type})")
st.line_chart(df_filtered, x="dteday", y="user_type")

st.markdown(f"Data di atas menunjukkan penggunaan jumlah sepeda dari pengguna **{user_type}** di **{workingday_type}** dari tanggal **{start_date}** sampai tanggal **{end_date}**.")

st.subheader("Pie Chart Klasifikasi Pengguna berdasarkan jumlah penggunaan sepeda")

total_registered = df_filtered["registered"].sum()
total_casual = df_filtered["casual"].sum()

labels = ['Registered', 'Casual']
sizes = [total_registered, total_casual]
explode = (0.05, 0.05)

fig1, ax1 = plt.subplots(figsize=(6, 6))
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')
st.pyplot(fig1)
st.markdown(f"Data di atas menunjukkan perbandingan penggunaan jumlah sepeda oleh pengguna **registered** dan **casual** di **{workingday_type}** dari tanggal **{start_date}** sampai tanggal **{end_date}**.")
