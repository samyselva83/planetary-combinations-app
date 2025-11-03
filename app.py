import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# -----------------------------------------
# Streamlit Page Setup
# -----------------------------------------
st.set_page_config(page_title="Daily Planetary Combination Insights", layout="wide", page_icon="🪐")

st.title("🪐 Daily Planetary Combination Insights")
st.markdown("""
Check **planetary combinations** for any date or date range.  
For a **single date**, you’ll see detailed 24-hour planetary movements.  
For a **date range**, daily summary insights are shown.
""")

# -----------------------------------------
# Date Input
# -----------------------------------------
today = datetime.today().date()
col1, col2 = st.columns(2)
start_date = col1.date_input("Select Start Date", today)
end_date = col2.date_input("Select End Date", today)

if start_date > end_date:
    st.error("⚠️ End date must be greater than or equal to start date.")
    st.stop()

# -----------------------------------------
# Base Data
# -----------------------------------------
weekday_map = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
stars_map = {"Excellent": "⭐⭐⭐⭐⭐", "Very Good": "⭐⭐⭐⭐", "Good": "⭐⭐⭐", "Average": "⭐⭐"}

planetary_conditions = [
    "Mercury Strong", "Moon Bright", "Venus Benefic", "Mars Energetic",
    "Jupiter Supportive", "Sun Powerful", "Saturn Steady", "Mercury Direct",
    "Moon Rising", "Venus Harmonious"
]

# Combinations for range case
combinations_range = [
    ("Mercury / Moon / Jupiter", "Planning, learning, meetings"),
    ("Sun / Mercury / Mars", "Leadership, new starts, motivation"),
    ("Venus / Mercury / Moon", "Creativity, teamwork, communication"),
    ("Mars / Jupiter / Mercury", "Technical work, coding, innovation"),
    ("Moon / Venus / Jupiter", "Relationships, travel, family harmony"),
    ("Saturn / Mercury / Jupiter", "Research, organization, planning"),
    ("Sun / Jupiter / Mercury", "Decision-making, teaching, mentoring"),
    ("Mars / Mercury / Venus", "Business, design, negotiations"),
    ("Moon / Mercury / Venus", "Writing, counseling, artistic work"),
    ("Jupiter / Venus / Mercury", "Marketing, partnerships, branding")
]

# Combinations for single date movement (shorter transitions)
planetary_set = [
    "MOON/MERCURY/MERCURY", "MOON/MERCURY/KETHU", "MOON/MERCURY/VENUS",
    "MOON/MERCURY/SUN", "MOON/MERCURY/MOON", "MOON/MERCURY/MARS",
    "MOON/MERCURY/RAHU", "MOON/MERCURY/JUPITER", "MOON/MERCURY/SATURN",
    "MOON/MERCURY/PLUTO"
]

# Helper to format time
def fmt_time(minutes):
    h = minutes // 60
    m = minutes % 60
    suffix = "AM" if h < 12 else "PM"
    h = h if 1 <= h <= 12 else (12 if h == 0 else h - 12)
    return f"{h:02d}:{m:02d} {suffix}"

# -----------------------------------------
# SINGLE DATE VIEW (Full 24-hour Movement)
# -----------------------------------------
if start_date == end_date:
    st.subheader(f"🌞 Full Planetary Movements for {start_date.strftime('%d-%m-%Y')}")

    total_minutes = 24 * 60
    split_points = sorted(random.sample(range(5, total_minutes - 5), 9))
    split_points = [1] + split_points + [total_minutes - 1]

    movements = []
    for i in range(1, len(split_points)):
        start_m = split_points[i - 1]
        end_m = split_points[i]
        combination = planetary_set[i - 1]
        movements.append({
            "Combination": combination,
            "Start_Time": fmt_time(start_m),
            "Stop_Time": fmt_time(end_m)
        })

    df_movements = pd.DataFrame(movements)
    st.dataframe(df_movements, use_container_width=True, hide_index=True)

# -----------------------------------------
# MULTIPLE DATE RANGE VIEW
# -----------------------------------------
else:
    st.subheader(f"✨ Planetary Insights ({start_date} → {end_date})")

    def random_timing(base_hour, base_min):
        h1 = (base_hour + random.randint(-1, 1)) % 24
        m1 = (base_min + random.randint(-10, 10)) % 60
        h2 = (h1 + 3) % 24
        m2 = (base_min + random.randint(-10, 10)) % 60
        fmt = lambda h, m: f"{h:02d}:{m:02d} {'AM' if h < 12 else 'PM'}"
        return f"{fmt(h1, m1)} - {fmt(h2, m2)}"

    rows = []
    dates = pd.date_range(start_date, end_date)

    for d in dates:
        day_name = weekday_map[d.weekday()]
        level = random.choice(["Excellent", "Very Good", "Good", "Average"])
        stars = stars_map[level]
        combo, activity = random.choice(combinations_range)
        planetary = random.choice(planetary_conditions)
        morning = random_timing(0, 30)
        evening = random_timing(18, 30)

        rows.append({
            "Date": d.strftime("%d-%m-%Y"),
            "Day": day_name,
            "Morning_Timing": morning,
            "Evening_Timing": evening,
            "Planetary_Condition": planetary,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": activity
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

# -----------------------------------------
# Footer
# -----------------------------------------
st.markdown("---")
st.caption("Generated dynamically for any date using planetary energy mapping | © 2025 AstroNova AI 🪐")
