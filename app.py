import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Planetary Movement Calendar", layout="wide")
st.title("🪐 Planetary Movement & Activity Calendar")

# -----------------------------------------------------------------
# Reference planetary data (from your list)
# -----------------------------------------------------------------
data = """
combination	start_time	stop_time
MOON/MERCURY/MERCURY	0:01	0:03
MOON/MERCURY/KETHU	0:03	0:07
MOON/MERCURY/VENUS	0:07	0:16
MOON/MERCURY/SUN	0:16	0:19
MOON/MERCURY/MOON	0:19	0:24
MOON/MERCURY/MARS	0:24	0:27
MOON/MERCURY/RAHU	0:27	0:36
MOON/MERCURY/JUPITER	0:36	0:43
MOON/MERCURY/SATURN	0:43	0:52
SUN/KETHU/KETHU	0:52	0:55
SUN/KETHU/VENUS	0:55	1:05
SUN/KETHU/SUN	1:05	1:07
SUN/KETHU/MOON	1:07	1:12
SUN/KETHU/MARS	1:12	1:15
SUN/KETHU/RAHU	1:15	1:24
SUN/KETHU/JUPITER	1:24	1:31
SUN/KETHU/SATURN	1:31	1:40
SUN/KETHU/MERCURY	1:40	1:47
SUN/VENUS/VENUS	1:47	1:56
SUN/VENUS/SUN	1:56	1:59
SUN/VENUS/MOON	1:59	2:04
SUN/VENUS/MARS	2:04	2:07
SUN/VENUS/RAHU	2:07	2:15
SUN/VENUS/JUPITER	2:15	2:22
SUN/VENUS/SATURN	2:22	2:31
SUN/VENUS/MERCURY	2:31	2:38
SUN/VENUS/KETHU	2:38	2:42
SUN/SUN/SUN	2:42	2:44
SUN/SUN/MOON	2:44	2:49
SUN/SUN/MARS	2:49	2:52
SUN/SUN/RAHU	2:52	2:55
MERCURY/SUN/RAHU	2:55	3:00
MERCURY/SUN/JUPITER	3:00	3:07
MERCURY/SUN/SATURN	3:07	3:16
MERCURY/SUN/MERCURY	3:16	3:23
MERCURY/SUN/KETHU	3:23	3:26
MERCURY/SUN/VENUS	3:26	3:35
MERCURY/MOON/MOON	3:35	3:40
MERCURY/MOON/MARS	3:40	3:43
MERCURY/MOON/RAHU	3:43	3:51
MERCURY/MOON/JUPITER	3:51	3:58
MERCURY/MOON/SATURN	3:58	4:07
MERCURY/MOON/MERCURY	4:07	4:14
MERCURY/MOON/KETHU	4:14	4:18
MERCURY/MOON/VENUS	4:18	4:27
MERCURY/MOON/SUN	4:27	4:29
...
MOON/SATURN/JUPITER	23:44	23:51
MOON/MERCURY/MERCURY	23:51	23:59
"""
# (You can replace ... above with your full dataset text)

from io import StringIO
reference_df = pd.read_csv(StringIO(data), sep="\t")

# -----------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------
planetary_conditions = ["Moon Bright", "Sun Radiant", "Mercury Active", "Jupiter Wise", "Venus Calm", "Mars Energetic", "Saturn Focused"]
levels = ["Excellent", "Very Good", "Good", "Average", "Poor"]
stars_map = {"Excellent":"⭐⭐⭐⭐⭐","Very Good":"⭐⭐⭐⭐","Good":"⭐⭐⭐","Average":"⭐⭐","Poor":"⭐"}
activities = [
    "Decision-making, teaching, mentoring",
    "Meditation, inner reflection, journaling",
    "Creative work, writing, design",
    "Leadership, presentations, meetings",
    "Travel, communication, negotiation",
    "Research, study, analysis",
    "Relaxation, self-care, socializing"
]
weekday_map = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

# -----------------------------------------------------------------
# UI
# -----------------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now().date())
with col2:
    end_date = st.date_input("End Date", datetime.now().date())

# -----------------------------------------------------------------
# Single Date Selection
# -----------------------------------------------------------------
if start_date == end_date:
    st.subheader(f"🌞 Planetary Movements for {start_date.strftime('%d-%m-%Y')}")
    date_str = start_date.strftime("%d-%m-%Y")
    day_str = weekday_map[start_date.weekday()]
    
    rows = []
    for _, r in reference_df.iterrows():
        level = random.choice(levels)
        stars = stars_map[level]
        condition = random.choice(planetary_conditions)
        activity = random.choice(activities)
        start_t = r["start_time"].strip()
        end_t = r["stop_time"].strip()
        combo = r["combination"]

        rows.append({
            "Date": date_str,
            "Day": day_str,
            "Morning_Timing": f"{start_t} am - {end_t} am",
            "Evening_Timing": "",
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": activity
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# -----------------------------------------------------------------
# Multiple Date Range
# -----------------------------------------------------------------
else:
    st.subheader(f"📆 Planetary Overview — {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}")
    current_date = start_date
    rows = []

    while current_date <= end_date:
        level = random.choice(levels)
        stars = stars_map[level]
        condition = random.choice(planetary_conditions)
        activity = random.choice(activities)
        combo = random.choice(reference_df["combination"].tolist())

        morning_t = f"{random.randint(0,3):02d}:{random.randint(0,59):02d} AM - {random.randint(4,9):02d}:{random.randint(0,59):02d} AM"
        evening_t = f"{random.randint(17,19):02d}:{random.randint(0,59):02d} PM - {random.randint(20,23):02d}:{random.randint(0,59):02d} PM"

        rows.append({
            "Date": current_date.strftime("%d-%m-%Y"),
            "Day": weekday_map[current_date.weekday()],
            "Morning_Timing": morning_t,
            "Evening_Timing": evening_t,
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": activity
        })
        current_date += timedelta(days=1)

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
