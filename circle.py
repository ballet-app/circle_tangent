import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Funkcja do rysowania okręgu
def draw_circle(ax, center, radius):
    theta = np.linspace(0, 2 * np.pi, 500)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    ax.plot(x, y, label='Okrąg')

# Funkcja do obliczenia stycznej
def compute_tangent_line(center, point):
    # Wektor promienia
    dx = point[0] - center[0]
    dy = point[1] - center[1]

    # Wektor styczny to wektor prostopadły do promienia
    # (np. (-dy, dx))
    tangent_vector = np.array([-dy, dx])
    norm = np.linalg.norm(tangent_vector)
    tangent_unit = tangent_vector / norm

    # Dwa punkty na stycznej (do rysowania)
    scale = 10  # długość stycznej
    pt1 = point + scale * tangent_unit
    pt2 = point - scale * tangent_unit

    # Równanie prostej stycznej: y = mx + b
    if tangent_unit[0] != 0:
        m = tangent_unit[1] / tangent_unit[0]
        b = point[1] - m * point[0]
        equation = f"y = {m:.2f}x + {b:.2f}"
    else:
        equation = f"x = {point[0]:.2f}"

    return pt1, pt2, equation

# Streamlit interfejs
st.title("Rysowanie okręgu i stycznej")
x0 = st.number_input("x współrzędna środka", value=0.0)
y0 = st.number_input("y współrzędna środka", value=0.0)
r = st.number_input("Promień", min_value=0.1, value=5.0)

st.write("Kliknij na okręgu, aby zobaczyć styczną w tym punkcie.")

# Obsługa kliknięcia
clicked_point = st.session_state.get("clicked_point", None)

fig, ax = plt.subplots()
draw_circle(ax, (x0, y0), r)
ax.set_aspect('equal')
ax.set_xlim(x0 - r - 5, x0 + r + 5)
ax.set_ylim(y0 - r - 5, y0 + r + 5)

# Ustawienie obsługi kliknięcia
def onclick(event):
    if event.xdata and event.ydata:
        x, y = event.xdata, event.ydata
        dist = np.hypot(x - x0, y - y0)
        if abs(dist - r) < 0.2:  # tolerancja kliknięcia na okręgu
            st.session_state.clicked_point = (x, y)
        else:
            st.warning("Kliknij bliżej okręgu.")

cid = fig.canvas.mpl_connect('button_press_event', onclick)

# Jeśli kliknięto punkt, rysuj styczną
if clicked_point:
    pt = np.array(clicked_point)
    pt1, pt2, eq = compute_tangent_line((x0, y0), pt)
    ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], 'r--', label='Styczna')
    ax.plot(pt[0], pt[1], 'ro')
    st.markdown(f"**Równanie stycznej:** {eq}")

ax.legend()
st.pyplot(fig)
