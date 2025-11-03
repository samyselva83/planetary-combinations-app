import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# -----------------------------------------
# Page Setup
# -----------------------------------------
st.set_page_config(page_title="Planetary Combination Viewer", layout="wide", page_icon="🪐")
st.title("🪐 Planetary Combinations and Timing")

today = datetime.today().date()
col1, col2 = st.columns(2)
start_date = col1.date_input("Select Start Date", today)
end_date = col2.date_input("Select End Date", today)

if start_date > end_date:
    st.error("⚠️ End date must be greater than or equal to start date.")
    st.stop()

weekday_map = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
stars_map = {"Excellent": "⭐⭐⭐⭐⭐", "Very Good": "⭐⭐⭐⭐", "Good": "⭐⭐⭐", "Average": "⭐⭐"}

planetary_conditions = [
    "Moon Bright", "Mercury Strong", "Venus Benefic", "Mars Energetic",
    "Jupiter Supportive", "Sun Powerful", "Saturn Steady"
]

levels = ["Excellent", "Very Good", "Good", "Average"]

activities = [
    "Decision-making, teaching, mentoring",
    "Planning, learning, meetings",
    "Leadership, new starts, motivation",
    "Creativity, teamwork, communication",
    "Research, organization, planning",
    "Writing, counseling, artistic work"
]

combinations = [
    "MOON/MERCURY/MERCURY", "MOON/MERCURY/KETHU", "MOON/MERCURY/VENUS",
    "MOON/MERCURY/SUN", "MOON/MERCURY/MOON", "MOON/MERCURY/MARS",
    "MOON/MERCURY/RAHU", "MOON/MERCURY/JUPITER", "MOON/MERCURY/SATURN", "MOON/MERCURY/PLUTO"
]

# Function to format time
def fmt_time(minutes):
    h = minutes // 60
    m = minutes % 60
    am_pm = "am" if h < 12 else "pm"
    h = h if h != 0 else 12
    return f"{h:02d}:{m:02d}:00 {am_pm}"

# ------------------------------------------------------
# SINGLE DATE MODE
# ------------------------------------------------------
if start_date == end_date:
    st.subheader(f"🌞 Full Planetary Movement — {start_date.strftime('%d-%m-%Y')}")

    total_minutes = 24 * 60
    split_points = sorted(random.sample(range(5, total_minutes - 5), 9))
    split_points = [1] + split_points + [total_minutes - 1]

    rows = []
    for i in range(1, len(split_points)):
        start_m = split_points[i - 1]
        end_m = split_points[i]

        combo = combinations[i - 1]
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

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ------------------------------------------------------
# MULTIPLE DATE MODE
# ------------------------------------------------------
else:
    st.subheader(f"✨ Planetary Insights ({start_date} → {end_date})")

    def random_timing(base_hour, base_min):
        h1 = (base_hour + random.randint(-1, 1)) % 24
        m1 = (base_min + random.randint(-10, 10)) % 60
        h2 = (h1 + 3) % 24
        m2 = (base_min + random.randint(-10, 10)) % 60
        fmt = lambda h, m: f"{h:02d}:{m:02d} {'am' if h < 12 else 'pm'}"
        return f"{fmt(h1, m1)} - {fmt(h2, m2)}"

    data = []
    for d in pd.date_range(start_date, end_date):
        day_name = weekday_map[d.weekday()]
        level = random.choice(levels)
        stars = stars_map[level]
        condition = random.choice(planetary_conditions)
        combo = random.choice(combinations)
        activity = random.choice(activities)
        morning = random_timing(0, 30)
        evening = random_timing(18, 30)

        data.append({
            "Date": d.strftime("%d-%m-%Y"),
            "Day": day_name,
            "Morning_Timing": morning,
            "Evening_Timing": evening,
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": activity
        })

    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Generated dynamically | AstroNova AI 🪐")
