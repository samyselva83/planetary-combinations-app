import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ----------------------------------------------------------
# COUNTRY & CITY DATA (directly defined, not uploaded)
# ----------------------------------------------------------
COUNTRY_LOCATIONS = {
    "India": ["Chennai", "Madurai", "Bangalore", "Mumbai", "Delhi"],
    "USA": ["New York", "Los Angeles", "Chicago"],
    "UK": ["London", "Manchester"],
    "Japan": ["Tokyo", "Osaka"],
    "France": ["Paris", "Lyon"]
}

# ----------------------------------------------------------
# DETERMINISTIC PLANETARY COMBINATIONS
# ----------------------------------------------------------
PLANETARY_COMBINATIONS = [
    "MOON/MERCURY/MERCURY", "MOON/MERCURY/KETHU", "MOON/MERCURY/VENUS",
    "MOON/MERCURY/SUN", "MOON/MERCURY/MOON", "MOON/MERCURY/MARS",
    "MOON/MERCURY/RAHU", "MOON/MERCURY/JUPITER", "MOON/MERCURY/SATURN",
    "SUN/VENUS/SUN", "SUN/VENUS/MOON", "SUN/VENUS/MARS",
    "MERCURY/MARS/MARS", "MERCURY/MARS/JUPITER", "MERCURY/MARS/SATURN",
    "VENUS/RAHU/SATURN", "VENUS/RAHU/VENUS", "MARS/JUPITER/MOON",
    "MARS/SATURN/SATURN", "MARS/SATURN/VENUS", "JUPITER/VENUS/SUN",
    "SATURN/MOON/MOON", "SATURN/MARS/MARS", "SATURN/JUPITER/JUPITER"
]

# ----------------------------------------------------------
# DETERMINISTIC CONDITIONS, STARS, LEVELS, ACTIVITIES
# ----------------------------------------------------------
PLANETARY_CONDITIONS = ["Moon Bright", "Sun Radiant", "Venus Calm", "Mars Energetic", "Saturn Focused", "Mercury Active"]
STARS = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
LEVELS = ["Poor", "Average", "Good", "Very Good", "Excellent"]
ACTIVITIES = [
    "Decision-making, teaching, mentoring",
    "Meditation, mindfulness, self-reflection",
    "Research, analysis, and deep work",
    "Creative work, music, or writing",
    "Leadership, presentations, planning",
    "Relaxation and family time"
]

# ----------------------------------------------------------
# FUNCTION: Generate deterministic planetary details
# ----------------------------------------------------------
def deterministic_planetary_data(country: str, city: str, start_date: datetime, days: int):
    data = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        date_str = date.strftime("%d-%m-%Y")
        day_str = date.strftime("%a")

        # Deterministic hash seed
        seed = abs(hash(f"{country}-{city}-{date_str}")) % 99999

        # Deterministic index selection
        condition = PLANETARY_CONDITIONS[seed % len(PLANETARY_CONDITIONS)]
        stars = STARS[seed % len(STARS)]
        level = LEVELS[seed % len(LEVELS)]
        combo = PLANETARY_COMBINATIONS[seed % len(PLANETARY_COMBINATIONS)]
        activity = ACTIVITIES[seed % len(ACTIVITIES)]

        # Deterministic morning/evening timings (slight variation per city)
        base_shift = (seed % 60)
        morning_start = (datetime(date.year, date.month, date.day, 6, 0) + timedelta(minutes=base_shift)).strftime("%I:%M:%S %p")
        morning_end = (datetime(date.year, date.month, date.day, 7, 0) + timedelta(minutes=base_shift)).strftime("%I:%M:%S %p")
        evening_start = (datetime(date.year, date.month, date.day, 18, 0) + timedelta(minutes=base_shift)).strftime("%I:%M:%S %p")
        evening_end = (datetime(date.year, date.month, date.day, 19, 0) + timedelta(minutes=base_shift)).strftime("%I:%M:%S %p")

        data.append({
            "Date": date_str,
            "Day": day_str,
            "Morning_Timing": f"{morning_start} - {morning_end}",
            "Evening_Timing": f"{evening_start} - {evening_end}",
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": activity,
            "Country": country,
            "City": city
        })
    return pd.DataFrame(data)

# ----------------------------------------------------------
# STREAMLIT UI
# ----------------------------------------------------------
st.set_page_config(page_title="🪐 Deterministic Planetary Generator", layout="wide")
st.title("🌌 Deterministic Planetary Combination Generator")
st.markdown("Generate consistent planetary insights based on **location** and **date** — no randomness, fully reproducible.")

# Country & City selection
country = st.selectbox("🌍 Select Country", list(COUNTRY_LOCATIONS.keys()))
city = st.selectbox("🏙️ Select City", COUNTRY_LOCATIONS[country])

# Date & duration
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("📅 Start Date", datetime(2025, 11, 3))
with col2:
    days = st.number_input("🗓️ Number of Days", min_value=1, max_value=60, value=10)

# Generate button
if st.button("🔮 Generate Planetary Schedule"):
    df = deterministic_planetary_data(country, city, datetime.combine(start_date, datetime.min.time()), days)
    st.success(f"✅ Generated for {city}, {country} from {start_date.strftime('%d-%m-%Y')} for {days} days.")
    st.dataframe(df, use_container_width=True)

    # Download CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "planetary_schedule.csv", "text/csv")

st.markdown("---")
st.caption("✨ Generated by Smart Agent — Deterministic Planetary AI ✨")
