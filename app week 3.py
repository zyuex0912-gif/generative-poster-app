# app.py — Generative Poster Web App for Streamlit Cloud
# Features: style presets, palettes, reproducibility, export as PNG (300 DPI)

import streamlit as st
import random, math, io
import numpy as np
from matplotlib.colors import hsv_to_rgb
import matplotlib.pyplot as plt

# --- Blob and Palette Functions ---
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    """Generate a wobbly closed shape around a center with base radius r."""
    angles = np.linspace(0, 2*math.pi, points, endpoint=False)
    radii  = r * (1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def make_palette(k=6, mode="random", base_h=0.60):
    """Return k colors (RGB) by sampling HSV depending on mode."""
    cols = []
    for _ in range(k):
        if mode == "pastel":
            h = random.random(); s = random.uniform(0.15, 0.35); v = random.uniform(0.90, 1.00)
        elif mode == "vivid":
            h = random.random(); s = random.uniform(0.80, 1.00); v = random.uniform(0.80, 1.00)
        elif mode == "mono":
            h = base_h;         s = random.uniform(0.20, 0.60); v = random.uniform(0.50, 1.00)
        else:
            h = random.random(); s = random.uniform(0.30, 1.00); v = random.uniform(0.50, 1.00)
        cols.append(tuple(hsv_to_rgb([h, s, v])))
    return cols

STYLE_PRESETS = {
    "Minimal":    dict(n_layers=5,  wobble_range=(0.02,0.08), alpha_range=(0.30,0.50), palette_mode="pastel"),
    "Vivid":      dict(n_layers=12, wobble_range=(0.05,0.20), alpha_range=(0.35,0.70), palette_mode="vivid"),
    "NoiseTouch": dict(n_layers=14, wobble_range=(0.12,0.30), alpha_range=(0.25,0.55), palette_mode="mono"),
}

def generate_poster(style=None, seed=None,
                    n_layers=8,
                    radius_range=(0.15, 0.45),
                    wobble_range=(0.05, 0.25),
                    alpha_range=(0.25, 0.6),
                    figsize=(7,10),
                    background=(0.98,0.98,0.97),
                    palette_mode="pastel"):
    """Create a generative poster with optional style and seed."""
    if style in STYLE_PRESETS:
        preset = STYLE_PRESETS[style]
        n_layers     = preset.get("n_layers", n_layers)
        wobble_range = preset.get("wobble_range", wobble_range)
        alpha_range  = preset.get("alpha_range", alpha_range)
        palette_mode = preset.get("palette_mode", palette_mode)

    if seed is not None:
        random.seed(seed); np.random.seed(seed)

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")
    ax.set_facecolor(background)
    palette = make_palette(6, mode=palette_mode)

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr  = random.uniform(*radius_range)
        wob = random.uniform(*wobble_range)
        x, y = blob(center=(cx, cy), r=rr, wobble=wob)
        color = random.choice(palette)
        alpha = random.uniform(*alpha_range)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    # Label
    ax.text(0.05, 0.95, f"Generative Poster • {style or 'Custom'}",
            fontsize=16, weight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.91, "Week 3 • Arts & Advanced Big Data",
            fontsize=11, transform=ax.transAxes)
    ax.set_xlim(0,1); ax.set_ylim(0,1)
    return fig

# --- Streamlit UI ---
st.title("🎨 Generative Abstract Poster")
st.caption("Week 3 • Arts & Advanced Big Data")

col1, col2, col3 = st.columns(3)
with col1:
    style = st.selectbox("🎨 Style Preset", ["Minimal", "Vivid", "NoiseTouch", "Custom"])
with col2:
    seed = st.number_input("🔢 Random Seed", min_value=0, max_value=9999, value=42)
with col3:
    n_layers = st.slider("🧩 Layers (if Custom)", 3, 20, 8)

generate = st.button("✨ Generate Poster")

if generate:
    fig = generate_poster(style=style if style != "Custom" else None,
                          seed=seed,
                          n_layers=n_layers)

    st.pyplot(fig)

    # Save to buffer for download
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0.1)
    buf.seek(0)

    st.download_button(
        label="💾 Download Poster (300 DPI PNG)",
        data=buf,
        file_name=f"poster_{style}_{seed}.png",
        mime="image/png"
    )

    plt.close(fig)
