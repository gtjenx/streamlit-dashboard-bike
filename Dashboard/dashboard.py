import streamlit as st
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
sns.set(style='whitegrid')

# Load data
file_path_day = os.path.join(os.path.dirname(__file__), "day_data.csv")
file_path_hour = os.path.join(os.path.dirname(__file__), "hour_data.csv")

day_data = pd.read_csv(file_path_day)
hour_data = pd.read_csv(file_path_hour)

# Convert date columns
day_data['dteday'] = pd.to_datetime(day_data['dteday'])
hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])

# Sidebar
st.sidebar.title("🚲 Bike Data")
min_date, max_date = day_data['dteday'].min(), day_data['dteday'].max()
start_date, end_date = st.sidebar.date_input("Pilih Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter data
filtered_day_data = day_data[(day_data['dteday'] >= pd.to_datetime(start_date)) & (day_data['dteday'] <= pd.to_datetime(end_date))]

# Header
st.title("🚴‍♂️ Bike Rental Dashboard")
st.markdown("### Visualisasi Data Penyewaan Sepeda")

# Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Penyewaan", value=f"{filtered_day_data['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Penyewaan Harian", value=f"{filtered_day_data['cnt'].mean():,.1f}")

# Line Chart - Tren Penyewaan Harian
st.subheader("📈 Tren Penyewaan Sepeda Harian")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(filtered_day_data['dteday'], filtered_day_data['cnt'], marker='o', color='#FF6F61')
ax.set_title("Tren Penyewaan Sepeda Harian")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.grid(False) 
st.pyplot(fig)

# Line Chart - Pola Penyewaan Per Jam
st.subheader("⏰ Pola Penyewaan Sepeda Per Jam")
hourly_trend = hour_data.groupby('hr')['cnt'].mean().reset_index()
max_hour = hourly_trend.loc[hourly_trend['cnt'].idxmax()]
min_hour = hourly_trend.loc[hourly_trend['cnt'].idxmin()]

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=hourly_trend, x='hr', y='cnt', marker='o', color='b', linewidth=2)
ax.axvline(max_hour['hr'], color='r', linestyle='--', label=f"Penyewaan Tertinggi: {int(max_hour['hr'])}")
ax.axvline(min_hour['hr'], color='g', linestyle='--', label=f"Penyewaan Terendah: {int(min_hour['hr'])}")
plt.scatter(max_hour['hr'], max_hour['cnt'], color='r', s=100, label="Tertinggi", edgecolors="black")
plt.scatter(min_hour['hr'], min_hour['cnt'], color='g', s=100, label="Terendah", edgecolors="black")
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
ax.legend()
ax.grid(False) 
st.pyplot(fig)

# Pie Chart - Proporsi Penyewaan Berdasarkan Musim
st.subheader("🍂 Proporsi Penyewaan Berdasarkan Musim")
season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
filtered_day_data['season_label'] = filtered_day_data['season'].map(season_mapping)
season_trend = filtered_day_data.groupby('season_label')['cnt'].sum().reset_index()

max_season = season_trend.loc[season_trend['cnt'].idxmax(), 'season_label']
colors = ['#F4A3C2' if s == max_season else '#D3D3D3' for s in season_trend['season_label']]
explode = [0.1 if s == max_season else 0 for s in season_trend['season_label']]

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(season_trend['cnt'], labels=season_trend['season_label'], autopct="%1.1f%%", colors=colors, startangle=140, explode=explode)
ax.set_title("Proporsi Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

# Grafik Penyewaan Berdasarkan Cuaca
st.subheader("\U0001F326 Pengaruh Cuaca terhadap Pengguna Terdaftar vs. Kasual")
weather_trend = filtered_day_data.groupby('weathersit')[['casual', 'registered']].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
weather_trend.set_index("weathersit").plot(kind="bar", stacked=False, colormap="Paired", ax=ax)
ax.set_title("Pengaruh Cuaca terhadap Pengguna Terdaftar vs. Kasual", fontsize=14)
ax.set_xlabel("Kondisi Cuaca", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(["Casual", "Registered"])
for container in ax.containers:
    ax.bar_label(container, fmt="%.0f", label_type="edge", fontsize=10, padding=3)
st.pyplot(fig)

st.caption("Pedal your worries away! 🚴‍♀️✨")
