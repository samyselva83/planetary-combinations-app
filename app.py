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

# ✅ Your expanded planetary combinations list
planetary_combinations = [
    "MOON/MERCURY/MERCURY", "MOON/MERCURY/KETHU", "MOON/MERCURY/VENUS", "MOON/MERCURY/SUN",
    "MOON/MERCURY/MOON", "MOON/MERCURY/MARS", "MOON/MERCURY/RAHU", "MOON/MERCURY/JUPITER",
    "MOON/MERCURY/SATURN", "SUN/KETHU/KETHU", "SUN/KETHU/VENUS", "SUN/KETHU/SUN",
    "SUN/KETHU/MOON", "SUN/KETHU/MARS", "SUN/KETHU/RAHU", "SUN/KETHU/JUPITER",
    "SUN/KETHU/SATURN", "SUN/KETHU/MERCURY", "SUN/VENUS/VENUS", "SUN/VENUS/SUN",
    "SUN/VENUS/MOON", "SUN/VENUS/MARS", "SUN/VENUS/RAHU", "SUN/VENUS/JUPITER",
    "SUN/VENUS/SATURN", "SUN/VENUS/MERCURY", "SUN/VENUS/KETHU", "SUN/SUN/SUN",
    "SUN/SUN/MOON", "SUN/SUN/MARS", "SUN/SUN/RAHU", "MERCURY/SUN/RAHU", "MERCURY/SUN/JUPITER",
    "MERCURY/SUN/SATURN", "MERCURY/SUN/MERCURY", "MERCURY/SUN/KETHU", "MERCURY/SUN/VENUS",
    "MERCURY/MOON/MOON", "MERCURY/MOON/MARS", "MERCURY/MOON/RAHU", "MERCURY/MOON/JUPITER",
    "MERCURY/MOON/SATURN", "MERCURY/MOON/MERCURY", "MERCURY/MOON/KETHU", "MERCURY/MOON/VENUS",
    "MERCURY/MOON/SUN", "MERCURY/MARS/MARS", "MERCURY/MARS/RAHU", "MERCURY/MARS/JUPITER",
    "MERCURY/MARS/SATURN", "VENUS/MARS/MERCURY", "VENUS/MARS/KETHU", "VENUS/MARS/VENUS",
    "VENUS/MARS/SUN", "VENUS/MARS/MOON", "VENUS/RAHU/RAHU", "VENUS/RAHU/JUPITER",
    "VENUS/RAHU/SATURN", "VENUS/RAHU/MERCURY", "VENUS/RAHU/KETHU", "VENUS/RAHU/VENUS",
    "VENUS/RAHU/SUN", "VENUS/RAHU/MOON", "VENUS/RAHU/MARS", "VENUS/JUPITER/JUPITER",
    "VENUS/JUPITER/SATURN", "VENUS/JUPITER/MERCURY", "VENUS/JUPITER/KETHU", "VENUS/JUPITER/VENUS",
    "VENUS/JUPITER/SUN", "VENUS/JUPITER/MOON", "MARS/JUPITER/MOON", "MARS/JUPITER/MARS",
    "MARS/JUPITER/RAHU", "MARS/SATURN/SATURN", "MARS/SATURN/MERCURY", "MARS/SATURN/KETHU",
    "MARS/SATURN/VENUS", "MARS/SATURN/SUN", "MARS/SATURN/MOON", "MARS/SATURN/MARS",
    "MARS/SATURN/RAHU", "MARS/SATURN/JUPITER", "MARS/MERCURY/MERCURY", "MARS/MERCURY/KETHU",
    "MARS/MERCURY/VENUS", "MARS/MERCURY/SUN", "MARS/MERCURY/MOON", "MARS/MERCURY/MARS",
    "MARS/MERCURY/RAHU", "MARS/MERCURY/JUPITER", "MARS/MERCURY/SATURN", "JUPITER/KETHU/KETHU",
    "JUPITER/KETHU/VENUS", "JUPITER/KETHU/SUN", "JUPITER/KETHU/MOON", "JUPITER/KETHU/MARS",
    "JUPITER/KETHU/RAHU", "JUPITER/KETHU/JUPITER", "JUPITER/KETHU/SATURN", "JUPITER/KETHU/MERCURY",
    "JUPITER/VENUS/VENUS", "JUPITER/VENUS/SUN", "JUPITER/VENUS/MOON", "JUPITER/VENUS/MARS",
    "JUPITER/VENUS/RAHU", "JUPITER/VENUS/JUPITER", "JUPITER/VENUS/SATURN", "JUPITER/VENUS/MERCURY",
    "JUPITER/VENUS/KETHU", "JUPITER/SUN/SUN", "JUPITER/SUN/MOON", "JUPITER/SUN/MARS",
    "JUPITER/SUN/RAHU", "SATURN/SUN/RAHU", "SATURN/SUN/JUPITER", "SATURN/SUN/SATURN",
    "SATURN/SUN/MERCURY", "SATURN/SUN/KETHU", "SATURN/SUN/VENUS", "SATURN/MOON/MOON",
    "SATURN/MOON/MARS", "SATURN/MOON/RAHU", "SATURN/MOON/JUPITER", "SATURN/MOON/SATURN",
    "SATURN/MOON/MERCURY", "SATURN/MOON/KETHU", "SATURN/MOON/VENUS", "SATURN/MOON/SUN",
    "SATURN/MARS/MARS", "SATURN/MARS/RAHU", "SATURN/MARS/JUPITER", "SATURN/MARS/SATURN",
    "SATURN/MARS/MERCURY", "SATURN/MARS/KETHU", "SATURN/MARS/VENUS", "SATURN/MARS/SUN",
    "SATURN/MARS/MOON", "SATURN/RAHU/RAHU", "SATURN/RAHU/JUPITER", "SATURN/RAHU/SATURN",
    "SATURN/RAHU/MERCURY", "SATURN/RAHU/KETHU", "SATURN/RAHU/VENUS", "SATURN/RAHU/SUN",
    "SATURN/RAHU/MOON", "SATURN/RAHU/MARS", "SATURN/JUPITER/JUPITER", "SATURN/JUPITER/SATURN",
    "SATURN/JUPITER/MERCURY", "SATURN/JUPITER/KETHU", "SATURN/JUPITER/VENUS", "SATURN/JUPITER/SUN",
    "SATURN/JUPITER/MOON", "JUPITER/JUPITER/MOON", "JUPITER/JUPITER/MARS", "JUPITER/JUPITER/RAHU",
    "JUPITER/SATURN/SATURN", "JUPITER/SATURN/MERCURY", "JUPITER/SATURN/KETHU", "JUPITER/SATURN/VENUS",
    "JUPITER/SATURN/SUN", "JUPITER/SATURN/MOON", "JUPITER/SATURN/MARS", "JUPITER/SATURN/RAHU",
    "JUPITER/SATURN/JUPITER", "JUPITER/MERCURY/MERCURY", "JUPITER/MERCURY/KETHU", "JUPITER/MERCURY/VENUS",
    "JUPITER/MERCURY/SUN", "JUPITER/MERCURY/MOON", "JUPITER/MERCURY/MARS", "JUPITER/MERCURY/RAHU",
    "JUPITER/MERCURY/JUPITER", "JUPITER/MERCURY/SATURN", "MARS/KETHU/KETHU", "MARS/KETHU/VENUS",
    "MARS/KETHU/SUN", "MARS/KETHU/MOON", "MARS/KETHU/MARS", "MARS/KETHU/RAHU", "MARS/KETHU/JUPITER",
    "MARS/KETHU/SATURN", "MARS/KETHU/MERCURY", "MARS/VENUS/VENUS", "MARS/VENUS/SUN", "MARS/VENUS/MOON",
    "MARS/VENUS/MARS", "MARS/VENUS/RAHU", "MARS/VENUS/JUPITER", "MARS/VENUS/SATURN", "MARS/VENUS/MERCURY",
    "MARS/VENUS/KETHU", "MARS/SUN/SUN", "MARS/SUN/MOON", "MARS/SUN/MARS", "MARS/SUN/RAHU",
    "VENUS/SUN/RAHU", "VENUS/SUN/JUPITER", "VENUS/SUN/SATURN", "VENUS/SUN/MERCURY", "VENUS/SUN/KETHU",
    "VENUS/SUN/VENUS", "VENUS/MOON/MOON", "VENUS/MOON/MARS", "VENUS/MOON/RAHU", "VENUS/MOON/JUPITER",
    "VENUS/MOON/SATURN", "VENUS/MOON/MERCURY", "VENUS/MOON/KETHU", "VENUS/MOON/VENUS", "VENUS/MOON/SUN",
    "VENUS/MARS/MARS", "VENUS/MARS/RAHU", "VENUS/MARS/JUPITER", "VENUS/MARS/SATURN", "MERCURY/MARS/MERCURY",
    "MERCURY/MARS/KETHU", "MERCURY/MARS/VENUS", "MERCURY/MARS/SUN", "MERCURY/MARS/MOON", "MERCURY/RAHU/RAHU",
    "MERCURY/RAHU/JUPITER", "MERCURY/RAHU/SATURN", "MERCURY/RAHU/MERCURY", "MERCURY/RAHU/KETHU",
    "MERCURY/RAHU/VENUS", "MERCURY/RAHU/SUN", "MERCURY/RAHU/MOON", "MERCURY/RAHU/MARS", "MERCURY/JUPITER/JUPITER",
    "MERCURY/JUPITER/SATURN", "MERCURY/JUPITER/MERCURY", "MERCURY/JUPITER/KETHU", "MERCURY/JUPITER/VENUS",
    "MERCURY/JUPITER/SUN", "MERCURY/JUPITER/MOON", "MOON/JUPITER/MOON", "MOON/JUPITER/MARS",
    "MOON/JUPITER/RAHU", "MOON/SATURN/SATURN", "MOON/SATURN/MERCURY", "MOON/SATURN/KETHU",
    "MOON/SATURN/VENUS", "MOON/SATURN/SUN", "MOON/SATURN/MOON", "MOON/SATURN/MARS", "MOON/SATURN/RAHU",
    "MOON/SATURN/JUPITER", "MOON/MERCURY/MERCURY"
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

    for start_time, end_time in slots:
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
            "Timing": f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}",
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
        data.extend(generate_planetary_data_for_date(start_date, location))
    else:
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
                "Evening_Timing": "06:00 PM - 11:59 PM",
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
st.markdown("Predict planetary combinations, energy levels, and activities — location-based 🌍")

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
