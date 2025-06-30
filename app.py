import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Coffee Sensor Visualizations", layout="wide")

BASE_DIR = "dataset"

SENSOR_COLUMNS = ["SP-12A", "SP-31", "TGS-813", "TGS-842", "SP-AQ3", "TGS-823", "ST-31", "TGS-800"]

st.title("Electronic Nose Coffee Sensor Data")

quality_folder = st.sidebar.selectbox("Select Coffee Quality", ["AQ_Coffee", "HQ_Coffee", "LQ_Coffee"])

folder_path = os.path.join(BASE_DIR, quality_folder)
file_list = sorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])

selected_file = st.sidebar.selectbox("Select File", file_list)

file_path = os.path.join(folder_path, selected_file)
df = pd.read_csv(file_path, delimiter="\t", header=None)

# Handle possible extra column
if df.shape[1] > 8:
    df = df.iloc[:, 1:]

df.columns = SENSOR_COLUMNS

# Sidebar - Sensor Selection
sensor_options = ["All Sensors"] + SENSOR_COLUMNS
selected_sensor = st.sidebar.selectbox("Select Sensor", sensor_options)

# Plotting
st.subheader(f"📈 Sensor Data Plot - {selected_file} ({quality_folder})")

fig, ax = plt.subplots(figsize=(14, 8))

if selected_sensor == "All Sensors":
    for col in df.columns:
        ax.plot(df.index, df[col], label=col)
else:
    ax.plot(df.index, df[selected_sensor], label=selected_sensor)

ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Resistance (kΩ)")
ax.set_title(f"{selected_sensor} - Resistance over Time")
ax.legend()
ax.grid(True)

st.pyplot(fig)
