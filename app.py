# app.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
import hashlib
import math

# Optional astronomical accuracy (skyfield). If not available we fallback.
USE_SKYFIELD = True
try:
    from skyfield.api import Loader, N, W, wgs84, load
    from skyfield.api import EarthSatellite
    SKYFIELD_OK = True
except Exception:
    SKYFIELD_OK = False
    USE_SKYFIELD = False

# ---------------------------
# Fallback city coordinates
# ---------------------------
CITY_COORDS = {
    "chennai": (13.0827, 80.2707),
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "bangalore": (12.9716, 77.5946),
    "hyderabad": (17.3850, 78.4867),
    "kolkata": (22.5726, 88.3639),
    "coimbatore": (11.0168, 76.9558),
    "madurai": (9.9252, 78.1198),
    "pune": (18.5204, 73.8567),
    "tirunelveli": (8.7139, 77.7567),
}

# ---------------------------
# Big list of combinations (use your full list)
# (Truncated here to keep code compact — replace with your full list if needed)
# ---------------------------
PLANETARY_COMBINATIONS_FULL = [
    "MOON/MERCURY/MERCURY","MOON/MERCURY/KETHU","MOON/MERCURY/VENUS","MOON/MERCURY/SUN",
    "MOON/MERCURY/MOON","MOON/MERCURY/MARS","MOON/MERCURY/RAHU","MOON/MERCURY/JUPITER",
    "MOON/MERCURY/SATURN","SUN/KETHU/KETHU","SUN/KETHU/VENUS","SUN/KETHU/SUN",
    "SUN/KETHU/MOON","SUN/KETHU/MARS","SUN/KETHU/RAHU","SUN/KETHU/JUPITER",
    "SUN/KETHU/SATURN","SUN/KETHU/MERCURY","SUN/VENUS/VENUS","SUN/VENUS/SUN",
    "SUN/VENUS/MOON","SUN/VENUS/MARS","SUN/VENUS/RAHU","SUN/VENUS/JUPITER",
    "SUN/VENUS/SATURN","SUN/VENUS/MERCURY","SUN/VENUS/KETHU","SUN/SUN/SUN",
    "SUN/SUN/MOON","SUN/SUN/MARS","SUN/SUN/RAHU","MERCURY/SUN/RAHU",
    "MERCURY/SUN/JUPITER","MERCURY/SUN/SATURN","MERCURY/SUN/MERCURY","MERCURY/SUN/KETHU",
    "MERCURY/SUN/VENUS","MERCURY/MOON/MOON","MERCURY/MOON/MARS","MERCURY/MOON/RAHU",
    "MERCURY/MOON/JUPITER","MERCURY/MOON/SATURN","MERCURY/MOON/MERCURY",
    "MERCURY/MOON/KETHU","MERCURY/MOON/VENUS","MERCURY/MOON/SUN","MERCURY/MARS/MARS",
    "MERCURY/MARS/RAHU","MERCURY/MARS/JUPITER","MERCURY/MARS/SATURN",
    # ... (you said you have a very large list — include whole list here)
    # For demo, we'll repeat list to make it long enough
]
# ensure lots of entries by repeating (in case user didn't paste full list into code)
if len(PLANETARY_COMBINATIONS_FULL) < 200:
    PLANETARY_COMBINATIONS_FULL = PLANETARY_COMBINATIONS_FULL * ((200 // len(PLANETARY_COMBINATIONS_FULL)) + 1)

# ---------------------------
# Helper deterministic functions
# ---------------------------
def deterministic_index(text, mod):
    """Stable index from text using SHA256 hex -> integer -> mod."""
    h = hashlib.sha256(text.encode()).hexdigest()
    return int(h[:16], 16) % mod

def deterministic_choice(text, arr):
    return arr[deterministic_index(text, len(arr))]

# ---------------------------
# (Optional) get moon longitude using skyfield (if available)
# ---------------------------
def get_moon_longitude_skyfield(lat, lon, date):
    """Return Moon ecliptic longitude (degrees) at midnight local time using skyfield.
       Returns None if skyfield not available or ephemeris cannot be loaded."""
    if not SKYFIELD_OK:
        return None
    try:
        # load ephemeris (this may download if not present)
        load = Loader('/tmp/skyfield-data')
        ts = load.timescale()
        # try to load 'de421.bsp' or 'de440s' if available
        try:
            eph = load('de421.bsp')
        except Exception:
            eph = load('de440s.bsp') if 'de440s.bsp' in load.open_url else load('de421.bsp')
        earth = eph['earth']
        moon = eph['moon']
        # create an observer at lat/lon (approx)
        observer = wgs84.latlon(lat, lon)
        # compute midnight UTC for local date approximation
        # We'll use 00:00 local time -> convert to UTC by assuming no timezone offset (approx).
        # For better accuracy you should convert local timezone to UTC; here we approximate.
        t = ts.utc(date.year, date.month, date.day, 0, 0, 0)
        astrom = earth.at(t).observe(moon).ecliptic_position()
        lon_deg = math.degrees(math.atan2(astrom[1].au, astrom[0].au)) % 360
        return lon_deg
    except Exception:
        return None

# ---------------------------
# Micro-slot generator for single-day detailed output
# ---------------------------
def generate_day_micro_slots(date, city):
    """Generate minute-level slots across 00:01 -> 23:59 using the combination sequence.
       Durations for each combo are deterministic derived from hash(combo+date+city)."""
    city_key = city.strip().lower()
    lat, lon = CITY_COORDS.get(city_key, (13.0827, 80.2707))

    # optionally use moon longitude to choose starting offset in the combination list
    moon_lon = get_moon_longitude_skyfield(lat, lon, date) if USE_SKYFIELD else None
    if moon_lon is None:
        # fallback offset deterministically from city+date
        start_offset = deterministic_index(f"{city}_{date}_startoffset", len(PLANETARY_COMBINATIONS_FULL))
    else:
        # convert moon longitude to nakshatra index (27)
        nak = int(moon_lon / (360 / 27)) % 27
        # use nak to shift starting offset
        start_offset = nak % len(PLANETARY_COMBINATIONS_FULL)

    # We will fill minutes from 00:01 to 23:59 (inclusive) -> total_minutes
    start_dt = datetime.combine(date, time(0,1))
    end_dt = datetime.combine(date, time(23,59))
    total_minutes = int((end_dt - start_dt).total_seconds() // 60) + 1

    rows = []
    minute_cursor = 0
    combo_idx = start_offset
    # We'll loop and assign durations until all minutes consumed
    while minute_cursor < total_minutes:
        combo = PLANETARY_COMBINATIONS_FULL[combo_idx % len(PLANETARY_COMBINATIONS_FULL)]
        # determine duration minutes deterministically between 2 and 12 (or use range you prefer)
        # formula: 2 + (hash % 11) => 2..12 minutes
        dur_mod = deterministic_index(f"{combo}_{date}_{city}_dur", 11)
        duration = 2 + dur_mod  # 2..12 minutes
        # cap duration if remaining minutes less than duration
        remaining = total_minutes - minute_cursor
        if duration > remaining:
            duration = remaining

        slot_start = start_dt + timedelta(minutes=minute_cursor)
        slot_end = slot_start + timedelta(minutes=duration - 1)  # inclusive end minute

        # compute deterministic attributes per slot
        seed = f"{combo}_{date}_{city}_{minute_cursor}"
        condition = deterministic_choice(seed + "_cond", [
            "Sun Radiant", "Moon Bright", "Mars Energetic", "Mercury Active",
            "Jupiter Wise", "Venus Calm", "Saturn Focused", "Rahu Wild", "Kethu Subtle"
        ])
        star_count = (deterministic_index(seed + "_stars", 5) + 1)  # 1..5
        stars = "⭐" * star_count
        level_map = {1:"Poor",2:"Average",3:"Good",4:"Very Good",5:"Excellent"}
        level = level_map.get(star_count, "Good")
        # recommended activity map (deterministic)
        activities = [
            "Decision-making, teaching, mentoring",
            "Creative work, music, or writing",
            "Meditation, mindfulness, self-reflection",
            "Leadership, presentations, planning",
            "Research, analysis, and deep work",
            "Relaxation and family time",
            "Physical exercise or travel"
        ]
        activity = deterministic_choice(seed + "_act", activities)

        rows.append({
            "Date": date.strftime("%d-%m-%Y"),
            "Day": date.strftime("%a"),
            "start_time": slot_start.strftime("%H:%M"),
            "stop_time": slot_end.strftime("%H:%M"),
            "Time Display": f"{slot_start.strftime('%I:%M %p')} - {slot_end.strftime('%I:%M %p')}",
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": activity,
            "Location": city.title()
        })

        minute_cursor += duration
        combo_idx += 1

    df = pd.DataFrame(rows)
    return df

# ---------------------------
# Multi-day summary generator (10 blocks per day)
# ---------------------------
def generate_multi_day_summary(start_date, end_date, city):
    rows = []
    current = start_date
    while current <= end_date:
        seed_base = f"{city}_{current}"
        # create ~10 deterministic blocks (morning -> evening)
        for i in range(10):
            combo = deterministic_choice(seed_base + f"_combo_{i}", PLANETARY_COMBINATIONS_FULL)
            cond = deterministic_choice(seed_base + f"_cond_{i}", [
                "Sun Radiant", "Moon Bright", "Mars Energetic", "Mercury Active",
                "Jupiter Wise", "Venus Calm", "Saturn Focused"
            ])
            star_count = (deterministic_index(seed_base + f"_star_{i}", 5) + 1)
            stars = "⭐" * star_count
            level_map = {1:"Poor",2:"Average",3:"Good",4:"Very Good",5:"Excellent"}
            level = level_map.get(star_count, "Good")
            activities = [
                "Decision-making, teaching, mentoring",
                "Creative work, music, or writing",
                "Meditation, mindfulness, self-reflection",
                "Leadership, presentations, planning",
                "Research, analysis, and deep work",
                "Relaxation and family time",
                "Physical exercise or travel"
            ]
            activity = deterministic_choice(seed_base + f"_act_{i}", activities)

            # set approximate morning/evening times for summary blocks
            # morning slots across 00:01-12:00, evening across 12:00-23:59
            if i < 5:
                slot_start = (datetime.combine(current, time(0,1)) + timedelta(minutes=i * (12*60//5))).time()
                slot_end = (datetime.combine(current, time(0,1)) + timedelta(minutes=(i+1) * (12*60//5)-1)).time()
            else:
                j = i - 5
                slot_start = (datetime.combine(current, time(12,0)) + timedelta(minutes=j * (12*60//5))).time()
                slot_end = (datetime.combine(current, time(12,0)) + timedelta(minutes=(j+1) * (12*60//5)-1)).time()

            rows.append({
                "Date": current.strftime("%d-%m-%Y"),
                "Day": current.strftime("%a"),
                "Morning_Timing": f"{slot_start.strftime('%I:%M %p')} - {slot_end.strftime('%I:%M %p')}" if i < 5 else "",
                "Evening_Timing": f"{slot_start.strftime('%I:%M %p')} - {slot_end.strftime('%I:%M %p')}" if i >= 5 else "",
                "Planetary_Condition": cond,
                "Stars": stars,
                "Level": level,
                "Best_Planetary_Combination": combo,
                "Recommended_Activity": activity,
                "Location": city.title()
            })
        current += timedelta(days=1)
    return pd.DataFrame(rows)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Planetary Slot Generator", layout="wide")
st.title("Deterministic Planetary Slot Generator — Single day micro slots + multi-day summary")

col1, col2, col3 = st.columns([2,2,1])
with col1:
    start_date = st.date_input("Start Date", datetime.now().date())
with col2:
    end_date = st.date_input("End Date", datetime.now().date())
with col3:
    city = st.text_input("Location (city)", "Chennai")

mode = st.radio("Mode", ["Generate (single day detailed when start=end) + multi-day summary", "Only single-day detailed (start=end required)"])

if st.button("Generate"):
    if mode.startswith("Only") and start_date != end_date:
        st.error("For 'Only single-day' mode please set Start Date == End Date.")
    else:
        if start_date == end_date:
            st.info(f"Generating micro-slot detail for {start_date.strftime('%d-%m-%Y')} at {city.title()}")
            df = generate_day_micro_slots(start_date, city)
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download single-day CSV", csv, f"planetary_{city}_{start_date}.csv", "text/csv")
        else:
            st.info(f"Generating multi-day summary from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')} for {city.title()}")
            df = generate_multi_day_summary(start_date, end_date, city)
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download multi-day CSV", csv, f"planetary_summary_{city}_{start_date}_to_{end_date}.csv", "text/csv")
