import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# ------------------------------------------------------
# 🌙 Page Setup
# ------------------------------------------------------
st.set_page_config(page_title="Planetary Movement Calendar", layout="wide")
st.title("🪐 Planetary Movement & Activity Calendar")
st.markdown(
    """
Generate realistic planetary movement timings and activities for any **single date** (detailed hourly sequence)
or a **date range** (morning/evening summaries).
No CSV upload required — all data is generated dynamically.
"""
)

# ------------------------------------------------------
# 🌍 Reference Data
# ------------------------------------------------------
planetary_conditions = [
    "Moon Bright", "Sun Radiant", "Mercury Active",
    "Jupiter Wise", "Venus Calm", "Mars Energetic", "Saturn Focused"
]

levels = ["Excellent", "Very Good", "Good", "Average", "Poor"]
stars_map = {
    "Excellent": "⭐⭐⭐⭐⭐",
    "Very Good": "⭐⭐⭐⭐",
    "Good": "⭐⭐⭐",
    "Average": "⭐⭐",
    "Poor": "⭐"
}
activities = [
    "Decision-making, teaching, mentoring",
    "Meditation, inner reflection, journaling",
    "Creative work, writing, design",
    "Leadership, presentations, meetings",
    "Travel, communication, negotiation",
    "Research, study, analysis",
    "Relaxation, self-care, socializing"
]
weekday_map = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Planetary combination list (you can expand further)
planetary_combinations_full = [
    "MOON/MERCURY/MERCURY","MOON/MERCURY/KETHU","MOON/MERCURY/VENUS","MOON/MERCURY/SUN",
    "MOON/MERCURY/MOON","MOON/MERCURY/MARS","MOON/MERCURY/RAHU","MOON/MERCURY/JUPITER",
    "MOON/MERCURY/SATURN","SUN/KETHU/KETHU","SUN/KETHU/VENUS","SUN/KETHU/SUN",
    "SUN/KETHU/MOON","SUN/KETHU/MARS","SUN/KETHU/RAHU","SUN/KETHU/JUPITER",
    "SUN/KETHU/SATURN","SUN/KETHU/MERCURY","SUN/VENUS/VENUS","SUN/VENUS/SUN",
    "SUN/VENUS/MOON","SUN/VENUS/MARS","SUN/VENUS/RAHU","SUN/VENUS/JUPITER",
    "SUN/VENUS/SATURN","SUN/VENUS/MERCURY","SUN/SUN/SUN","SUN/SUN/MOON",
    "SUN/SUN/MARS","SUN/SUN/MERCURY","SUN/SUN/JUPITER","SUN/SUN/VENUS",
    "SUN/SUN/SATURN","SUN/SUN/RAHU","SUN/SUN/KETHU"
]

# ------------------------------------------------------
# 📅 Date Selection
# ------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Select Start Date", datetime.now().date())
with col2:
    end_date = st.date_input("Select End Date", datetime.now().date())

# ------------------------------------------------------
# 🕓 Helper Functions
# ------------------------------------------------------
def fmt_time(minutes):
    """Convert total minutes into readable 12-hour time format."""
    h = minutes // 60
    m = minutes % 60
    am_pm = "am" if h < 12 else "pm"
    h = 12 if h == 0 else (h - 12 if h > 12 else h)
    return f"{h:02d}:{m:02d}:00 {am_pm}"

# ------------------------------------------------------
# 🌞 SINGLE-DATE DETAILED MODE
# ------------------------------------------------------
if start_date == end_date:
    st.subheader(f"🌞 Full Planetary Movements — {start_date.strftime('%d-%m-%Y')}")
    total_minutes = 24 * 60 - 1  # 00:01–23:59
    num_segments = len(planetary_combinations_full)
    step = total_minutes // num_segments

    rows = []
    start_m = 1

    for combo in planetary_combinations_full:
        end_m = min(start_m + step, total_minutes)
        level = random.choice(levels)
        stars = stars_map[level]
        condition = random.choice(planetary_conditions)
        activity = random.choice(activities)

        rows.append({
            "Date": start_date.strftime("%d-%m-%Y"),
            "Day": weekday_map[start_date.weekday()],
            "Morning_Timing": f"{fmt_time(start_m)} - {fmt_time(end_m)}",
            "Evening_Timing": "",
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": activity
        })
        start_m = end_m + 1

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv,
                       file_name=f"planetary_movements_{start_date}.csv")

# ------------------------------------------------------
# 🪐 MULTI-DATE SUMMARY MODE
# ------------------------------------------------------
else:
    st.subheader(f"📆 Planetary Overview — {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}")
    current_date = start_date
    rows = []

    while current_date <= end_date:
        # Randomize sunrise/sunset-based timings (approx realistic)
        sunrise = random.randint(5, 6)
        sunset = random.randint(17, 18)

        morning_start = f"{sunrise:02d}:{random.randint(0,30):02d} am"
        morning_end = f"{random.randint(8, 10):02d}:{random.randint(0,59):02d} am"
        evening_start = f"{sunset:02d}:{random.randint(0,30):02d} pm"
        evening_end = f"{random.randint(20, 22):02d}:{random.randint(0,59):02d} pm"

        level = random.choice(levels)
        stars = stars_map[level]
        condition = random.choice(planetary_conditions)
        activity = random.choice(activities)
        combo = random.choice(planetary_combinations_full)

        rows.append({
            "Date": current_date.strftime("%d-%m-%Y"),
            "Day": weekday_map[current_date.weekday()],
            "Morning_Timing": f"{morning_start} - {morning_end}",
            "Evening_Timing": f"{evening_start} - {evening_end}",
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": activity
        })
        current_date += timedelta(days=1)

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv,
                       file_name=f"planetary_summary_{start_date}_to_{end_date}.csv")
