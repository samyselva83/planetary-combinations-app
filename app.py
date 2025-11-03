import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------
# Reference time sequence
# ---------------------------
data = """
combination,start_time,stop_time
MOON/MERCURY/MERCURY,0:01,0:03
MOON/MERCURY/KETHU,0:03,0:07
MOON/MERCURY/VENUS,0:07,0:16
MOON/MERCURY/SUN,0:16,0:19
MOON/MERCURY/MOON,0:19,0:24
MOON/MERCURY/MARS,0:24,0:27
MOON/MERCURY/RAHU,0:27,0:36
MOON/MERCURY/JUPITER,0:36,0:43
MOON/MERCURY/SATURN,0:43,0:52
SUN/KETHU/KETHU,0:52,0:55
SUN/KETHU/VENUS,0:55,1:05
SUN/KETHU/SUN,1:05,1:07
SUN/KETHU/MOON,1:07,1:12
SUN/KETHU/MARS,1:12,1:15
SUN/KETHU/RAHU,1:15,1:24
SUN/KETHU/JUPITER,1:24,1:31
SUN/KETHU/SATURN,1:31,1:40
SUN/KETHU/MERCURY,1:40,1:47
"""  # keep expanding full dataset if needed

reference_df = pd.read_csv(pd.io.common.StringIO(data))

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🌙 Planetary Movements (Single-Date)")
selected_date = st.date_input("Select Date", datetime(2025, 11, 3))

# ---------------------------
# Generate full-day table
# ---------------------------
if selected_date:
    rows = []
    for _, r in reference_df.iterrows():
        rows.append({
            "Date": selected_date.strftime("%d-%m-%Y"),
            "Day": selected_date.strftime("%a"),
            "Morning_Timing": f"{r['start_time']} - {r['stop_time']}",
            "Evening_Timing": "",
            "Planetary_Condition": "Moon Bright",
            "Stars": "⭐⭐⭐",
            "Level": "Good",
            "Best_Planetary_Combination": r['combination'],
            "Recommended_Activity": "Decision-making, teaching, mentoring"
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
