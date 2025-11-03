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

# Mapping star rating to level
level_map = {
    "⭐": "Poor",
    "⭐⭐": "Average",
    "⭐⭐⭐": "Good",
    "⭐⭐⭐⭐": "Very Good",
    "⭐⭐⭐⭐⭐": "Excellent"
}


# -------------------------------------------
# 🌅 Utility: Generate Time Slots for Single Day
# -------------------------------------------
def generate_time_slots(start_time, end_time, slot_minutes=41):
    """
    Generates time slots from start_time to end_time (inclusive) with slot_minutes duration
    """
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
# 🪐 Generate Planetary Data for Each Slot
# -------------------------------------------
def generate_planetary_data_for_date(current_date):
    rows = []
    start_datetime = datetime.combine(current_date, datetime.strptime("00:01", "%H:%M").time())
    end_datetime = datetime.combine(current_date, datetime.strptime("23:59", "%H:%M").time())

    # Create about 10 slots for the day
    slots = generate_time_slots(start_datetime, end_datetime, slot_minutes=144)  # 24hr/10 = 144 mins

    for i, (start_time, end_time) in enumerate(slots, start=1):
        # Deterministic random seed per slot
        slot_seed = hash(f"{current_date}_{start_time}_{end_time}") % (10**8)
        random.seed(slot_seed)

        # Generate consistent values
        condition = random.choice(planetary_conditions)
        stars = random.choice(list(level_map.keys()))
        level = level_map[stars]
        activity = random.choice(recommended_activities)
        combination = random.choice([
            "SUN/JUPITER/MERCURY", "MOON/MERCURY/MARS", "VENUS/SATURN/JUPITER",
            "MARS/SUN/MERCURY", "MOON/MERCURY/KETHU", "MERCURY/VENUS/SUN",
            "SATURN/JUPITER/MOON", "SUN/VENUS/MERCURY", "MOON/MARS/JUPITER",
            "MERCURY/SUN/VENUS"
        ])

        rows.append({
            "Date": current_date.strftime("%d-%m-%Y"),
            "Day": current_date.strftime("%a"),
            "Morning_Timing": f"{start_time.strftime('%I:%M:%S %p')} - {end_time.strftime('%I:%M:%S %p')}",
            "Evening_Timing": "",
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combination,
            "Recommended_Activity": activity
        })

    return rows


# -------------------------------------------
# 📅 Generate Data for Single or Multiple Dates
# -------------------------------------------
def generate_planetary_table(start_date, end_date):
    data = []

    if start_date == end_date:
        # Single-day detailed breakdown
        current_date = start_date
        data.extend(generate_planetary_data_for_date(current_date))
    else:
        # Multi-day summary (one per date)
        current_date = start_date
        while current_date <= end_date:
            # Deterministic seed per day
            day_seed = hash(str(current_date)) % (10**8)
            random.seed(day_seed)

            condition = random.choice(planetary_conditions)
            stars = random.choice(list(level_map.keys()))
            level = level_map[stars]
            activity = random.choice(recommended_activities)
            combination = random.choice([
                "SUN/JUPITER/MERCURY", "MOON/MERCURY/MARS", "VENUS/SATURN/JUPITER",
                "MARS/SUN/MERCURY", "MOON/MERCURY/KETHU", "MERCURY/VENUS/SUN",
                "SATURN/JUPITER/MOON", "SUN/VENUS/MERCURY", "MOON/MARS/JUPITER",
                "MERCURY/SUN/VENUS"
            ])

            data.append({
                "Date": current_date.strftime("%d-%m-%Y"),
                "Day": current_date.strftime("%a"),
                "Morning_Timing": "00:27 AM - 03:41 AM",
                "Evening_Timing": "18:40 PM - 22:54 PM",
                "Planetary_Condition": condition,
                "Stars": stars,
                "Level": level,
                "Best_Planetary_Combination": combination,
                "Recommended_Activity": activity
            })
            current_date += timedelta(days=1)

    return pd.DataFrame(data)


# -------------------------------------------
# 🎨 Streamlit UI
# -------------------------------------------
st.title("🔭 Planetary Energy Predictor")
st.markdown("Generate daily planetary movement & recommended activities table.")

col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date", datetime.now().date())
end_date = col2.date_input("End Date", datetime.now().date())

if st.button("Generate Table"):
    df = generate_planetary_table(start_date, end_date)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download CSV",
        csv,
        f"planetary_energy_{start_date}_to_{end_date}.csv",
        "text/csv",
        key="download-csv"
    )
