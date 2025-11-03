import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# -------------------------------------------
# 🔮 Base Data and Mappings
# -------------------------------------------
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
    "⭐": "Poor",
    "⭐⭐": "Average",
    "⭐⭐⭐": "Good",
    "⭐⭐⭐⭐": "Very Good",
    "⭐⭐⭐⭐⭐": "Excellent"
}

planetary_combinations = [
    "SUN/JUPITER/MERCURY", "MOON/MERCURY/MARS", "VENUS/SATURN/JUPITER",
    "MARS/SUN/MERCURY", "MOON/MERCURY/KETHU", "MERCURY/VENUS/SUN",
    "SATURN/JUPITER/MOON", "SUN/VENUS/MERCURY", "MOON/MARS/JUPITER",
    "MERCURY/SUN/VENUS"
]

# -------------------------------------------
# 🌅 Generate Time Slots
# -------------------------------------------
def generate_time_slots(start_time, end_time, slot_minutes=144):
    slots = []
    current = start_time
    while current < end_time:
        next_time = current + timedelta(minutes=slot_minutes)
        if next_time > end_time:
            next_time = end_time
        slots.append((current.time(), next_time.time()))
        current = next_time
    return slots

# -------------------------------------------
# 🪐 Generate Planetary Data for One Date
# -------------------------------------------
def generate_planetary_data_for_date(current_date, location):
    rows = []
    start_datetime = datetime.combine(current_date, datetime.strptime("00:01", "%H:%M").time())
    end_datetime = datetime.combine(current_date, datetime.strptime("23:59", "%H:%M").time())
    slots = generate_time_slots(start_datetime, end_datetime, slot_minutes=144)

    for i, (start_time, end_time) in enumerate(slots, start=1):
        # Deterministic seed for location + date + slot
        slot_seed = hash(f"{location}_{current_date}_{start_time}_{end_time}") % (10**8)
        random.seed(slot_seed)

        condition = random.choice(planetary_conditions)
        stars = random.choice(list(level_map.keys()))
        level = level_map[stars]
        activity = random.choice(recommended_activities)
        combination = random.choice(planetary_combinations)

        rows.append({
            "Date": current_date.strftime("%d-%m-%Y"),
            "Day": current_date.strftime("%a"),
            "Morning_Timing": f"{start_time.strftime('%I:%M:%S %p')} - {end_time.strftime('%I:%M:%S %p')}",
            "Evening_Timing": "",
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combination,
            "Recommended_Activity": activity,
            "Location": location
        })
    return rows

# -------------------------------------------
# 📅 Generate Data for Multiple Dates
# -------------------------------------------
def generate_planetary_table(start_date, end_date, location):
    data = []

    if start_date == end_date:
        # Single day: full 24h sequence
        data.extend(generate_planetary_data_for_date(start_date, location))
    else:
        # Multi-day summary
        current_date = start_date
        while current_date <= end_date:
            day_seed = hash(f"{location}_{current_date}") % (10**8)
            random.seed(day_seed)

            condition = random.choice(planetary_conditions)
            stars = random.choice(list(level_map.keys()))
            level = level_map[stars]
            activity = random.choice(recommended_activities)
            combination = random.choice(planetary_combinations)

            data.append({
                "Date": current_date.strftime("%d-%m-%Y"),
                "Day": current_date.strftime("%a"),
                "Morning_Timing": "00:01 AM - 03:00 AM",
                "Evening_Timing": "18:00 PM - 23:59 PM",
                "Planetary_Condition": condition,
                "Stars": stars,
                "Level": level,
                "Best_Planetary_Combination": combination,
                "Recommended_Activity": activity,
                "Location": location
            })
            current_date += timedelta(days=1)

    return pd.DataFrame(data)

# -------------------------------------------
# 🎨 Streamlit UI
# -------------------------------------------
st.set_page_config(page_title="🔭 Planetary Energy Predictor", layout="wide")
st.title("🔭 Planetary Energy Predictor")
st.markdown("Predict planetary combinations, energy levels, and activities — now location-based 🌍")

col1, col2, col3 = st.columns(3)
start_date = col1.date_input("Start Date", datetime.now().date())
end_date = col2.date_input("End Date", datetime.now().date())
location = col3.text_input("Enter Location (e.g., Chennai, London, New York)", "Chennai")

if st.button("Generate Table"):
    df = generate_planetary_table(start_date, end_date, location.strip().title())
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download CSV",
        csv,
        f"planetary_energy_{location}_{start_date}_to_{end_date}.csv",
        "text/csv",
        key="download-csv"
    )
