import pandas as pd
import hashlib
import math
from datetime import datetime, timedelta

# --- Deterministic helper functions ---

def deterministic_index(text, mod):
    """Stable index from text using SHA256 hash."""
    h = hashlib.sha256(text.encode()).hexdigest()
    return int(h[:8], 16) % mod

def time_from_angle(angle, base_hour, amplitude):
    """Generate deterministic time offset (for sunrise/sunset variations)."""
    minutes = base_hour * 60 + amplitude * math.sin(math.radians(angle))
    hour = int(minutes // 60)
    minute = int(minutes % 60)
    return hour, minute

# --- Planetary datasets ---

planetary_conditions = [
    "Sun Radiant", "Moon Serene", "Mars Energetic", "Mercury Active",
    "Jupiter Wise", "Venus Harmonious", "Saturn Steady", "Rahu Chaotic", "Kethu Subtle"
]

planetary_combinations = [
    "MOON/MERCURY/MERCURY", "MOON/MERCURY/KETHU", "MOON/MERCURY/VENUS",
    "MOON/MERCURY/SUN", "MOON/MERCURY/MOON", "MOON/MERCURY/MARS",
    "MOON/MERCURY/RAHU", "MOON/MERCURY/JUPITER", "MOON/MERCURY/SATURN",
    "SUN/KETHU/KETHU", "SUN/KETHU/VENUS", "SUN/KETHU/SUN", "SUN/KETHU/MOON",
    "SUN/KETHU/MARS", "SUN/KETHU/RAHU", "SUN/KETHU/JUPITER", "SUN/KETHU/SATURN",
    "SUN/KETHU/MERCURY", "SUN/VENUS/VENUS", "SUN/VENUS/SUN", "SUN/VENUS/MOON",
    "SUN/VENUS/MARS", "SUN/VENUS/RAHU", "SUN/VENUS/JUPITER", "SUN/VENUS/SATURN",
    "SUN/VENUS/MERCURY", "SUN/VENUS/KETHU", "SUN/SUN/SUN", "SUN/SUN/MOON",
    "SUN/SUN/MARS", "SUN/SUN/RAHU"
]

recommended_activities = [
    "Leadership", "Meditation", "Creative work", "Research", "Communication",
    "Music or writing", "Physical training", "Travel planning", "Finance review"
]

level_map = {
    1: "Poor",
    2: "Average",
    3: "Good",
    4: "Very Good",
    5: "Excellent"
}

# --- Main deterministic generator ---

def generate_planetary_table(start_date, end_date, location):
    all_data = []
    current_date = start_date

    while current_date <= end_date:
        # Deterministic parameters
        day_of_year = current_date.timetuple().tm_yday
        loc_value = sum(ord(c) for c in location.lower())
        angle = (day_of_year * 0.9856 + loc_value) % 360  # Earth-like orbital path

        # Calculate sunrise-like offset (approx)
        base_hour, base_minute = time_from_angle(angle, base_hour=0, amplitude=90)
        start_time = datetime.combine(current_date, datetime.min.time()) + timedelta(
            hours=base_hour, minutes=base_minute
        )

        # 12 deterministic 2-hour slots
        slot_duration = 120  # minutes
        for i in range(12):
            slot_start = start_time + timedelta(minutes=i * slot_duration)
            slot_end = slot_start + timedelta(minutes=slot_duration - 1)

            # Deterministic planetary data
            cond_idx = deterministic_index(f"{location}_{current_date}_{i}_cond", len(planetary_conditions))
            comb_idx = deterministic_index(f"{location}_{current_date}_{i}_combo", len(planetary_combinations))
            act_idx = deterministic_index(f"{location}_{current_date}_{i}_act", len(recommended_activities))
            star_count = (deterministic_index(f"{location}_{current_date}_{i}_stars", 5) + 1)

            condition = planetary_conditions[cond_idx]
            stars = "⭐" * star_count
            level = level_map[star_count]
            combination = planetary_combinations[comb_idx]
            activity = recommended_activities[act_idx]

            all_data.append({
                "Date": current_date.strftime("%d-%m-%Y"),
                "Day": current_date.strftime("%a"),
                "Time Slot": f"{slot_start.strftime('%I:%M %p')} - {slot_end.strftime('%I:%M %p')}",
                "Planetary Condition": condition,
                "Stars": stars,
                "Level": level,
                "Best Planetary Combination": combination,
                "Recommended Activity": activity,
                "Location": location
            })

        current_date += timedelta(days=1)

    return pd.DataFrame(all_data)
