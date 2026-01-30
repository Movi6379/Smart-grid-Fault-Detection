import streamlit as st
import pandas as pd
import plotly.express as px

# Set Page Config
st.set_page_config(page_title="Smart Grid Fault Dashboard", layout="wide")
st.title("⚡ Smart Grid Fault Analysis & Rectification")

# Load Data
@st.cache_data
def load_data():
    fault_df = pd.read_csv('fault_dataset.csv')
    asset_df = pd.read_csv('grid_asset_data.csv')
    return fault_df, asset_df

fault_df, asset_df = load_data()

# 1. FAULT AFFECTED AREA (SIDEBAR)
st.sidebar.header("Filter Affected Area")
line_selection = st.sidebar.selectbox("Select Distribution Line", fault_df['line'].dropna().unique())
substation_selection = st.sidebar.selectbox("Select Substation", asset_df['Substation_ID'].unique())

# Filter data based on selection
line_data = fault_df[fault_df['line'] == line_selection]
fault_type = line_data['fault'].iloc[0]

# 2. RECTIFICATION LOGIC
def get_rectification(f_type):
    rect_map = {
        '3psc': "Emergency Trip: Open Three-Phase Breaker. Check for insulation failure.",
        'spgf': "Ground Fault Detected: Isolate affected phase and check grounding transformer.",
        'Overload': "Load Shedding: Reduce non-critical load in SS_001 area.",
        'UnderVoltage': "Capacitor Bank Activation: Boost voltage at the substation level.",
        'no fault': "System Healthy"
    }
    return rect_map.get(f_type, "Standard Inspection Required")

# 3. DASHBOARD LAYOUT
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📍 Fault Location: {line_selection}")
    st.metric("Detected Fault Type", fault_type)
    st.info(f"**Recommended Rectification:** {get_rectification(fault_type)}")

with col2:
    st.subheader("Voltage Profile Analysis")
    fig = px.line(line_data, y=['Ua1', 'Ub1', 'Uc1'], title=f"3-Phase Voltage at {line_selection}")
    st.plotly_chart(fig)

# 4. ASSET MONITORING (FROM GRID_ASSET_DATA)
st.divider()
st.subheader("Substation Asset Health Monitor")
sub_data = asset_df[asset_df['Substation_ID'] == substation_selection]
fig_asset = px.bar(sub_data, x='Asset_ID', y='Voltage_V', color='Asset_Type', 
                   title=f"Voltage Stability across {substation_selection}")
st.plotly_chart(fig_asset)

# Display raw events
if st.checkbox("Show Recent Fault Events"):
    st.write(asset_df[['Timestamp', 'Substation_ID', 'Fault_Event', 'Asset_Type']].dropna())
