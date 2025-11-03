import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# ------------------------------------------------------
# 🌙 Title and Description
# ------------------------------------------------------
st.set_page_config(page_title="Planetary Movement Calendar", layout="wide")
st.title("🪐 Planetary Movement & Activity Calendar")
st.markdown("Generate planetary conditions and activity suggestions for any date or date range.")

# ------------------------------------------------------
# 🌍 Constants and Reference Lists
# ------------------------------------------------------
planetary_conditions = ["Moon Bright", "Sun Radiant", "Mercury Active", "Jupiter Wise", "Venus Calm", "Mars Energetic", "Saturn Focused"]
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

# Full planetary combination list (you can expand later)
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
# Helper Functions
# ------------------------------------------------------
def fmt_time(minutes):
    h = minutes // 60
    m = minutes % 60
    am_pm = "am" if h < 12 else "pm"
    h = 12 if h == 0 else (h - 12 if h > 12 else h)
    return f"{h:02d}:{m:02d}:00 {am_pm}"

# ------------------------------------------------------
# 🧭 Single-Date Mode
# ------------------------------------------------------
if start_date == end_date:
    st.subheader(f"🌞 Full Planetary Movements — {start_date.strftime('%d-%m-%Y')}")

    total_minutes = 24 * 60 - 1  # 00:01–23:59
    step = total_minutes // len(planetary_combinations_full)
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
    st.download_button("📥 Download CSV", data=csv, file_name=f"planetary_movements_{start_date}.csv")

# ------------------------------------------------------
# 🪐 Multi-Date Mode
# ------------------------------------------------------
else:
    st.subheader(f"📆 Planetary Overview — {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}")
    current_date = start_date
    rows = []

    while current_date <= end_date:
        level = random.choice(levels)
        stars = stars_map[level]
        condition = random.choice(planetary_conditions)
        activity = random.choice(activities)
        combo = random.choice(planetary_combinations_full)
        morning_start = f"{random.randint(0, 3):02d}:{random.randint(0,59):02d} AM"
        morning_end = f"{random.randint(4, 9):02d}:{random.randint(0,59):02d} AM"
        evening_start = f"{random.randint(17, 19):02d}:{random.randint(0,59):02d} PM"
        evening_end = f"{random.randint(20, 23):02d}:{random.randint(0,59):02d} PM"

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
    st.download_button("📥 Download CSV", data=csv, file_name=f"planetary_summary_{start_date}_to_{end_date}.csv")
