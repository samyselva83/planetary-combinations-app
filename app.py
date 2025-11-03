import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# ----------------------------
# Country & City Mapping (internal)
# ----------------------------
LOCATION_DATA = {
    "India": {
        "timezone": "Asia/Kolkata",
        "cities": ["Chennai", "Madurai", "Bangalore", "Hyderabad", "Mumbai", "Delhi", "Kolkata", "Coimbatore"]
    },
    "USA": {
        "timezone": "America/New_York",
        "cities": ["New York", "Los Angeles", "Chicago", "Houston", "San Francisco"]
    },
    "UK": {
        "timezone": "Europe/London",
        "cities": ["London", "Manchester", "Birmingham", "Liverpool"]
    },
    "Germany": {
        "timezone": "Europe/Berlin",
        "cities": ["Berlin", "Munich", "Hamburg", "Frankfurt"]
    },
    "France": {
        "timezone": "Europe/Paris",
        "cities": ["Paris", "Lyon", "Marseille", "Nice"]
    },
    "Japan": {
        "timezone": "Asia/Tokyo",
        "cities": ["Tokyo", "Osaka", "Kyoto", "Yokohama"]
    },
    "Australia": {
        "timezone": "Australia/Sydney",
        "cities": ["Sydney", "Melbourne", "Brisbane", "Perth"]
    },
    "Canada": {
        "timezone": "America/Toronto",
        "cities": ["Toronto", "Vancouver", "Montreal", "Ottawa"]
    },
    "Brazil": {
        "timezone": "America/Sao_Paulo",
        "cities": ["São Paulo", "Rio de Janeiro", "Brasília"]
    },
    "South Africa": {
        "timezone": "Africa/Johannesburg",
        "cities": ["Johannesburg", "Cape Town", "Durban"]
    }
}

# ----------------------------
# Deterministic Planetary Data
# ----------------------------
PLANETARY_COMBINATIONS = [
    "MOON/MERCURY/MERCURY", "MOON/MERCURY/KETHU", "MOON/MERCURY/VENUS", "MOON/MERCURY/SUN",
    "MOON/MERCURY/MOON", "MOON/MERCURY/MARS", "MOON/MERCURY/RAHU", "MOON/MERCURY/JUPITER",
    "MOON/MERCURY/SATURN", "SUN/KETHU/KETHU", "SUN/KETHU/VENUS", "SUN/KETHU/SUN", "SUN/KETHU/MOON",
    "SUN/KETHU/MARS", "SUN/KETHU/RAHU", "SUN/KETHU/JUPITER", "SUN/KETHU/SATURN", "SUN/KETHU/MERCURY"
]

PLANETARY_DETAILS = {
    "MOON": ("Moon Bright", "⭐⭐⭐", "Good", "Decision-making, teaching, mentoring"),
    "SUN": ("Solar Radiance", "⭐⭐⭐⭐", "Excellent", "Leadership, motivation, clarity"),
    "MERCURY": ("Mercury Calm", "⭐⭐", "Fair", "Communication, negotiation, analysis"),
    "VENUS": ("Venus Harmony", "⭐⭐⭐⭐⭐", "Best", "Love, creativity, partnerships"),
    "MARS": ("Mars Active", "⭐⭐⭐", "Good", "Energy, drive, competitive spirit"),
    "JUPITER": ("Jupiter Wise", "⭐⭐⭐⭐", "Excellent", "Learning, teaching, spiritual pursuits"),
    "SATURN": ("Saturn Focused", "⭐⭐", "Moderate", "Planning, persistence, discipline"),
    "RAHU": ("Rahu Ambitious", "⭐⭐", "Mixed", "Innovation, risk-taking, growth"),
    "KETHU": ("Kethu Detached", "⭐", "Challenging", "Spiritual growth, analysis"),
}

# ----------------------------
# Deterministic Report Generator
# ----------------------------
def generate_deterministic_report(start_date, end_date, country, city):
    tz_info = LOCATION_DATA[country]["timezone"]
    timezone = pytz.timezone(tz_info)

    start = datetime.strptime(start_date, "%Y-%m-%d").astimezone(timezone)
    end = datetime.strptime(end_date, "%Y-%m-%d").astimezone(timezone)

    delta = (end - start).days + 1
    rows = []

    for i in range(delta):
        date = start + timedelta(days=i)
        date_str = date.strftime("%d-%m-%Y")
        day_str = date.strftime("%a")

        # Deterministic combination using date+city
        seed = (hash(date_str + city + country) % len(PLANETARY_COMBINATIONS))
        combination = PLANETARY_COMBINATIONS[seed]
        main_planet = combination.split("/")[0]
        condition, stars, level, activity = PLANETARY_DETAILS.get(main_planet, ("Unknown", "⭐", "Normal", "General activity"))

        # Timing
        morning_start = datetime(date.year, date.month, date.day, 6, 0, 0).strftime("%I:%M:%S %p")
        morning_end = datetime(date.year, date.month, date.day, 7, 0, 0).strftime("%I:%M:%S %p")
        evening_start = datetime(date.year, date.month, date.day, 18, 0, 0).strftime("%I:%M:%S %p")
        evening_end = datetime(date.year, date.month, date.day, 19, 0, 0).strftime("%I:%M:%S %p")

        rows.append({
            "Date": date_str,
            "Day": day_str,
            "Country": country,
            "City": city,
            "Morning_Timing": f"{morning_start} - {morning_end}",
            "Evening_Timing": f"{evening_start} - {evening_end}",
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combination,
            "Recommended_Activity": activity,
        })

    return pd.DataFrame(rows)

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Astro Day Report", layout="wide", page_icon="🌕")
st.title("🌕 Deterministic Planetary Combination Report")

col1, col2, col3, col4 = st.columns(4)
with col1:
    start_date = st.date_input("Start Date", datetime.today())
with col2:
    end_date = st.date_input("End Date", datetime.today() + timedelta(days=2))
with col3:
    country = st.selectbox("Select Country", list(LOCATION_DATA.keys()))
with col4:
    city = st.selectbox("Select City", LOCATION_DATA[country]["cities"])

if st.button("Generate Report"):
    df = generate_deterministic_report(str(start_date), str(end_date), country, city)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download as CSV", csv, f"{city}_Astro_Report.csv", "text/csv")

st.markdown("---")
st.caption("✨ Deterministic planetary combination report – consistent results based on date, country, and city.")
