import streamlit as st
from datetime import datetime
from itertools import permutations
import pandas as pd
from astral import LocationInfo
from astral.sun import sun

# --- Indian Cities ---
INDIAN_CITIES = {
    "Madurai": LocationInfo("Madurai", "India", "Asia/Kolkata", 9.9252, 78.1198),
    "Chennai": LocationInfo("Chennai", "India", "Asia/Kolkata", 13.0827, 80.2707),
    "Bangalore": LocationInfo("Bangalore", "India", "Asia/Kolkata", 12.9716, 77.5946),
    "Mumbai": LocationInfo("Mumbai", "India", "Asia/Kolkata", 19.0760, 72.8777),
    "Delhi": LocationInfo("Delhi", "India", "Asia/Kolkata", 28.6139, 77.2090),
    "Hyderabad": LocationInfo("Hyderabad", "India", "Asia/Kolkata", 17.3850, 78.4867),
    "Kolkata": LocationInfo("Kolkata", "India", "Asia/Kolkata", 22.5726, 88.3639),
    "Coimbatore": LocationInfo("Coimbatore", "India", "Asia/Kolkata", 11.0168, 76.9558),
    "Trichy": LocationInfo("Tiruchirappalli", "India", "Asia/Kolkata", 10.7905, 78.7047),
    "Thiruvananthapuram": LocationInfo("Thiruvananthapuram", "India", "Asia/Kolkata", 8.5241, 76.9366),
}

PLANETS = ["SUN", "MOON", "MERCURY", "VENUS", "MARS", "JUPITER", "SATURN", "RAHU", "KETHU"]

st.set_page_config(page_title="🪐 Deterministic Astro Model", layout="wide", page_icon="🌞")
st.title("🪐 Deterministic Planetary Combination Model")

# --- Sidebar ---
st.sidebar.header("Configuration")
mode = st.sidebar.radio("Select Mode:", ["Single Date", "Multiple Dates"])
city = st.sidebar.selectbox("Select City (India)", list(INDIAN_CITIES.keys()))
selected_city = INDIAN_CITIES[city]

# --- Date Input ---
if mode == "Single Date":
    date = st.sidebar.date_input("Select a Date", datetime.now())
else:
    dates_input = st.sidebar.text_area(
        "Enter multiple dates (comma separated, format: YYYY-MM-DD)",
        "2024-10-01, 2024-12-25, 2025-03-21"
    )
    date_list = [d.strip() for d in dates_input.split(",") if d.strip()]

# --- Generate All 3-planet Combinations ---
def generate_combinations():
    combos = ["/".join(p) for p in permutations(PLANETS, 3)]
    return combos

def to_table_format(combos, cols=10):
    # Split into equal columns
    n_rows = (len(combos) + cols - 1) // cols
    data = []
    for i in range(n_rows):
        row = combos[i*cols:(i+1)*cols]
        row += [""] * (cols - len(row))  # pad with blanks
        data.append(row)
    col_names = [f"Col {i+1}" for i in range(cols)]
    return pd.DataFrame(data, columns=col_names)

# --- Display for Single Date ---
if mode == "Single Date":
    st.subheader(f"📅 Planetary Combinations for {date.strftime('%d-%m-%Y')} ({city})")
    suntime = sun(selected_city.observer, date=date)
    st.write(f"**Sunrise:** {suntime['sunrise'].strftime('%H:%M')} | **Sunset:** {suntime['sunset'].strftime('%H:%M')}**")

    combos = generate_combinations()
    df = to_table_format(combos, cols=10)
    st.write(f"Total combinations generated: **{len(combos)}** (displayed in 10 columns)")
    st.dataframe(df, use_container_width=True)

# --- Display for Multiple Dates ---
else:
    st.subheader(f"📅 Common Combinations Across Multiple Dates ({city})")

    date_combos = {}
    for d in date_list:
        try:
            dt = datetime.strptime(d, "%Y-%m-%d")
            date_combos[d] = set(generate_combinations())
        except:
            st.error(f"Invalid date format: {d}")

    if len(date_combos) > 1:
        common = set.intersection(*date_combos.values())
        st.success(f"Common combinations found across {len(date_combos)} dates: {len(common)}")
        df_common = to_table_format(sorted(list(common)), cols=10)
        st.dataframe(df_common, use_container_width=True)
    else:
        st.warning("Please enter at least two valid dates to compare.")

st.markdown("---")
st.caption("🪐 Deterministic Astro Model | Built with ❤️ using Streamlit")
