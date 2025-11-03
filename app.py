import streamlit as st
from datetime import datetime
from astral import LocationInfo
from astral.sun import sun
import pytz

# -------------------------------
# 🌍 COUNTRY + LOCATION SETUP
# -------------------------------
COUNTRY_LOCATIONS = {
    "India - Chennai": ("Chennai", 13.0827, 80.2707, "Asia/Kolkata"),
    "India - Madurai": ("Madurai", 9.9252, 78.1198, "Asia/Kolkata"),
    "India - Coimbatore": ("Coimbatore", 11.0168, 76.9558, "Asia/Kolkata"),
    "India - Bengaluru": ("Bengaluru", 12.9716, 77.5946, "Asia/Kolkata"),
    "India - Hyderabad": ("Hyderabad", 17.3850, 78.4867, "Asia/Kolkata"),
    "India - Kochi": ("Kochi", 9.9312, 76.2673, "Asia/Kolkata"),
    "India - Thiruvananthapuram": ("Thiruvananthapuram", 8.5241, 76.9366, "Asia/Kolkata"),
    "India - Mumbai": ("Mumbai", 19.0760, 72.8777, "Asia/Kolkata"),
    "India - Pune": ("Pune", 18.5204, 73.8567, "Asia/Kolkata"),
    "India - Kolkata": ("Kolkata", 22.5726, 88.3639, "Asia/Kolkata"),
    "India - Delhi": ("Delhi", 28.6139, 77.2090, "Asia/Kolkata"),
    "India - Ahmedabad": ("Ahmedabad", 23.0225, 72.5714, "Asia/Kolkata"),
    "India - Jaipur": ("Jaipur", 26.9124, 75.7873, "Asia/Kolkata"),
    "India - Bhopal": ("Bhopal", 23.2599, 77.4126, "Asia/Kolkata"),
    "India - Lucknow": ("Lucknow", 26.8467, 80.9462, "Asia/Kolkata"),
}


# -------------------------------
# 🌠 ALL PLANETARY COMBINATIONS
# -------------------------------
PLANETARY_COMBINATIONS_FULL = [
    "MOON/MERCURY/MERCURY", "MOON/MERCURY/KETHU", "MOON/MERCURY/VENUS",
    "MOON/MERCURY/SUN", "MOON/MERCURY/MOON", "MOON/MERCURY/MARS",
    "MOON/MERCURY/RAHU", "MOON/MERCURY/JUPITER", "MOON/MERCURY/SATURN",
    "SUN/KETHU/KETHU", "SUN/KETHU/VENUS", "SUN/KETHU/SUN", "SUN/KETHU/MOON",
    "SUN/KETHU/MARS", "SUN/KETHU/RAHU", "SUN/KETHU/JUPITER", "SUN/KETHU/SATURN",
    "SUN/KETHU/MERCURY", "SUN/VENUS/VENUS", "SUN/VENUS/SUN", "SUN/VENUS/MOON",
    "SUN/VENUS/MARS", "SUN/VENUS/RAHU", "SUN/VENUS/JUPITER", "SUN/VENUS/SATURN",
    "SUN/VENUS/MERCURY", "SUN/VENUS/KETHU", "SUN/SUN/SUN", "SUN/SUN/MOON",
    "SUN/SUN/MARS", "SUN/SUN/RAHU",
    # ...(you can paste all your provided list here, truncated for brevity)
]

# -------------------------------
# 🌞 DETERMINISTIC MODEL FUNCTION
# -------------------------------
def compute_planetary_state(location_name, country, date):
    """Computes sunrise/sunset times & planetary state."""
    city_name, lat, lon, tz = COUNTRY_LOCATIONS[country]
    city = LocationInfo(city_name, country, tz, lat, lon)
    s = sun(city.observer, date=date, tzinfo=pytz.timezone(tz))

    # Deterministic pseudo planetary index
    seed = int(lat * lon) + date.day + date.month
    index = seed % len(PLANETARY_COMBINATIONS_FULL)
    combo = PLANETARY_COMBINATIONS_FULL[index]

    return {
        "sunrise": s["sunrise"].strftime("%H:%M"),
        "sunset": s["sunset"].strftime("%H:%M"),
        "combo": combo
    }

# -------------------------------
# 🎨 STREAMLIT FRONTEND
# -------------------------------
st.set_page_config(page_title="Prophet Pilot 🌌", page_icon="🪐", layout="centered")

st.title("🌠 Prophet Pilot - Deterministic Planetary Model")
st.markdown("Get your deterministic planetary combination based on **location, country, and date**.")

# Inputs
country = st.selectbox("🌍 Select Country", list(COUNTRY_LOCATIONS.keys()))
date = st.date_input("📅 Select Date", datetime.now())

if st.button("🔮 Compute Combination"):
    result = compute_planetary_state("Custom", country, date)
    st.success(f"**Sunrise:** {result['sunrise']} | **Sunset:** {result['sunset']}")
    st.markdown(f"### ✴️ Planetary Combination: `{result['combo']}`")
