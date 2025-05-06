import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def draw_circle(ax, center, radius):
    theta = np.linspace(0, 2 * np.pi, 500)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    ax.plot(x, y, label='Okrąg')

def compute_tangent_line(center, point):
    dx = point[0] - center[0]
    dy = point[1] - center[1]

    tangent_vector = np.array([-dy, dx])
    norm = np.linalg.norm(tangent_vector)
    tangent_unit = tangent_vector / norm

    scale = 10
    pt1 = point + scale * tangent_unit
    pt2 = point - scale * tangent_unit

    if tangent_unit[0] != 0:
        m = tangent_unit[1] / tangent_unit[0]
        b = point[1] - m * point[0]
        equation = f"y = {m:.2f}x + {b:.2f}"
    else:
        equation = f"x = {point[0]:.2f}"

    return pt1, pt2, equation

# --- Streamlit UI ---
st.title("Okrąg, promień i styczna")

x0 = st.number_input("x środka okręgu", value=0.0)
y0 = st.number_input("y środka okręgu", value=0.0)
r = st.number_input("Promień okręgu", min_value=0.1, value=5.0)

st.subheader("Punkt styczności")
px = st.number_input("x punktu", value=x0 + r)
py = st.number_input("y punktu", value=y0)

dist = np.hypot(px - x0, py - y0)
on_circle = np.isclose(dist, r, atol=0.1)

fig, ax = plt.subplots()
draw_circle(ax, (x0, y0), r)

ax.set_aspect('equal')
ax.set_xlim(x0 - r - 5, x0 + r + 5)
ax.set_ylim(y0 - r - 5, y0 + r + 5)
ax.grid(True)

# Środek
ax.plot(x0, y0, 'bo')
ax.text(x0, y0, f'  Środek ({x0:.2f}, {y0:.2f})', color='blue')

if on_circle:
    pt = np.array([px, py])

    # Promień
    ax.plot([x0, px], [y0, py], 'g-', label='Promień')
    ax.text((x0 + px)/2, (y0 + py)/2, f'{dist:.2f}', color='green')

    # Punkt styczności
    ax.plot(px, py, 'ro', label='Punkt styczności')
    ax.text(px, py, f'  ({px:.2f}, {py:.2f})', color='red')

    # Styczna
    pt1, pt2, eq = compute_tangent_line((x0, y0), pt)
    ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], 'r--', label='Styczna')

    st.markdown(f"**Równanie stycznej:** {eq}")
    st.markdown(f"**Współrzędne punktu styczności:** ({px:.2f}, {py:.2f})")
else:
    st.warning("Punkt nie leży na okręgu (dopuszczalne odchylenie: ±0.1).")

ax.legend()
st.pyplot(fig)
