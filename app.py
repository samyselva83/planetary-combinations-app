import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
import random

# ------------------------------------------
# LOCATION DATABASE (India + timezone info)
# ------------------------------------------
COUNTRY_LOCATIONS = {
    "India - Chennai": ("Chennai", 13.0827, 80.2707, "Asia/Kolkata"),
    "India - Madurai": ("Madurai", 9.9252, 78.1198, "Asia/Kolkata"),
    "India - Coimbatore": ("Coimbatore", 11.0168, 76.9558, "Asia/Kolkata"),
    "India - Bengaluru": ("Bengaluru", 12.9716, 77.5946, "Asia/Kolkata"),
    "India - Hyderabad": ("Hyderabad", 17.3850, 78.4867, "Asia/Kolkata"),
    "India - Kochi": ("Kochi", 9.9312, 76.2673, "Asia/Kolkata"),
    "India - Mumbai": ("Mumbai", 19.0760, 72.8777, "Asia/Kolkata"),
    "India - Delhi": ("Delhi", 28.6139, 77.2090, "Asia/Kolkata"),
    "India - Kolkata": ("Kolkata", 22.5726, 88.3639, "Asia/Kolkata"),
    "India - Jaipur": ("Jaipur", 26.9124, 75.7873, "Asia/Kolkata"),
}

# Planetary cycles used deterministically
PLANETS = ["MOON", "MERCURY", "VENUS", "SUN", "MARS", "RAHU", "JUPITER", "SATURN", "KETHU"]

# Activity mapping (simplified for demo)
ACTIVITY_MAP = {
    "SUN": "Leadership / Focused Work",
    "MOON": "Creative Work / Music",
    "MARS": "Sports / Energy Tasks",
    "MERCURY": "Communication / Writing",
    "JUPITER": "Teaching / Strategy",
    "VENUS": "Relationships / Art",
    "SATURN": "Planning / Long-term work",
    "RAHU": "Exploration / Research",
    "KETHU": "Meditation / Spiritual",
}

STAR_LEVELS = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
LEVELS = ["Poor", "Average", "Good", "Very Good", "Excellent"]

# ------------------------------------------
# Helper Functions
# ------------------------------------------

def generate_planetary_combinations(date_obj, city):
    """Deterministic combinations based on date and city coordinates"""
    random.seed(f"{date_obj}-{city}")
    combos = []
    base_hour = 0
    for i in range(9):
        # Time window (3-hour slots approx)
        start_time = (datetime.combine(date_obj, datetime.min.time()) + timedelta(hours=base_hour)).strftime("%I:%M %p")
        end_time = (datetime.combine(date_obj, datetime.min.time()) + timedelta(hours=base_hour + 3)).strftime("%I:%M %p")
        start_end = f"{start_time} - {end_time}"

        # Deterministic planet order
        first, second, third = random.sample(PLANETS, 3)
        combo = f"{first}/{second}/{third}"

        # Deterministic level
        star_idx = (hash(f"{first}{second}{third}{date_obj}") % len(STAR_LEVELS))
        stars = STAR_LEVELS[star_idx]
        level = LEVELS[star_idx]

        # Get activity
        activity = ACTIVITY_MAP[first]

        combos.append({
            "Date": date_obj.strftime("%d-%m-%Y"),
            "Time Slot": start_end,
            "Planetary Combination": combo,
            "Stars": stars,
            "Level": level,
            "Recommended Activity": activity
        })
        base_hour += 3

    return combos

# ------------------------------------------
# Streamlit UI
# ------------------------------------------
st.set_page_config(page_title="Planetary Combination Predictor", layout="wide")

st.title("🌌 Planetary Combination Predictor (Deterministic Model)")

# Select city
city_name = st.selectbox("Select City", list(COUNTRY_LOCATIONS.keys()))
city, lat, lon, tz_str = COUNTRY_LOCATIONS[city_name]
timezone = pytz.timezone(tz_str)

# Single or multiple dates
option = st.radio("Select Mode", ["Single Date", "Multiple Dates"], horizontal=True)

if option == "Single Date":
    date = st.date_input("Select Date", datetime.now().date())
    if st.button("Generate"):
        data = generate_planetary_combinations(date, city)
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "planetary_data.csv", "text/csv")
else:
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now().date())
    with col2:
        end_date = st.date_input("End Date", datetime.now().date() + timedelta(days=3))

    if st.button("Generate for Date Range"):
        all_data = []
        current_date = start_date
        while current_date <= end_date:
            daily_data = generate_planetary_combinations(current_date, city)
            all_data.extend(daily_data)
            current_date += timedelta(days=1)

        df = pd.DataFrame(all_data)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "planetary_range_data.csv", "text/csv")
