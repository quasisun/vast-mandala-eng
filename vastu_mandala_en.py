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

# Planetary info
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

# Reduce to single digit, default to 9 if 0
def reduce_to_digit(value):
    total = sum(int(d) for d in str(value) if d.isdigit())
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total if total > 0 else 9

# Draw 9x9 grid
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

# Interface
st.title("Personalized Vastu Purusha Mandala")

st.markdown("""
Enter the coordinates of your home, land, or workplace.   
Paste your **latitude** and **longitude** below.

This tool will calculate:
- 4 numbers from your coordinates (degrees and minutes),
- Reduce each to a digit (1–9),
- Show the corresponding planetary energies.

Each sector of the mandala is then colored accordingly.
""")

lat_input = st.text_input("Latitude", "0.0000")
lon_input = st.text_input("Longitude", "0.0000")

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

        st.markdown("### Zone Interpretations")
        for zn, label in zip([z1, z2, z3, z4], [
            "Zone 1 (Latitude Degrees)",
            "Zone 2 (Longitude Degrees)",
            "Zone 3 (Latitude Minutes)",
            "Zone 4 (Longitude Minutes)"
        ]):
            if zn in planet_info:
                name, color, trait = planet_info[zn]
                st.markdown(f"**{label}: {zn}** — {name} | {color}, {trait}")
            else:
                st.markdown(f"**{label}: {zn}** — No planetary interpretation available.")

        draw_grid({1: z1, 2: z2, 3: z3, 4: z4})

        if any(z in [4, 7, 8, 9] for z in [z1, z2, z3, z4]):
            st.warning("One or more zones are ruled by Rahu, Ketu, Saturn, or Mars — potential instability or challenges.")
            st.markdown("**Suggested remedies:** more light, fire, mantras, natural fabrics and textures, avoid overly dark or synthetic colors in decor.")

        st.markdown("""
---

### How it works

- Latitude and longitude are split into degrees and minutes,
- Each part is reduced to a single digit from 1–9,
- These digits correspond to planetary influences,
- The 9×9 grid is colored according to those energies.

---

### How to use your mandala

- Print or screenshot the grid,
- Hang it with north at the top,
- Use the planetary colors and meanings to harmonize interior zones with paint, light, fabric, symbols or mantras.
""")

    except ValueError:
        st.error("Please enter valid numeric coordinates.")

st.markdown("""
---

App by **S. A. Kreuzer**  
""")
