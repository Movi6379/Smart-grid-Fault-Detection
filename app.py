import streamlit as st
import pandas as pd
import plotly.express as px

# Set Page Config
st.set_page_config(page_title="Smart Grid Fault Dashboard", layout="wide")

st.title("⚡ Smart Grid Fault Analysis & Rectification")

# 1. ROBUST DATA LOADING
@st.cache_data
def load_data():
    try:
        # Loading your specific datasets
        f_df = pd.read_csv('fault_dataset.csv')
        a_df = pd.read_csv('grid_asset_data.csv')
        return f_df, a_df
    except FileNotFoundError as e:
        st.error(f"Missing Data File: {e}")
        return None, None

fault_df, asset_df = load_data()

# Only proceed if data loaded successfully
if fault_df is not None and asset_df is not None:
    
    # 2. SIDEBAR FILTERS
    st.sidebar.header("Filter Affected Area")
    
    # Ensure 'line' column exists
    if 'line' in fault_df.columns:
        line_list = fault_df['line'].dropna().unique()
        line_selection = st.sidebar.selectbox("Select Distribution Line", line_list)
        
        # Filter for selected line
        line_data = fault_df[fault_df['line'] == line_selection]
        
        # Determine fault type safely
        if not line_data.empty and 'fault' in line_data.columns:
            current_fault = line_data['fault'].iloc[0]
        else:
            current_fault = "no fault"
    else:
        st.error("Column 'line' not found in fault_dataset.csv")
        st.stop()

    sub_selection = st.sidebar.selectbox("Select Substation", asset_df['Substation_ID'].unique())

    # 3. RECTIFICATION LOGIC
    def get_rectification(f_type):
        rect_map = {
            '3psc': "🚨 **Emergency Trip:** Open Three-Phase Breaker. Check for insulation failure.",
            'spgf': "⚠️ **Ground Fault:** Isolate affected phase and check grounding transformer.",
            'Overload': "📉 **Load Shedding:** Reduce non-critical load in current sector.",
            'UnderVoltage': "🔋 **Capacitor Bank:** Activate banks to boost voltage at substation.",
            'no fault': "✅ **System Healthy:** No immediate action required."
        }
        return rect_map.get(f_type, "🔍 **Standard Inspection Required**")

    # 4. DASHBOARD LAYOUT
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📍 Status Report")
        st.write(f"**Location:** {line_selection}")
        st.metric("Detected Fault", str(current_fault).upper())
        st.info(get_rectification(current_fault))

    with col2:
        st.subheader("Voltage Profile Analysis")
        # Checking for the specific voltage columns in your dataset
        v_cols = [c for c in ['Ua1', 'Ub1', 'Uc1'] if c in line_data.columns]
        if v_cols:
            fig = px.line(line_data, y=v_cols, title=f"3-Phase Voltage: {line_selection}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Voltage columns (Ua1, Ub1, Uc1) not found in dataset.")

    # 5. ASSET MONITORING
    st.divider()
    st.subheader("Substation Asset Health Monitor")
    
    sub_data = asset_df[asset_df['Substation_ID'] == sub_selection]
    
    if not sub_data.empty:
        fig_asset = px.bar(sub_data, x='Asset_ID', y='Voltage_V', color='Asset_Type', 
                           title=f"Voltage Stability: {sub_selection}")
        st.plotly_chart(fig_asset, use_container_width=True)

    # 6. RAW DATA TOGGLE
    if st.checkbox("Show Recent Fault Events"):
        st.dataframe(asset_df[['Timestamp', 'Substation_ID', 'Fault_Event', 'Asset_Type']].dropna())

else:
    st.info("Upload your CSV files to the repository to begin analysis.")
