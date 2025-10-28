import streamlit as st
import random, math, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import pandas as pd

# ----------------------------------------------------------
# 1. 波浪形状生成器（基础水波纹形状）
# ----------------------------------------------------------
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points, endpoint=False)
    angle_factor = 0.6 + 0.4 * np.cos(angles)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5) * angle_factor)
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# ----------------------------------------------------------
# 2. 调色板管理（海洋主题）
# ----------------------------------------------------------
PALETTE_FILE = "palette.csv"

if not os.path.exists(PALETTE_FILE):
    df_init = pd.DataFrame([
        {"name": "deep_sea", "r": 0.05, "g": 0.1, "b": 0.3},
        {"name": "mid_sea", "r": 0.1, "g": 0.2, "b": 0.5},
        {"name": "shallow_sea", "r": 0.2, "g": 0.4, "b": 0.7},
        {"name": "wave_white", "r": 0.9, "g": 0.95, "b": 1.0},
        {"name": "sea_green", "r": 0.1, "g": 0.3, "b": 0.5},
        {"name": "sun_blue", "r": 0.3, "g": 0.6, "b": 0.9}
    ])
    df_init.to_csv(PALETTE_FILE, index=False)

def read_palette():
    return pd.read_csv(PALETTE_FILE)

def load_csv_palette():
    df = read_palette()
    return [(row.r, row.g, row.b) for row in df.itertuples()]

# ----------------------------------------------------------
# 3. 调色板生成器（偏蓝绿）
# ----------------------------------------------------------
def make_palette(k=6, mode="pastel", base_h=0.60):
    cols = []
    if mode == "csv":
        return load_csv_palette()
    for _ in range(k):
        if mode == "pastel":
            h = random.uniform(0.5, 0.7)
            s = random.uniform(0.15, 0.35)
            v = random.uniform(0.8, 1.0)
        elif mode == "vivid":
            h = random.uniform(0.5, 0.7)
            s = random.uniform(0.8, 1.0)
            v = random.uniform(0.8, 1.0)
        elif mode == "mono":
            h = base_h
            s = random.uniform(0.2, 0.6)
            v = random.uniform(0.5, 1.0)
        else:
            h = random.uniform(0.5, 0.7)
            s = random.uniform(0.3, 1.0)
            v = random.uniform(0.5, 1.0)
        cols.append(tuple(hsv_to_rgb([h, s, v])))
    return cols

# ----------------------------------------------------------
# 4. 海报绘制函数
# ----------------------------------------------------------
def draw_poster(n_layers=8, wobble=0.15, palette_mode="pastel", seed=0):
    random.seed(seed)
    np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis('off')
    ax.set_facecolor((0.97, 0.97, 0.97))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    palette = make_palette(6, mode=palette_mode)

    for layer in range(n_layers):
        layer_ratio = layer / (n_layers - 1)
        cx = 0.5 + (random.random() - 0.5) * 0.4 * (1 - layer_ratio)
        cy = 0.2 + layer_ratio * 0.6
        rr = 0.4 - layer_ratio * 0.25
        x, y = blob((cx, cy), r=rr, wobble=wobble * (0.5 + layer_ratio))

        if palette_mode == "csv" and len(palette) >= 4:
            if layer_ratio < 0.3:
                color = palette[0]
            elif layer_ratio < 0.6:
                color = palette[1]
            else:
                color = palette[2]
        else:
            color = random.choice(palette)

        alpha = 0.5 + layer_ratio * 0.3
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

        if layer_ratio > 0.7 and random.random() > 0.5:
            peak_mask = y > cy + rr * 0.6
            if np.sum(peak_mask) > 20:
                foam_x = x[peak_mask] + (np.random.rand(np.sum(peak_mask)) - 0.5) * 0.03
                foam_y = y[peak_mask] + (np.random.rand(np.sum(peak_mask)) - 0.5) * 0.02
                ax.fill(
                    foam_x, foam_y,
                    color=palette[3] if len(palette) >= 4 else (1, 1, 1, 0.7),
                    alpha=0.5, edgecolor='none'
                )

    ax.text(0.05, 0.95, f"Interactive Poster • {palette_mode}",
            transform=ax.transAxes, fontsize=12, weight="bold")

    return fig

# ----------------------------------------------------------
# 5. Streamlit 界面
# ----------------------------------------------------------
st.set_page_config(page_title="Ocean Wave Poster", layout="centered")
st.title("🌊 Generative Ocean Wave Poster")
st.write("An interactive generative art experiment inspired by ocean waves.")

# Sidebar controls
with st.sidebar:
    st.header("🎛 Controls")
    n_layers = st.slider("Number of Layers", 3, 20, 8)
    wobble = st.slider("Wave Wobble", 0.01, 9.0, 0.15, 0.01)
    palette_mode = st.selectbox("Palette Mode", ["pastel", "vivid", "mono", "random", "csv"])
    seed = st.number_input("Random Seed", 0, 9999, 0)
    generate_btn = st.button("Generate Poster")

# Draw and display poster
if generate_btn:
    fig = draw_poster(n_layers=n_layers, wobble=wobble,
                      palette_mode=palette_mode, seed=seed)
    st.pyplot(fig)

    # Download button
    fig.savefig("poster1.png", dpi=300, bbox_inches="tight")
    with open("poster1.png", "rb") as f:
        st.download_button("💾 Download Poster", f, file_name="poster1.png", mime="image/png")
else:
    st.info("Adjust the sliders in the sidebar and click **Generate Poster** to begin.")
