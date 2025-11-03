import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# -------------------------------------------
# Fixed Planetary Combinations (from your list)
# -------------------------------------------
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

# -------------------------------------------
# Supporting Information
# -------------------------------------------
planetary_conditions = {
    "SUN": "Radiant", "MOON": "Bright", "MARS": "Energetic",
    "MERCURY": "Active", "JUPITER": "Wise", "VENUS": "Calm",
    "SATURN": "Focused", "RAHU": "Mysterious", "KETHU": "Intuitive"
}

stars_map = {
    1: "⭐",
    2: "⭐⭐",
    3: "⭐⭐⭐",
    4: "⭐⭐⭐⭐",
    5: "⭐⭐⭐⭐⭐"
}

level_map = {
    "⭐": "Poor",
    "⭐⭐": "Average",
    "⭐⭐⭐": "Good",
    "⭐⭐⭐⭐": "Very Good",
    "⭐⭐⭐⭐⭐": "Excellent"
}

activities = [
    "Meditation or spiritual work",
    "Creative writing or design",
    "Decision-making and leadership",
    "Teaching or learning",
    "Planning new ventures",
    "Physical exercise or travel",
    "Relaxation or family time"
]

# -------------------------------------------
# Helper: Generate Time Slots
# -------------------------------------------
def generate_fixed_time_slots(start_time, slot_minutes, total_slots):
    slots = []
    current = start_time
    for _ in range(total_slots):
        end_time = current + timedelta(minutes=slot_minutes)
        slots.append((current.time(), end_time.time()))
        current = end_time
    return slots


# -------------------------------------------
# Generate Planetary Data (Single Date)
# -------------------------------------------
def generate_single_date_data(date):
    rows = []
    start_datetime = datetime.combine(date, datetime.strptime("00:01", "%H:%M").time())
    total_combinations = len(planetary_combinations)
    slot_minutes = int((24 * 60) / total_combinations)  # even spacing
    slots = generate_fixed_time_slots(start_datetime, slot_minutes, total_combinations)

    for (start_time, end_time), combo in zip(slots, planetary_combinations):
        main_planet = combo.split("/")[0]
        condition = f"{main_planet} {planetary_conditions.get(main_planet, '')}"

        # Deterministic stars based on combo name hash
        stars = stars_map[(abs(hash(combo)) % 5) + 1]
        level = level_map[stars]

        # Activity also fixed by hash of combo
        act = activities[abs(hash(combo)) % len(activities)]

        rows.append({
            "Date": date.strftime("%d-%m-%Y"),
            "Day": date.strftime("%a"),
            "Timing": f"{start_time.strftime('%I:%M:%S %p')} - {end_time.strftime('%I:%M:%S %p')}",
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": act
        })
    return rows


# -------------------------------------------
# Multi-Date Summary (simplified)
# -------------------------------------------
def generate_multi_date_summary(start_date, end_date):
    data = []
    current = start_date
    while current <= end_date:
        combo = planetary_combinations[abs(hash(str(current))) % len(planetary_combinations)]
        main_planet = combo.split("/")[0]
        condition = f"{main_planet} {planetary_conditions.get(main_planet, '')}"
        stars = stars_map[(abs(hash(combo)) % 5) + 1]
        level = level_map[stars]
        act = activities[abs(hash(combo)) % len(activities)]

        data.append({
            "Date": current.strftime("%d-%m-%Y"),
            "Day": current.strftime("%a"),
            "Morning_Timing": "00:01 AM - 02:59 AM",
            "Evening_Timing": "18:00 PM - 23:59 PM",
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": act
        })
        current += timedelta(days=1)
    return data


# -------------------------------------------
# Streamlit UI
# -------------------------------------------
st.title("🌌 Planetary Combination Energy Viewer")

col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date", datetime.now().date())
end_date = col2.date_input("End Date", datetime.now().date())

if st.button("Generate Table"):
    if start_date == end_date:
        df = pd.DataFrame(generate_single_date_data(start_date))
    else:
        df = pd.DataFrame(generate_multi_date_summary(start_date, end_date))

    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, f"planetary_{start_date}_to_{end_date}.csv", "text/csv")
