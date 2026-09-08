import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Beijing Air Quality Dashboard",
    page_icon="🌫️",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'main_data.csv')
    df = pd.read_csv(csv_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

df = load_data()

# Title
st.title("🌫️ Beijing Air Quality Dashboard")
st.markdown("Analisis Kualitas Udara di Beijing (2013-2017)")

# Sidebar filters
st.sidebar.header("Filter Data")

# Date range filter
min_date = df['datetime'].min().date()
max_date = df['datetime'].max().date()
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Station filter with an explicit "All Stations" option
station_options = sorted(df['station'].unique())
station_choices = ["All Stations"] + station_options
selected_stations = st.sidebar.multiselect(
    "Pilih Stasiun",
    options=station_choices,
    default=["All Stations"]
)
if not selected_stations or "All Stations" in selected_stations:
    selected_stations = station_options

# Filter data
filtered_df = df[
    (df['datetime'].dt.date >= start_date) &
    (df['datetime'].dt.date <= end_date) &
    (df['station'].isin(selected_stations))
]

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_pm25 = filtered_df['PM2.5'].mean()
    st.metric("Rata-rata PM2.5", f"{avg_pm25:.1f} ug/m3")

with col2:
    avg_pm10 = filtered_df['PM10'].mean()
    st.metric("Rata-rata PM10", f"{avg_pm10:.1f} ug/m3")

with col3:
    avg_temp = filtered_df['TEMP'].mean()
    st.metric("Rata-rata Suhu", f"{avg_temp:.1f}°C")

with col4:
    avg_o3 = filtered_df['O3'].mean()
    st.metric("Rata-rata O3", f"{avg_o3:.1f} ug/m3")

st.divider()

# Warna netral seragam untuk semua bar; warna aksen hanya dipakai untuk
# menyorot kategori dengan nilai tertinggi (petunjuk informasi, bukan dekorasi)
NEUTRAL_COLOR = "#95a5a6"
HIGHLIGHT_COLOR = "#e74c3c"

# Section 1: PM2.5 Trend
st.header("📈 Tren PM2.5 Bulanan")

monthly_trend = filtered_df.groupby(pd.Grouper(key='datetime', freq='MS'))['PM2.5'].mean().reset_index()

fig_trend = px.line(
    monthly_trend,
    x='datetime',
    y='PM2.5',
    title='Rata-rata PM2.5 per Bulan pada Rentang Tanggal Terpilih',
    markers=True,
    labels={'PM2.5': 'Rata-rata PM2.5 (ug/m3)', 'datetime': 'Bulan'}
)
fig_trend.update_traces(line_color=HIGHLIGHT_COLOR, line_width=3)
st.plotly_chart(fig_trend, use_container_width=True)

# Section 2: Station Comparison
st.header("🏙️ Perbandingan PM2.5 antar Stasiun")

station_avg = filtered_df.groupby('station')['PM2.5'].mean().sort_values(ascending=True).reset_index()
station_bar_colors = [
    HIGHLIGHT_COLOR if v == station_avg['PM2.5'].max() else NEUTRAL_COLOR
    for v in station_avg['PM2.5']
]

fig_station = px.bar(
    station_avg,
    x='PM2.5',
    y='station',
    orientation='h',
    title='Rata-rata PM2.5 per Stasiun (merah = tertinggi)',
    labels={'PM2.5': 'Rata-rata PM2.5 (ug/m3)', 'station': 'Stasiun'}
)
fig_station.update_traces(marker_color=station_bar_colors)
st.plotly_chart(fig_station, use_container_width=True)

# Section 3: Seasonal Pattern
st.header("🗓️ Pola Musiman PM2.5")

monthly_pattern = filtered_df.groupby('month')['PM2.5'].mean().reset_index()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
monthly_pattern['month_name'] = monthly_pattern['month'].apply(lambda x: month_names[x-1])
monthly_bar_colors = [
    HIGHLIGHT_COLOR if v == monthly_pattern['PM2.5'].max() else NEUTRAL_COLOR
    for v in monthly_pattern['PM2.5']
]

fig_monthly = px.bar(
    monthly_pattern,
    x='month_name',
    y='PM2.5',
    title='Rata-rata PM2.5 per Bulan (merah = tertinggi)',
    labels={'PM2.5': 'Rata-rata PM2.5 (ug/m3)', 'month_name': 'Bulan'}
)
fig_monthly.update_traces(marker_color=monthly_bar_colors)
st.plotly_chart(fig_monthly, use_container_width=True)

# Section 4: Weekday vs Weekend
st.header("📅 Perbandingan Weekday vs Weekend")

st.subheader("Stasiun Dongsi (2015-2016)")
dongsi_data = filtered_df[
    (filtered_df['station'] == 'Dongsi') & 
    (filtered_df['year'].isin([2015, 2016]))
]

if len(dongsi_data) > 0:
    weekday_avg = dongsi_data[dongsi_data['is_weekend'] == False]['PM2.5'].mean()
    weekend_avg = dongsi_data[dongsi_data['is_weekend'] == True]['PM2.5'].mean()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Weekday PM2.5", f"{weekday_avg:.2f} ug/m3")
    with col2:
        st.metric("Weekend PM2.5", f"{weekend_avg:.2f} ug/m3")
    
    # Hourly comparison
    hourly_comp = dongsi_data.groupby(['hour', 'is_weekend'])['PM2.5'].mean().unstack()
    
    fig_hourly = go.Figure()
    fig_hourly.add_trace(go.Scatter(
        x=hourly_comp.index, 
        y=hourly_comp[False],
        name='Weekday',
        line=dict(color='#3498db', width=3),
        mode='lines+markers'
    ))
    fig_hourly.add_trace(go.Scatter(
        x=hourly_comp.index, 
        y=hourly_comp[True],
        name='Weekend',
        line=dict(color='#e74c3c', width=3),
        mode='lines+markers'
    ))
    
    fig_hourly.update_layout(
        title='Pola PM2.5 per Jam: Weekday vs Weekend',
        xaxis_title='Jam',
        yaxis_title='PM2.5 (ug/m3)',
        xaxis=dict(dtick=1)
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

# Section 5: Clustering
st.header("🎯 Clustering Stasiun (Manual Grouping)")

station_stats = filtered_df.groupby('station').agg({
    'PM2.5': 'mean',
    'PM10': 'mean',
    'TEMP': 'mean'
}).reset_index()

def categorize_pm25(value):
    if value <= 12:
        return 'Baik'
    elif value <= 35.4:
        return 'Sedang'
    elif value <= 55.4:
        return 'Tidak Sehat untuk Sensitif'
    elif value <= 150.4:
        return 'Tidak Sehat'
    else:
        return 'Sangat Tidak Sehat'

station_stats['category'] = station_stats['PM2.5'].apply(categorize_pm25)

fig_cluster = px.scatter(
    station_stats,
    x='PM10',
    y='PM2.5',
    color='category',
    size='TEMP',
    hover_name='station',
    title='Clustering Stasiun Berdasarkan PM2.5 dan PM10',
    labels={
        'PM2.5': 'PM2.5 (ug/m3)', 
        'PM10': 'PM10 (ug/m3)',
        'TEMP': 'Suhu (°C)'
    },
    color_discrete_map={
        'Baik': '#00e400',
        'Sedang': '#ffff00',
        'Tidak Sehat untuk Sensitif': '#ff7e00',
        'Tidak Sehat': '#ff0000',
        'Sangat Tidak Sehat': '#8f3f97'
    }
)
st.plotly_chart(fig_cluster, use_container_width=True)

# Display clustering table
st.subheader("Detail Clustering Stasiun")
st.dataframe(
    station_stats[['station', 'PM2.5', 'PM10', 'category']].sort_values('PM2.5', ascending=False),
    use_container_width=True
)

# Footer
st.divider()
st.markdown("""
**Kualitas Udara berdasarkan Standar WHO (PM2.5):**
- 🟢 **Baik:** 0-12 ug/m3
- 🟡 **Sedang:** 12.1-35.4 ug/m3
- 🟠 **Tidak Sehat untuk Sensitif:** 35.5-55.4 ug/m3
- 🔴 **Tidak Sehat:** 55.5-150.4 ug/m3
- 🟣 **Sangat Tidak Sehat:** >150.5 ug/m3
""")
