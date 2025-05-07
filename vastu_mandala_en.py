import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Planet colors in Vedic astrology
color_map = {
    1: '#E52B50', 2: '#87CEEB', 3: '#F4C430', 4: '#86261c',
    5: '#009B77', 6: '#FADADD', 7: '#b2beb5', 8: '#0047AB', 9: '#ff4040'
}

# Vastu mandala zone layout
zone_coords = {
    1: [(4,4), (5,4), (6,4), (4,5), (5,5), (6,5), (4,6), (5,6), (6,6),
        (2,1), (2,2), (1,2), (8,1), (8,2), (9,2), (1,8), (2,8), (2,9), (8,8), (8,9), (9,8)],
    2: [(5,1), (4,2), (5,2), (6,2), (4,3), (5,3), (6,3),
        (2,4), (3,4), (1,5), (2,5), (3,5), (2,6), (3,6),
        (4,7), (5,7), (6,7), (4,8), (5,8), (6,8), (5,9),
        (7,4), (7,5), (7,6), (8,4), (8,5), (8,6), (9,5)],
    3: [(6,1), (3,3), (7,3), (1,4), (9,6), (3,7), (7,7), (4,9)],
    4: [(1,1), (3,1), (9,1), (9,3), (1,7), (1,9), (7,9), (9,9)]
}

# Planet information
planet_info = {
    1: ("Sun", "ruby", "leadership, authority, clarity"),
    2: ("Moon", "light blue", "emotion, softness, intuition"),
    3: ("Jupiter", "saffron", "wisdom, guidance, growth"),
    4: ("Rahu", "tea brown", "illusions, instability, surprises"),
    5: ("Mercury", "emerald", "intellect, communication, flexibility"),
    6: ("Venus", "pink", "harmony, love, beauty"),
    7: ("Ketu", "smoky", "isolation, detachment, mysticism"),
    8: ("Saturn", "blue", "karma, discipline, responsibility"),
    9: ("Mars", "scarlet", "energy, action, intensity")
}

# Reduce number to a single digit
def reduce_to_digit(value):
    total = sum(int(d) for d in str(value) if d.isdigit())
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total

# Draw the grid with colors
def draw_grid(colors):
    zone_map = np.zeros((9, 9), dtype=int)
    for zone, coords in zone_coords.items():
        for x, y in coords:
            zone_map[y - 1, x - 1] = zone
    fig, ax = plt.subplots(figsize=(6, 6))
    for y in range(9):
        for x in range(9):
            zone = zone_map[y, x]
            color = color_map[colors[zone]] if zone in colors else 'white'
            rect = plt.Rectangle([x, 8 - y], 1, 1, facecolor=color, edgecolor='black')
            ax.add_patch(rect)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_xticks(np.arange(9) + 0.5)
    ax.set_yticks(np.arange(9) + 0.5)
    ax.set_xticklabels(range(1, 10))
    ax.set_yticklabels(range(1, 10))
    ax.set_aspect('equal')
    plt.grid(True)
    st.pyplot(fig)

# UI
st.title("Personalized Vastu Mandala")

st.markdown("""
Enter the coordinates of your home, plot, apartment, or workspace.  
You can find coordinates using [this online tool](https://snipp.ru/tools/address-coord).  
Copy and paste the latitude and longitude below.

Each zone of the mandala corresponds to a planetary influence and is assigned a color:

- The degree and minute values are reduced to single-digit numbers (1–9),
- Each number corresponds to a Vedic planet,
- You will see the colors and meanings for your specific location.
""")

lat_input = st.text_input("Latitude (e.g., 65.026802)", "65.026802")
lon_input = st.text_input("Longitude (e.g., 35.709128)", "35.709128")

if st.button("Generate Mandala"):
    try:
        lat = float(lat_input)
        lon = float(lon_input)

        lat_deg = int(lat)
        lat_min = int(round((lat - lat_deg) * 60))
        lon_deg = int(lon)
        lon_min = int(round((lon - lon_deg) * 60))

        z1 = reduce_to_digit(lat_deg)
        z2 = reduce_to_digit(lon_deg)
        z3 = reduce_to_digit(lat_min)
        z4 = reduce_to_digit(lon_min)

        st.markdown(f"### Zone Interpretation")
        st.markdown(f"**Zone 1 (Latitude Degrees): {z1}** — {planet_info[z1][0]} | {planet_info[z1][1]}, {planet_info[z1][2]}")
        st.markdown(f"**Zone 2 (Longitude Degrees): {z2}** — {planet_info[z2][0]} | {planet_info[z2][1]}, {planet_info[z2][2]}")
        st.markdown(f"**Zone 3 (Latitude Minutes): {z3}** — {planet_info[z3][0]} | {planet_info[z3][1]}, {planet_info[z3][2]}")
        st.markdown(f"**Zone 4 (Longitude Minutes): {z4}** — {planet_info[z4][0]} | {planet_info[z4][1]}, {planet_info[z4][2]}")

        draw_grid({1: z1, 2: z2, 3: z3, 4: z4})

        if any(z in [4, 7, 8, 9] for z in [z1, z2, z3, z4]):
            st.warning("Your mandala includes challenging planetary zones (Rahu, Ketu, Saturn, or Mars).")
            st.markdown("**Recommended remedies:** use sunlight, candles, mantras, sacred symbols, natural materials (wood, cotton, stone), and avoid overuse of dark or intense colors in interiors.")

        st.markdown("""
---

### How the Calculation Works

- We split the latitude and longitude into degrees and minutes,
- Each value is summed into a single-digit number (1–9),
- These numbers correspond to the 9 Vedic planets,
- We use a traditional South Indian swastika-based Vastu mandala (9×9 zones).

---

### How to Use Your Mandala
- Generate your mandala and review the planetary zones,
- Save or print the image,
- Place it on a wall in your home or workspace (with **north at the top**),
- Decorate or energize zones using the suggested planetary colors, mantras, incense, or symbols.
""")

    except ValueError:
        st.error("Please enter valid numeric coordinates.")

st.markdown("""
---

🔍 For a full personalized interpretation and vastu consultation, you can [book a session here](https://goroskop1008.ru/uslugi/#consult#!/tproduct/842449103-1607970659374)

🛠️ Application developed by **S. A. Kreutzer**  
All rights reserved.
""")
