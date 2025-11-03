# app.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
import hashlib
import math

# Optional Skyfield (astronomical)
try:
    from skyfield.api import Loader, wgs84
    SKYFIELD_OK = True
except Exception:
    SKYFIELD_OK = False

# ---------------------------
# Countries → Cities → Coordinates
# ---------------------------
LOCATION_DATA = {
    "India": {
        "Chennai": (13.0827, 80.2707),
        "Bangalore": (12.9716, 77.5946),
        "Mumbai": (19.0760, 72.8777),
        "Delhi": (28.6139, 77.2090),
        "Hyderabad": (17.3850, 78.4867),
        "Kolkata": (22.5726, 88.3639),
        "Coimbatore": (11.0168, 76.9558),
        "Madurai": (9.9252, 78.1198),
        "Pune": (18.5204, 73.8567),
        "Tirunelveli": (8.7139, 77.7567),
    },
    "USA": {
        "New York": (40.7128, -74.0060),
        "Los Angeles": (34.0522, -118.2437),
        "Chicago": (41.8781, -87.6298),
        "Houston": (29.7604, -95.3698),
        "San Francisco": (37.7749, -122.4194),
    },
    "UK": {
        "London": (51.5074, -0.1278),
        "Manchester": (53.4808, -2.2426),
        "Birmingham": (52.4862, -1.8904),
        "Edinburgh": (55.9533, -3.1883),
    },
    "Australia": {
        "Sydney": (-33.8688, 151.2093),
        "Melbourne": (-37.8136, 144.9631),
        "Brisbane": (-27.4698, 153.0251),
        "Perth": (-31.9505, 115.8605),
    },
    "Germany": {
        "Berlin": (52.5200, 13.4050),
        "Munich": (48.1351, 11.5820),
        "Frankfurt": (50.1109, 8.6821),
    }
}

# Default coordinates (if custom city typed)
DEFAULT_COORDS = (13.0827, 80.2707)

# ---------------------------
# Planetary combinations list
# (short demo subset — replace with your full list)
# ---------------------------
PLANETARY_COMBINATIONS_FULL = [
    "MOON/MERCURY/MERCURY", "MOON/MERCURY/KETHU", "MOON/MERCURY/VENUS",
    "MOON/MERCURY/SUN", "MOON/MERCURY/MOON", "MOON/MERCURY/MARS",
    "MOON/MERCURY/RAHU", "MOON/MERCURY/JUPITER", "MOON/MERCURY/SATURN",
    "SUN/KETHU/KETHU", "SUN/KETHU/VENUS", "SUN/KETHU/SUN",
    "SUN/KETHU/MOON", "SUN/KETHU/MARS", "SUN/KETHU/RAHU",
    "SUN/KETHU/JUPITER", "SUN/KETHU/SATURN", "SUN/KETHU/MERCURY",
]
if len(PLANETARY_COMBINATIONS_FULL) < 200:
    PLANETARY_COMBINATIONS_FULL *= 20  # repeat to extend

# ---------------------------
# Deterministic helper functions
# ---------------------------
def deterministic_index(text, mod):
    return int(hashlib.sha256(text.encode()).hexdigest()[:16], 16) % mod

def deterministic_choice(text, arr):
    return arr[deterministic_index(text, len(arr))]

# ---------------------------
# Micro-slot generator
# ---------------------------
def generate_day_micro_slots(date, city, country):
    coords = None
    if country in LOCATION_DATA and city in LOCATION_DATA[country]:
        coords = LOCATION_DATA[country][city]
    lat, lon = coords if coords else DEFAULT_COORDS

    start_dt = datetime.combine(date, time(0, 1))
    end_dt = datetime.combine(date, time(23, 59))
    total_minutes = int((end_dt - start_dt).total_seconds() // 60)

    rows = []
    minute_cursor = 0
    combo_idx = deterministic_index(f"{date}_{city}_{country}", len(PLANETARY_COMBINATIONS_FULL))

    while minute_cursor < total_minutes:
        combo = PLANETARY_COMBINATIONS_FULL[combo_idx % len(PLANETARY_COMBINATIONS_FULL)]
        duration = 2 + deterministic_index(f"{combo}_{date}_{city}", 11)  # 2–12 min
        remaining = total_minutes - minute_cursor
        if duration > remaining:
            duration = remaining
        slot_start = start_dt + timedelta(minutes=minute_cursor)
        slot_end = slot_start + timedelta(minutes=duration - 1)
        seed = f"{combo}_{date}_{city}_{minute_cursor}"
        condition = deterministic_choice(seed, [
            "Sun Radiant", "Moon Bright", "Mars Energetic",
            "Mercury Active", "Jupiter Wise", "Venus Calm", "Saturn Focused"
        ])
        star_count = (deterministic_index(seed, 5) + 1)
        stars = "⭐" * star_count
        level_map = {1:"Poor",2:"Average",3:"Good",4:"Very Good",5:"Excellent"}
        level = level_map.get(star_count, "Good")
        activity = deterministic_choice(seed + "_act", [
            "Decision-making", "Creative work", "Meditation",
            "Leadership", "Research", "Relaxation", "Exercise"
        ])

        rows.append({
            "Country": country,
            "Location": city,
            "Date": date.strftime("%d-%m-%Y"),
            "Day": date.strftime("%a"),
            "Start": slot_start.strftime("%H:%M"),
            "End": slot_end.strftime("%H:%M"),
            "Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Combination": combo,
            "Recommended_Activity": activity
        })
        minute_cursor += duration
        combo_idx += 1
    return pd.DataFrame(rows)

# ---------------------------
# Multi-day summary generator
# ---------------------------
def generate_multi_day_summary(start_date, end_date, city, country):
    rows = []
    current = start_date
    while current <= end_date:
        seed = f"{country}_{city}_{current}"
        for i in range(10):
            combo = deterministic_choice(seed + f"_combo{i}", PLANETARY_COMBINATIONS_FULL)
            stars = "⭐" * (1 + deterministic_index(seed + f"_stars{i}", 5))
            cond = deterministic_choice(seed + f"_cond{i}", [
                "Sun Radiant", "Moon Bright", "Mars Energetic", "Mercury Active"
            ])
            level_map = {1:"Poor",2:"Average",3:"Good",4:"Very Good",5:"Excellent"}
            level = level_map.get(len(stars), "Good")
            act = deterministic_choice(seed + f"_act{i}", [
                "Decision-making", "Creative work", "Meditation",
                "Leadership", "Research", "Relaxation", "Exercise"
            ])
            rows.append({
                "Country": country,
                "Location": city,
                "Date": current.strftime("%d-%m-%Y"),
                "Day": current.strftime("%a"),
                "Condition": cond,
                "Stars": stars,
                "Level": level,
                "Best_Combination": combo,
                "Recommended_Activity": act
            })
        current += timedelta(days=1)
    return pd.DataFrame(rows)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Planetary Slot Generator", layout="wide")
st.title("🌍 Planetary Slot Generator (with Country support)")

col1, col2 = st.columns(2)
with col1:
    country = st.selectbox("Select Country", list(LOCATION_DATA.keys()))
with col2:
    city = st.selectbox("Select City", list(LOCATION_DATA[country].keys()))

st.markdown("---")
start_date = st.date_input("Start Date", datetime.now().date())
end_date = st.date_input("End Date", datetime.now().date())
mode = st.radio("Mode", ["Single-day detailed (micro slots)", "Multi-day summary"])

if st.button("Generate"):
    if mode.startswith("Single"):
        df = generate_day_micro_slots(start_date, city, country)
    else:
        df = generate_multi_day_summary(start_date, end_date, city, country)

    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, f"planetary_{country}_{city}.csv", "text/csv")
