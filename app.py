import pandas as pd
from datetime import datetime, timedelta

# 🌙 Fixed planetary combination list for single-date generation
FIXED_PLANETARY_LIST = [
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
    "MARS/VENUS/KETHU", "MARS/SUN/SUN", "MARS/SUN/MOON", "MARS/SUN/MARS", "MARS/SUN/RAHU", "VENUS/SUN/RAHU",
    "VENUS/SUN/JUPITER", "VENUS/SUN/SATURN", "VENUS/SUN/MERCURY", "VENUS/SUN/KETHU", "VENUS/SUN/VENUS",
    "VENUS/MOON/MOON", "VENUS/MOON/MARS", "VENUS/MOON/RAHU", "VENUS/MOON/JUPITER", "VENUS/MOON/SATURN",
    "VENUS/MOON/MERCURY", "VENUS/MOON/KETHU", "VENUS/MOON/VENUS", "VENUS/MOON/SUN", "VENUS/MARS/MARS",
    "VENUS/MARS/RAHU", "VENUS/MARS/JUPITER", "VENUS/MARS/SATURN", "MERCURY/MARS/MERCURY",
    "MERCURY/MARS/KETHU", "MERCURY/MARS/VENUS", "MERCURY/MARS/SUN", "MERCURY/MARS/MOON",
    "MERCURY/RAHU/RAHU", "MERCURY/RAHU/JUPITER", "MERCURY/RAHU/SATURN", "MERCURY/RAHU/MERCURY",
    "MERCURY/RAHU/KETHU", "MERCURY/RAHU/VENUS", "MERCURY/RAHU/SUN", "MERCURY/RAHU/MOON",
    "MERCURY/RAHU/MARS", "MERCURY/JUPITER/JUPITER", "MERCURY/JUPITER/SATURN", "MERCURY/JUPITER/MERCURY",
    "MERCURY/JUPITER/KETHU", "MERCURY/JUPITER/VENUS", "MERCURY/JUPITER/SUN", "MERCURY/JUPITER/MOON",
    "MOON/JUPITER/MOON", "MOON/JUPITER/MARS", "MOON/JUPITER/RAHU", "MOON/SATURN/SATURN",
    "MOON/SATURN/MERCURY", "MOON/SATURN/KETHU", "MOON/SATURN/VENUS", "MOON/SATURN/SUN",
    "MOON/SATURN/MOON", "MOON/SATURN/MARS", "MOON/SATURN/RAHU", "MOON/SATURN/JUPITER", "MOON/MERCURY/MERCURY"
]

# ⭐️ Deterministic mappings (same for all runs)
STAR_MAP = {
    "MOON": "⭐⭐⭐⭐",
    "SUN": "⭐⭐⭐⭐⭐",
    "MARS": "⭐⭐⭐",
    "MERCURY": "⭐⭐⭐⭐",
    "JUPITER": "⭐⭐⭐⭐⭐",
    "VENUS": "⭐⭐⭐⭐",
    "SATURN": "⭐⭐⭐",
    "RAHU": "⭐⭐",
    "KETHU": "⭐⭐"
}

LEVEL_MAP = {
    "⭐⭐⭐⭐⭐": "Excellent",
    "⭐⭐⭐⭐": "Very Good",
    "⭐⭐⭐": "Average",
    "⭐⭐": "Challenging"
}

ACTIVITY_MAP = {
    "MOON": "Creative thinking or emotional healing.",
    "SUN": "Leadership or decision making.",
    "MARS": "Action, physical work, or competition.",
    "MERCURY": "Communication, teaching, or analysis.",
    "JUPITER": "Learning, teaching, or wisdom.",
    "VENUS": "Art, beauty, and harmony activities.",
    "SATURN": "Discipline, planning, or responsibility.",
    "RAHU": "Innovation, tech work, or exploration.",
    "KETHU": "Meditation, spirituality, or detachment."
}

# 🌞 Generate planetary table
def generate_planetary_table(start_date: str, end_date: str):
    start = datetime.strptime(start_date, "%d-%m-%Y")
    end = datetime.strptime(end_date, "%d-%m-%Y")

    if start == end:
        # Single-date → fixed planetary list, full-day split
        total_minutes = 24 * 60 - 1
        step = total_minutes // len(FIXED_PLANETARY_LIST)
        current_time = datetime.combine(start.date(), datetime.strptime("00:01", "%H:%M").time())

        rows = []
        for combo in FIXED_PLANETARY_LIST:
            planet = combo.split("/")[-1]
            start_time = current_time.strftime("%I:%M %p")
            end_time = (current_time + timedelta(minutes=step)).strftime("%I:%M %p")
            stars = STAR_MAP.get(planet, "⭐⭐⭐")
            level = LEVEL_MAP[stars]
            activity = ACTIVITY_MAP.get(planet, "General activities.")

            rows.append([
                start.strftime("%d-%m-%Y"), start.strftime("%a"),
                f"{start_time} - {end_time}", f"{planet} Influence",
                stars, level, combo, activity
            ])
            current_time += timedelta(minutes=step)

        df = pd.DataFrame(rows, columns=[
            "Date", "Day", "Time Slot", "Planetary_Condition",
            "Stars", "Level", "Planetary_Combination", "Recommended_Activity"
        ])
        df.to_csv("planetary_single_date.csv", index=False)
        print("✅ Single-date planetary file saved as 'planetary_single_date.csv'")

    else:
        # Multi-date → existing logic
        print("🪐 Multiple dates selected — using dynamic logic (as before).")
        # (You can reuse your multi-date dynamic function here.)

# Example Usage:
generate_planetary_table("03-11-2025", "03-11-2025")  # Single date example
# generate_planetary_table("03-11-2025", "05-11-2025")  # Multi-date example
