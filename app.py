import streamlit as st
import random
from datetime import datetime, timedelta
import pandas as pd

# ==========================================================
#  CONFIGURABLE LISTS
# ==========================================================
countries = [
    "India", "USA", "UK", "France", "Germany",
    "Japan", "Australia", "Canada", "Brazil", "South Africa"
]

cities = [
    "Chennai", "New York", "London", "Paris", "Berlin",
    "Tokyo", "Sydney", "Toronto", "São Paulo", "Cape Town"
]

planetary_combinations = [
    "MOON/MERCURY/MERCURY", "MOON/MERCURY/KETHU", "MOON/MERCURY/VENUS",
    "MOON/MERCURY/SUN", "MOON/MERCURY/MOON", "MOON/MERCURY/MARS",
    "MOON/MERCURY/RAHU", "MOON/MERCURY/JUPITER", "MOON/MERCURY/SATURN",
    "SUN/KETHU/KETHU", "SUN/KETHU/VENUS", "SUN/KETHU/SUN",
    "SUN/KETHU/MOON", "SUN/KETHU/MARS", "SUN/KETHU/RAHU",
    "SUN/KETHU/JUPITER", "SUN/KETHU/SATURN", "SUN/KETHU/MERCURY",
    "SUN/VENUS/VENUS", "SUN/VENUS/SUN", "SUN/VENUS/MOON",
    "SUN/VENUS/MARS", "SUN/VENUS/RAHU", "SUN/VENUS/JUPITER",
    "SUN/VENUS/SATURN", "SUN/VENUS/MERCURY", "SUN/VENUS/KETHU",
    "SUN/SUN/SUN", "SUN/SUN/MOON", "SUN/SUN/MARS", "SUN/SUN/RAHU"
]

stars = ["⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐"]
levels = ["Average", "Good", "Excellent"]
conditions = ["Moon Bright", "Moon Dim", "Sun Strong", "Planetary Balance"]
activities = [
    "Decision-making, teaching, mentoring",
    "Travel, new beginnings, business planning",
    "Meditation, creativity, reflection",
    "Communication, collaboration, teamwork",
    "Analysis, documentation, finance review"
]

# ==========================================================
#  FUNCTION TO GENERATE DATA
# ==========================================================
def generate_planetary_table(start_date, days=10):
    rows = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        date_str = date.strftime("%d-%m-%Y")
        day = date.strftime("%a")

        idx = i % len(countries)
        country = countries[idx]
        city = cities[idx]

        # Deterministic but unique timing per city/date
        base_seed = abs(hash(date_str + city)) % 30
        morning_shift = base_seed % 30
        evening_shift = (base_seed * 2) % 30

        morning_start = (datetime(date.year, date.month, date.day, 6, 0) + timedelta(minutes=morning_shift)).strftime("%I:%M:%S %p")
        morning_end = (datetime(date.year, date.month, date.day, 7, 0) + timedelta(minutes=morning_shift)).strftime("%I:%M:%S %p")

        evening_start = (datetime(date.year, date.month, date.day, 18, 0) + timedelta(minutes=evening_shift)).strftime("%I:%M:%S %p")
        evening_end = (datetime(date.year, date.month, date.day, 19, 0) + timedelta(minutes=evening_shift)).strftime("%I:%M:%S %p")

        rows.append({
            "Date": date_str,
            "Day": day,
            "Country": country,
            "City": city,
            "Morning_Timing": f"{morning_start} - {morning_end}",
            "Evening_Timing": f"{evening_start} - {evening_end}",
            "Planetary_Condition": random.choice(conditions),
            "Stars": random.choice(stars),
            "Level": random.choice(levels),
            "Best_Planetary_Combination": random.choice(planetary_combinations),
            "Recommended_Activity": random.choice(activities)
        })
    return pd.DataFrame(rows)

# ==========================================================
#  STREAMLIT UI
# ==========================================================
st.set_page_config(page_title="🌙 Planetary Combinations", layout="wide")

st.title("🌟 Planetary Combination Generator")
st.write("Generate deterministic planetary schedules by location and date.")

# Input fields
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Select start date", datetime(2025, 11, 3))
with col2:
    days = st.number_input("Number of days", min_value=1, max_value=365, value=10)

# Generate button
if st.button("Generate Planetary Schedule"):
    df = generate_planetary_table(start_date=datetime.combine(start_date, datetime.min.time()), days=days)
    
    st.success(f"✅ Generated planetary schedule for {days} days starting from {start_date.strftime('%d-%m-%Y')}")
    st.dataframe(df, use_container_width=True)

    # Download option
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="planetary_schedule.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("Created by Smart Agent AI 🔮")

