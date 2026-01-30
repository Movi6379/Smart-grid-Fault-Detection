⚡ Smart Grid Fault Analytics
An interactive dashboard for detecting power grid faults, identifying affected areas, and automating rectification strategies using Python and Streamlit.

📊 Core Functionalities
Fault Localization: Pinpoints faults (3psc, 2psc, spgf) to specific lines (Line 1-5) and exact cable positions.

Substation Monitoring: Real-time health tracking of Transformers, Switches, and Smart Meters at SS_001 and SS_002.

Predictive Rectification: Automated logic recommending fixes (e.g., Capacitor Activation for Under-Voltage or Breaker Tripping for Short Circuits).

📂 Data Sources
fault_dataset.csv: Electrical telemetry (Voltage/Current) and fault labels.

grid_asset_data.csv: Operational logs, asset types, and maintenance actions.

🛠️ Tech Stack
Language: Python 3.x

Dashboard: Streamlit

Visuals: Plotly Express

Data Handling: Pandas
