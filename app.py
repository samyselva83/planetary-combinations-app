# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 12:17:02 2025

@author: samys
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Planetary Combinations Calendar", layout="wide", page_icon="🪐")

# --------------------------
# Title & Description
# --------------------------
st.title("🪐 Planetary Combination Insights")
st.markdown("""
This app provides the **best planetary combinations** for new or daily activities.  
You can select a custom date range (or use today's date) to view the top 10 combinations with their benefits and energies.
""")

# --------------------------
# Date Selection
# --------------------------
today = datetime.today()
col1, col2 = st.columns(2)
start_date = col1.date_input("Select Start Date", today)
end_date = col2.date_input("Select End Date", today + timedelta(days=1))

# --------------------------
# Planetary Combination Data
# --------------------------
data = [
    {
        "Combination": "Mercury / Moon / Jupiter",
        "Core Energy": "Wisdom + Emotion + Clarity",
        "Key Benefit": "Enhances planning, communication, and decision-making",
        "Best Idea For": "Learning, presentations, and meetings"
    },
    {
        "Combination": "Sun / Mercury / Mars",
        "Core Energy": "Leadership + Logic + Action",
        "Key Benefit": "Inspires confidence and quick execution",
        "Best Idea For": "Starting projects, leadership, public initiatives"
    },
    {
        "Combination": "Venus / Mercury / Moon",
        "Core Energy": "Creativity + Communication + Calm",
        "Key Benefit": "Supports artistic and relationship growth",
        "Best Idea For": "Design, art, social and teamwork activities"
    },
    {
        "Combination": "Mars / Jupiter / Mercury",
        "Core Energy": "Courage + Wisdom + Logic",
        "Key Benefit": "Great for technical and strategic planning",
        "Best Idea For": "Coding, analysis, innovation"
    },
    {
        "Combination": "Moon / Venus / Jupiter",
        "Core Energy": "Peace + Love + Fortune",
        "Key Benefit": "Boosts harmony and emotional intelligence",
        "Best Idea For": "Family time, travel, spiritual balance"
    },
    {
        "Combination": "Saturn / Mercury / Jupiter",
        "Core Energy": "Discipline + Intellect + Knowledge",
        "Key Benefit": "Excellent for long-term planning and stability",
        "Best Idea For": "Research, organization, study"
    },
    {
        "Combination": "Sun / Jupiter / Mercury",
        "Core Energy": "Authority + Wisdom + Communication",
        "Key Benefit": "Empowers teaching and leadership decisions",
        "Best Idea For": "Mentoring, education, guidance"
    },
    {
        "Combination": "Mars / Mercury / Venus",
        "Core Energy": "Drive + Logic + Harmony",
        "Key Benefit": "Balances creativity and productivity",
        "Best Idea For": "Business strategy, negotiations"
    },
    {
        "Combination": "Moon / Mercury / Venus",
        "Core Energy": "Intuition + Logic + Grace",
        "Key Benefit": "Ideal for self-expression and writing",
        "Best Idea For": "Counseling, writing, content creation"
    },
    {
        "Combination": "Jupiter / Venus / Mercury",
        "Core Energy": "Expansion + Beauty + Intelligence",
        "Key Benefit": "Enhances wealth, creativity, and communication",
        "Best Idea For": "Marketing, branding, partnerships"
    }
]

df = pd.DataFrame(data)

# --------------------------
# Display Section
# --------------------------
st.subheader(f"✨ Planetary Combinations ({start_date} → {end_date})")
st.dataframe(df, use_container_width=True, hide_index=True)

# --------------------------
# Footer
# --------------------------
st.markdown("---")
st.caption("Developed with 💫 Streamlit | Ideal for daily guidance & astrological insight")
