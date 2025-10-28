# app.py — Week 4: 3D-like Generative Poster
# Concepts: shadow, transparency, layering, depth cues (warm/cool colors)
# Deployment: Streamlit Cloud interactive app

import streamlit as st
import random, math, io
import numpy as np
import matplotlib.pyplot as plt

# --- Core Function ---
def blob(center=(0.5,0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2*math.pi, points, endpoint=False)
    radii  = r * (1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def generate_3d_poster(n_layers=6, seed=0):
    """Generate a 3D-like generative poster figure."""
    random.seed(seed); np.random.seed(seed)
    fig, ax = plt.subplots(figsize=(7,7))
    ax.axis('off')
    ax.set_facecolor((0.98, 0.97, 0.95))  # soft warm off-white background

    for depth in range(n_layers):
        # Position and base radius
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x, y = blob((cx,cy), r=rr, wobble=0.12)

        # Soft shadow layer
        shadow_alpha = max(0.12 - depth * 0.02, 0)
        shadow_scale = 1.05 + depth * 0.02
        ax.fill(
            cx + (x - cx) * shadow_scale + 0.015,
            cy + (y - cy) * shadow_scale - 0.015,
            color=(0.2, 0.2, 0.2),
            alpha=shadow_alpha
        )

        # Warm-to-cool depth color shift
        if depth < n_layers / 2:
            r = 0.8 + random.uniform(-0.2, 0.1)
            g = 0.4 + random.uniform(-0.1, 0.1)
            b = 0.2 + random.uniform(0, 0.1)
        else:
            r = 0.2 + random.uniform(0, 0.1)
            g = 0.4 + random.uniform(-0.1, 0.1)
            b = 0.8 + random.uniform(-0.2, 0.1)
        color = (min(r,1.0), min(g,1.0), min(b,1.0))

        # Transparency by depth (near solid, far soft)
        alpha = min(0.5 + depth * 0.08, 1.0)
        ax.fill(x, y, color=color, alpha=alpha)

    # Label overlay
    ax.text(0.05, 0.95, "3D-like Generative Poster",
            fontsize=16, weight="bold", transform=ax.transAxes)
    ax.text(0.05, 0.91, "Week 4 • Arts & Advanced Big Data",
            fontsize=11, transform=ax.transAxes)

    ax.set_xlim(0,1); ax.set_ylim(0,1)
    return fig

# --- Streamlit UI ---
st.title("🌀 3D-like Generative Poster")
st.caption("Week 4 • Arts & Advanced Big Data")

# Sidebar controls
st.sidebar.header("🎛 Poster Parameters")
n_layers = st.sidebar.slider("Number of Layers", 3, 15, 6)
seed = st.sidebar.number_input("Random Seed", min_value=0, max_value=9999, value=1007)
show_shadow = st.sidebar.checkbox("Show Shadows", value=True)

# Generate poster
if st.button("✨ Generate Poster"):
    fig = generate_3d_poster(n_layers=n_layers, seed=seed)
    st.pyplot(fig)

    # Export to PNG buffer
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0.1)
    buf.seek(0)
    st.download_button(
        label="💾 Download Poster (300 DPI PNG)",
        data=buf,
        file_name=f"3d_poster_seed{seed}.png",
        mime="image/png"
    )
    plt.close(fig)

st.markdown("---")
st.markdown("Developed for **Generative Media Art — Week 4** | Demonstrating *depth cues, transparency & layering*.")
