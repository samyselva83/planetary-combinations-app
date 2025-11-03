# ------------------------------------------------------
# SINGLE DATE MODE — FULL 24-HOUR PLANETARY SEQUENCE
# ------------------------------------------------------
if start_date == end_date:
    st.subheader(f"🌞 Full Planetary Movements — {start_date.strftime('%d-%m-%Y')}")

    # Reference list (you can move this to a .txt file and read from it later)
    planetary_combinations_full = [
        "MOON/MERCURY/MERCURY","MOON/MERCURY/KETHU","MOON/MERCURY/VENUS","MOON/MERCURY/SUN",
        "MOON/MERCURY/MOON","MOON/MERCURY/MARS","MOON/MERCURY/RAHU","MOON/MERCURY/JUPITER",
        "MOON/MERCURY/SATURN","SUN/KETHU/KETHU","SUN/KETHU/VENUS","SUN/KETHU/SUN",
        "SUN/KETHU/MOON","SUN/KETHU/MARS","SUN/KETHU/RAHU","SUN/KETHU/JUPITER",
        "SUN/KETHU/SATURN","SUN/KETHU/MERCURY","SUN/VENUS/VENUS","SUN/VENUS/SUN"
        # (you can continue the list — all the rest from your reference)
    ]

    total_minutes = 24 * 60 - 1  # full day minus 1 minute
    step = total_minutes // len(planetary_combinations_full)

    def fmt_time(minutes):
        h = minutes // 60
        m = minutes % 60
        am_pm = "am" if h < 12 else "pm"
        h = 12 if h == 0 else (h - 12 if h > 12 else h)
        return f"{h:02d}:{m:02d}:00 {am_pm}"

    rows = []
    start_m = 1
    for combo in planetary_combinations_full:
        end_m = min(start_m + step, total_minutes)
        level = random.choice(levels)
        stars = stars_map[level]
        condition = random.choice(planetary_conditions)
        activity = random.choice(activities)

        rows.append({
            "Date": start_date.strftime("%d-%m-%Y"),
            "Day": weekday_map[start_date.weekday()],
            "Morning_Timing": f"{fmt_time(start_m)} - {fmt_time(end_m)}",
            "Evening_Timing": "",
            "Planetary_Condition": condition,
            "Stars": stars,
            "Level": level,
            "Best_Planetary_Combination": combo,
            "Recommended_Activity": activity
        })
        start_m = end_m + 1

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
