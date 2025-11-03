import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sun
import pytz
import hashlib
import math

# ----------------------------------------------------
# 🌍 Deterministic location-based planetary data model
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


# ----------------------------------------------------
# 🔢 Deterministic hash-based selector
# ----------------------------------------------------
def deterministic_choice(seed_str, items):
    """Select an item deterministically using hash (not random)."""
    hash_val = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16)
    return items[hash_val % len(items)]


# ----------------------------------------------------
# ☀️ Get Sunrise/Sunset for a given location and date
# ----------------------------------------------------
def get_sun_times(location_name, date):
    try:
        loc = LocationInfo(location_name)
    except Exception:
        # fallback if location not found
        loc = LocationInfo("Chennai", "India", "Asia/Kolkata", 13.0827, 80.2707)

    tz = pytz.timezone(loc.timezone)
    s = sun(loc.observer, date=date, tzinfo=tz)
    return s["sunrise"], s["sunset"]


# ----------------------------------------------------
# 🪐 Generate deterministic planetary data for one date
# ----------------------------------------------------
def generate_planetary_data_for_date(date, location):
    sunrise, sunset = get_sun_times(location, date)

    # Split daylight hours into 10 planetary periods (morning slots)
    daylight_duration = (sunset - sunrise) / 10
    morning_slots = [
        (sunrise + i * daylight_duration, sunrise + (i + 1) * daylight_duration)
        for i in range(10)
    ]

    # Evening: mirror with same slot size from sunset to midnight
    evening_start = sunset
    evening_end = datetime.combine(date, datetime.max.time()).replace(hour=23, minute=59, second=0, microsecond=0)
    evening_duration = (evening_end - evening_start) / 10
    evening_slots = [
        (evening_start + i * evening_duration, evening_start + (i + 1) * evening_duration)
        for i in range(10)
    ]

    rows = []
    for i, (m_start, m_end) in enumerate(morning_slots):
        seed = f"{location}_{date}_{i}_morning"
        cond = deterministic_choice(seed, planetary_conditions)
        stars, level = level_map[(int(hashlib.md5(seed.encode()).hexdigest(), 16) % 5) + 1]
        combo = deterministic_choice(seed, planetary_combinations)
        activity = deterministic_choice(seed, recommended_activities)

        rows.append({
            "Date": date.strftime("%d-%m-%Y"),
            "Day": date.strftime("%a"),
            "Timing": f"{m_start.strftime('%I:%M %p')} - {m_end.strftime('%I:%M %p')}",
            "Phase": "Morning",
            "Planetary_Condition": cond,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": activity,
            "Location": location
        })

    for i, (e_start, e_end) in enumerate(evening_slots):
        seed = f"{location}_{date}_{i}_evening"
        cond = deterministic_choice(seed, planetary_conditions)
        stars, level = level_map[(int(hashlib.md5(seed.encode()).hexdigest(), 16) % 5) + 1]
        combo = deterministic_choice(seed, planetary_combinations)
        activity = deterministic_choice(seed, recommended_activities)

        rows.append({
            "Date": date.strftime("%d-%m-%Y"),
            "Day": date.strftime("%a"),
            "Timing": f"{e_start.strftime('%I:%M %p')} - {e_end.strftime('%I:%M %p')}",
            "Phase": "Evening",
            "Planetary_Condition": cond,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": activity,
            "Location": location
        })

    return rows


# ----------------------------------------------------
# 📅 Generate data for multiple dates
# ----------------------------------------------------
def generate_planetary_table(start_date, end_date, location):
    all_rows = []
    current_date = start_date
    while current_date <= end_date:
        all_rows.extend(generate_planetary_data_for_date(current_date, location))
        current_date += timedelta(days=1)
    return pd.DataFrame(all_rows)


# ----------------------------------------------------
# 🎨 Streamlit UI
# ----------------------------------------------------
st.set_page_config(page_title="Planetary Energy Predictor", layout="wide")
st.title("🔭 Deterministic Planetary Energy Predictor")

location = st.text_input("Enter Location", "Chennai")
col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date", datetime.now().date())
end_date = col2.date_input("End Date", datetime.now().date())

if st.button("Generate Table"):
    df = generate_planetary_table(start_date, end_date, location)
    st.success(f"Generated planetary schedule for {location}")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download CSV",
        csv,
        f"planetary_energy_{start_date}_to_{end_date}_{location}.csv",
        "text/csv"
    )
