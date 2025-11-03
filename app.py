import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
import math
import hashlib

# ----------------------------------------------------
# 🌍 Approximate latitude/longitude for common cities
# ----------------------------------------------------
CITY_COORDS = {
    "chennai": (13.0827, 80.2707),
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "bangalore": (12.9716, 77.5946),
    "hyderabad": (17.3850, 78.4867),
    "kolkata": (22.5726, 88.3639),
    "coimbatore": (11.0168, 76.9558),
    "madurai": (9.9252, 78.1198),
    "pune": (18.5204, 73.8567),
    "tirunelveli": (8.7139, 77.7567),
}

# ----------------------------------------------------
# 🌅 Approximate sunrise/sunset calculator (no APIs)
# ----------------------------------------------------
def calculate_sunrise_sunset(lat, lon, date):
    """Approximate sunrise/sunset times in local time."""
    day_of_year = date.timetuple().tm_yday
    decl = 23.44 * math.cos(math.radians(360/365 * (day_of_year - 173)))
    ha = math.degrees(math.acos(-math.tan(math.radians(lat)) * math.tan(math.radians(decl))))
    sunrise = 12 - ha/15
    sunset = 12 + ha/15
    sunrise_time = datetime.combine(date, time(int(sunrise), int((sunrise % 1)*60)))
    sunset_time = datetime.combine(date, time(int(sunset), int((sunset % 1)*60)))
    return sunrise_time, sunset_time


# ----------------------------------------------------
# 🪐 Core planetary logic (deterministic)
# ----------------------------------------------------
planetary_conditions = [
    "Sun Radiant", "Moon Bright", "Mars Energetic",
    "Mercury Active", "Jupiter Wise", "Venus Calm", "Saturn Focused"
]

recommended_activities = [
    "Decision-making, teaching, mentoring",
    "Creative work, music, or writing",
    "Meditation, mindfulness, self-reflection",
    "Leadership, presentations, planning",
    "Research, analysis, and deep work",
    "Relaxation and family time",
    "Physical exercise or travel"
]

level_map = {
    1: ("⭐", "Poor"),
    2: ("⭐⭐", "Average"),
    3: ("⭐⭐⭐", "Good"),
    4: ("⭐⭐⭐⭐", "Very Good"),
    5: ("⭐⭐⭐⭐⭐", "Excellent")
}

planetary_combinations = [
    "MOON/MERCURY/MARS", "SUN/VENUS/MERCURY", "VENUS/SATURN/JUPITER",
    "MARS/SUN/MERCURY", "MOON/MERCURY/KETHU", "MERCURY/VENUS/SUN",
    "SATURN/JUPITER/MOON", "SUN/VENUS/MOON", "MERCURY/MARS/SUN",
    "JUPITER/SUN/MARS", "VENUS/MOON/KETHU", "MARS/KETHU/RAHU"
]


def deterministic_choice(seed_str, items):
    hash_val = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16)
    return items[hash_val % len(items)]


# ----------------------------------------------------
# 📅 Generate deterministic planetary data for a date
# ----------------------------------------------------
def generate_planetary_data_for_date(date, city):
    city_lower = city.lower()
    lat, lon = CITY_COORDS.get(city_lower, (13.0827, 80.2707))
    sunrise, sunset = calculate_sunrise_sunset(lat, lon, date)

    daylight_duration = (sunset - sunrise) / 10
    morning_slots = [
        (sunrise + i * daylight_duration, sunrise + (i + 1) * daylight_duration)
        for i in range(10)
    ]

    evening_start = sunset
    evening_end = datetime.combine(date, time(23, 59))
    evening_duration = (evening_end - evening_start) / 10
    evening_slots = [
        (evening_start + i * evening_duration, evening_start + (i + 1) * evening_duration)
        for i in range(10)
    ]

    rows = []
    for phase, slots in [("Morning", morning_slots), ("Evening", evening_slots)]:
        for i, (s, e) in enumerate(slots):
            seed = f"{city}_{date}_{phase}_{i}"
            cond = deterministic_choice(seed, planetary_conditions)
            stars, level = level_map[(int(hashlib.md5(seed.encode()).hexdigest(), 16) % 5) + 1]
            combo = deterministic_choice(seed, planetary_combinations)
            activity = deterministic_choice(seed, recommended_activities)
            rows.append({
                "Date": date.strftime("%d-%m-%Y"),
                "Day": date.strftime("%a"),
                "Timing": f"{s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}",
                "Phase": phase,
                "Planetary_Condition": cond,
                "Stars": stars,
                "Level": level,
                "Best_Planetary_Combination": combo,
                "Recommended_Activity": activity,
                "Location": city.title()
            })
    return rows


# ----------------------------------------------------
# 📅 Generate multiple-day table
# ----------------------------------------------------
def generate_planetary_table(start_date, end_date, city):
    all_rows = []
    current_date = start_date
    while current_date <= end_date:
        all_rows.extend(generate_planetary_data_for_date(current_date, city))
        current_date += timedelta(days=1)
    return pd.DataFrame(all_rows)


# ----------------------------------------------------
# 🎨 Streamlit UI
# ----------------------------------------------------
st.set_page_config(page_title="Deterministic Planetary Energy Predictor", layout="wide")
st.title("🔭 Deterministic Planetary Energy Predictor")

city = st.text_input("Enter Location", "Chennai")
col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date", datetime.now().date())
end_date = col2.date_input("End Date", datetime.now().date())

if st.button("Generate Table"):
    df = generate_planetary_table(start_date, end_date, city)
    st.success(f"Generated deterministic planetary schedule for {city}")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download CSV",
        csv,
        f"planetary_energy_{start_date}_to_{end_date}_{city}.csv",
        "text/csv"
    )
