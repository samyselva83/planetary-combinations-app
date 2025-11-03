import csv
import random
from datetime import datetime, timedelta

# ==========================================================
#  CONFIGURABLE LISTS
# ==========================================================

# 🌍 Country list
countries = [
    "India", "USA", "UK", "France", "Germany",
    "Japan", "Australia", "Canada", "Brazil", "South Africa"
]

# 🏙️ City list (parallel mapping for demo purposes)
cities = [
    "Chennai", "New York", "London", "Paris", "Berlin",
    "Tokyo", "Sydney", "Toronto", "São Paulo", "Cape Town"
]

# 🌠 Planetary combinations (from your data)
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

# 🌟 Possible stars & levels
stars = ["⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐"]
levels = ["Average", "Good", "Excellent"]

# 🌙 Planetary conditions
conditions = ["Moon Bright", "Moon Dim", "Sun Strong", "Planetary Balance"]

# 🎯 Recommended activities
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

        # Pick a random location
        idx = i % len(countries)
        country = countries[idx]
        city = cities[idx]

        # Generate unique deterministic timings per date + city
        base_seed = abs(hash(date_str + city)) % 30  # 0–29 minute shift
        morning_shift = base_seed % 30
        evening_shift = (base_seed * 2) % 30

        morning_start = (datetime(date.year, date.month, date.day, 6, 0) + timedelta(minutes=morning_shift)).strftime("%I:%M:%S %p")
        morning_end = (datetime(date.year, date.month, date.day, 7, 0) + timedelta(minutes=morning_shift)).strftime("%I:%M:%S %p")

        evening_start = (datetime(date.year, date.month, date.day, 18, 0) + timedelta(minutes=evening_shift)).strftime("%I:%M:%S %p")
        evening_end = (datetime(date.year, date.month, date.day, 19, 0) + timedelta(minutes=evening_shift)).strftime("%I:%M:%S %p")

        # Pick other attributes randomly
        condition = random.choice(conditions)
        star = random.choice(stars)
        level = random.choice(levels)
        combo = random.choice(planetary_combinations)
        activity = random.choice(activities)

        # Add the row
        rows.append({
            "Date": date_str,
            "Day": day,
            "Country": country,
            "City": city,
            "Morning_Timing": f"{morning_start} - {morning_end}",
            "Evening_Timing": f"{evening_start} - {evening_end}",
            "Planetary_Condition": condition,
            "Stars": star,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": activity
        })
    
    return rows

# ==========================================================
#  MAIN EXECUTION
# ==========================================================

if __name__ == "__main__":
    start_date = datetime.strptime("03-11-2025", "%d-%m-%Y")
    data = generate_planetary_table(start_date, days=10)

    # Save as CSV
    filename = "planetary_schedule.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Planetary schedule generated successfully: {filename}")
    for row in data:
        print(row)
