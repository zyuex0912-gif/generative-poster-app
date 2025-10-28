# app.py — Generative Poster (Streamlit Version)
# Supports palette modes, seed control, and PNG export

import streamlit as st
import random, math, io, os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import hsv_to_rgb

# --- Utility: Blob Shape ---
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points, endpoint=False)
    radii  = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# --- Palette Setup ---
PALETTE_FILE = "palette.csv"

DEFAULT_PALETTE = """name,r,g,b
amethyst,0.6,0.4,0.8
byzantine,0.74,0.2,0.64
eggplant,0.38,0.25,0.32
electric_purple,0.75,0.0,1.0
grape,0.44,0.18,0.66
lavender,0.9,0.9,0.98
lilac,0.78,0.63,0.78
magenta,1.0,0.0,1.0
majesty,0.42,0.05,0.68
mauve,0.88,0.69,1.0
mulberry,0.77,0.26,0.55
orchid,0.85,0.44,0.84
pansy,0.39,0.24,0.59
thistle,0.72,0.65,0.72
violet,0.54,0.17,0.89
wisteria,0.75,0.61,0.98
aztec_purple,0.54,0.23,1.0
baltimore_ravens_purple,0.16,0.01,0.33
bright_lilac,0.85,0.57,0.94
fuchsia_purple,0.71,0.33,0.63
"""

# Create palette.csv on first run
if not os.path.exists(PALETTE_FILE):
    with open(PALETTE_FILE, "w") as f:
        f.write(DEFAULT_PALETTE)

def load_csv_palette():
    df = pd.read_csv(PALETTE_FILE)
    return [(row.r, row.g, row.b) for row in df.itertuples()]

def make_palette(k=6, mode="pastel", base_h=0.60):
    if mode == "csv":
        return load_csv_palette()

    cols = []
    for _ in range(k):
        if mode == "pastel":
            h = random.random(); s = random.uniform(0.15, 0.35); v = random.uniform(0.9, 1.0)
        elif mode == "vivid":
            h = random.random(); s = random.uniform(0.8, 1.0);  v = random.uniform(0.8, 1.0)
        elif mode == "mono":
            h = base_h; s = random.uniform(0.2, 0.6); v = random.uniform(0.5, 1.0)
        else:
            h = random.random(); s = random.uniform(0.3, 1.0); v = random.uniform(0.5, 1.0)
        cols.append(tuple(hsv_to_rgb([h, s, v])))
    return cols

# --- Drawing Function ---
def draw_poster(n_layers=8, wobble=0.15, palette_mode="pastel", seed=0):
    random.seed(seed); np.random.seed(seed)
    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")
    ax.set_facecolor((0.97, 0.97, 0.97))

    palette = make_palette(6, mode=palette_mode)
    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x, y = blob((cx, cy), r=rr, wobble=wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.3, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    ax.text(0.05, 0.95, f"Generative Poster • {palette_mode}",
            transform=ax.transAxes, fontsize=13, weight="bold")
    ax.text(0.05, 0.91, "Week 5 • Arts & Advanced Big Data",
            transform=ax.transAxes, fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig

# --- Streamlit Interface ---
st.title("🎨 Interactive Generative Poster")

# Sidebar controls
st.sidebar.header("🎛 Settings")
n_layers = st.sidebar.slider("Number of Layers", 3, 20, 8)
wobble = st.sidebar.slider("Wobble", 0.01, 1.0, 0.15, 0.01)
palette_mode = st.sidebar.selectbox("Palette Mode", ["pastel", "vivid", "mono", "random", "csv"])
seed = st.sidebar.number_input("Seed", min_value=0, max_value=9999, value=0, step=1)

# Generate Poster
fig = draw_poster(n_layers, wobble, palette_mode, seed)
st.pyplot(fig)

# Save as PNG
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0.1)
buf.seek(0)

st.download_button(
    label="💾 Download Poster (300 DPI PNG)",
    data=buf,
    file_name=f"poster_{palette_mode}_seed{seed}.png",
    mime="image/png"
)

st.markdown("---")
st.markdown("Developed for **Arts & Advanced Big Data • Week 5** — Demonstrating color harmony, reproducibility, and visual softness.")
