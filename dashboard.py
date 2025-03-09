import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
from datetime import datetime
sns.set(style='whitegrid')

# Load data
day_data = pd.read_csv("day_data.csv") 
hour_data = pd.read_csv("hour_data.csv")

# Convert date columns
day_data['dteday'] = pd.to_datetime(day_data['dteday'])
hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])

# Sidebar untuk filter waktu
st.sidebar.title("🚲 Bike Date")

min_date = day_data['dteday'].min()
max_date = day_data['dteday'].max()

start_date, end_date = st.sidebar.date_input("Pilih Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter data berdasarkan rentang waktu
filtered_day_data = day_data[(day_data['dteday'] >= pd.to_datetime(start_date)) & (day_data['dteday'] <= pd.to_datetime(end_date))]

# Header Dashboard
st.title("🚴‍♂️ Bike Rental Dashboard")
st.markdown("### Visualisasi Data Penyewaan Sepeda")
st.write("Dashboard ini menampilkan analisis penyewaan sepeda berdasarkan berbagai faktor seperti cuaca, musim, dan waktu dalam sehari.")

# Metrik utama
col1, col2 = st.columns(2)
with col1:
    total_rentals = filtered_day_data['cnt'].sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")
with col2:
    avg_rentals = round(filtered_day_data['cnt'].mean(), 1)
    st.metric("Rata-rata Penyewaan Harian", value=f"{avg_rentals:,}")

# Grafik Tren Penyewaan Harian
st.subheader("📈 Tren Penyewaan Sepeda Harian")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(filtered_day_data['dteday'], filtered_day_data['cnt'], marker='o', color='#FF6F61')
ax.set_title("Tren Penyewaan Sepeda Harian", fontsize=14, fontweight='bold')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.grid(False)  
st.pyplot(fig)

# Grafik Penyewaan Berdasarkan Musim
st.subheader("🍂 Penyewaan Sepeda Berdasarkan Musim")
season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
filtered_day_data['season_label'] = filtered_day_data['season'].map(season_mapping)
season_df = filtered_day_data.groupby('season_label')['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=season_df, x='season_label', y='cnt', palette='coolwarm', ax=ax)
ax.set_title("Jumlah Penyewaan Berdasarkan Musim", fontsize=14, fontweight='bold')
ax.set_xlabel("")
ax.set_ylabel("Jumlah Penyewaan")
ax.grid(False)  
st.pyplot(fig)

# Grafik Pola Penyewaan Harian
st.subheader("⏰ Pola Penyewaan Sepeda Per Jam")
hourly_df = hour_data.groupby('hr')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=hourly_df, x='hr', y='cnt', marker='o', color='#6A0572')
ax.set_title("Rata-rata Penyewaan Sepeda Per Jam", fontsize=14, fontweight='bold')
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
ax.grid(False)  
st.pyplot(fig)

st.caption("Pedal your worries away! 🚴‍♀️✨.")
