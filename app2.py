# app.py — Generative Abstract Poster (Week 9)
# Features: palettes, presets, seed, soft visuals, PNG export

import streamlit as st
import random, math, io
import numpy as np
import matplotlib.pyplot as plt

# --- Define Color Palettes ---
PALETTES = {
    "Pastel": [(0.96, 0.75, 0.76), (0.74, 0.89, 0.82), (0.86, 0.80, 0.95), (0.97, 0.93, 0.76), (0.75, 0.86, 0.96)],
    "Vivid": [(0.9, 0.3, 0.3), (0.3, 0.6, 0.9), (0.3, 0.9, 0.5), (0.95, 0.8, 0.25), (0.7, 0.4, 0.9)],
    "NoiseTouch": [(0.85, 0.8, 0.75), (0.76, 0.82, 0.85), (0.8, 0.83, 0.8), (0.9, 0.88, 0.8), (0.7, 0.75, 0.7)],
}

# --- Helper Functions ---
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    """Generate a wobbly closed blob shape."""
    angles = np.linspace(0, 2*math.pi, points)
    radii = r * (1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# --- Streamlit UI ---
st.title("🎨 Generative Abstract Poster")
st.caption("Week 9 • Arts & Advanced Big Data")

col1, col2, col3 = st.columns(3)
with col1:
    style = st.selectbox("Style Preset", ["Minimal", "Vivid", "NoiseTouch"])
with col2:
    n_layers = st.slider("Number of Layers", 3, 15, 8)
with col3:
    seed = st.number_input("Random Seed", min_value=0, max_value=9999, value=0)

# Wobble range & palette setup
if style == "Minimal":
    palette = PALETTES["Pastel"]
    wobble_min, wobble_max = 0.02, 0.12
elif style == "Vivid":
    palette = PALETTES["Vivid"]
    wobble_min, wobble_max = 0.1, 0.3
else:
    palette = PALETTES["NoiseTouch"]
    wobble_min, wobble_max = 0.05, 0.25

generate = st.button("🎨 Generate Poster")

if generate:
    # Reproducible randomness
    random.seed(seed)
    np.random.seed(seed)

    # Create figure
    fig, ax = plt.subplots(figsize=(7,10))
    ax.axis("off")
    ax.set_facecolor((0.98, 0.98, 0.97))  # off-white background

    # Draw layered blobs
    for i in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x, y = blob(center=(cx, cy), r=rr, wobble=random.uniform(wobble_min, wobble_max))
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    # Typographic label
    plt.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold', transform=ax.transAxes)
    plt.text(0.05, 0.91, "Week 9 • Arts & Advanced Big Data", fontsize=11, transform=ax.transAxes)

    st.pyplot(fig)

    # --- Export to PNG ---
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0.1)
    buf.seek(0)

    st.download_button(
        label="💾 Download Poster as PNG (300 DPI)",
        data=buf,
        file_name=f"generative_poster_seed{seed}.png",
        mime="image/png"
    )

    plt.close(fig)
