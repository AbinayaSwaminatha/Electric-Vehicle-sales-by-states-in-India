import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Abinaya\Downloads\archive (2).zip")
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()
    df = df.rename(columns={"ev_sales_quantity": "sales"})
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    df = df[df['sales'] > 0]
    return df
df = load_data()

# Sidebar filters
st.sidebar.title("🔍 Filter EV Sales Data")
years = sorted(df['year'].dropna().unique())
states = sorted(df['state'].dropna().unique())
vehicle_types = sorted(df['vehicle_type'].dropna().unique())

selected_years = st.sidebar.multiselect("Select Year(s)", years, default=years)
selected_states = st.sidebar.multiselect("Select State(s)", states, default=states)
selected_types = st.sidebar.multiselect("Select Vehicle Type(s)", vehicle_types, default=vehicle_types)

# Filtered data
filtered_df = df[
    df['year'].isin(selected_years) &
    df['state'].isin(selected_states) &
    df['vehicle_type'].isin(selected_types)
]

# Title
st.title("🚗 Electric Vehicle Sales in India")
st.markdown("Explore EV sales trends across Indian states with interactive filters and visualizations.")

# KPIs
total_sales = int(filtered_df['sales'].sum())
top_state = filtered_df.groupby('state')['sales'].sum().idxmax()
top_type = filtered_df.groupby('vehicle_type')['sales'].sum().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("🔋 Total EV Sales", f"{total_sales:,}")
col2.metric("📍 Top State", top_state)
col3.metric("🚘 Top Vehicle Type", top_type)

# Sales by State
st.subheader("📍 EV Sales by State")
state_sales = filtered_df.groupby('state')['sales'].sum().reset_index().sort_values(by='sales', ascending=False)
fig_state = px.bar(state_sales, x='state', y='sales', color='sales', title='EV Sales by State')
st.plotly_chart(fig_state, use_container_width=True)

# Yearly Trend
st.subheader("📈 Yearly Sales Trend")
yearly_sales = filtered_df.groupby('year')['sales'].sum().reset_index()
fig_year = px.line(yearly_sales, x='year', y='sales', markers=True, title='EV Sales Over Time')
st.plotly_chart(fig_year, use_container_width=True)

# Vehicle Type Breakdown
st.subheader("🚙 Vehicle Type Distribution")
type_sales = filtered_df.groupby('vehicle_type')['sales'].sum().reset_index()
fig_type = px.pie(type_sales, names='vehicle_type', values='sales', title='EV Sales by Vehicle Type')
st.plotly_chart(fig_type, use_container_width=True)

# Monthly Trend
if 'month_name' in filtered_df.columns:
    st.subheader("📆 Monthly Sales Pattern")
    month_order = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    monthly_sales = filtered_df.groupby('month_name')['sales'].sum().reindex(month_order).reset_index()
    fig_month = px.bar(monthly_sales, x='month_name', y='sales', title='Monthly EV Sales')
    st.plotly_chart(fig_month, use_container_width=True)
