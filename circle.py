import numpy as np
import matplotlib.pyplot as plt

# Parametry okręgu
center = (2, 3)
radius = 4

# Tworzenie danych do okręgu
theta = np.linspace(0, 2 * np.pi, 1000)
x_circle = center[0] + radius * np.cos(theta)
y_circle = center[1] + radius * np.sin(theta)

# Tworzenie wykresu
fig, ax = plt.subplots()
circle_line, = ax.plot(x_circle, y_circle, label='Okrąg')
tangent_line, = ax.plot([], [], 'r-', label='Styczna')
tangent_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10, verticalalignment='top')

ax.set_aspect('equal')
ax.set_title('Kliknij punkt na okręgu, aby narysować styczną')
ax.set_xlim(center[0] - radius - 2, center[0] + radius + 2)
ax.set_ylim(center[1] - radius - 2, center[1] + radius + 2)

def on_click(event):
    if not event.inaxes:
        return
    
    # Sprawdź, czy kliknięto blisko okręgu
    dx = event.xdata - center[0]
    dy = event.ydata - center[1]
    distance = np.hypot(dx, dy)

    if abs(distance - radius) < 0.1:  # tolerancja
        x0, y0 = event.xdata, event.ydata

        # Wektor promienia
        vx, vy = dx, dy

        # Wektor styczny: prostopadły do promienia
        tx, ty = -vy, vx

        # Normalizacja wektora stycznego
        length = np.hypot(tx, ty)
        tx /= length
        ty /= length

        # Punkty do rysowania stycznej
        scale = 10
        x_tangent = [x0 - tx * scale, x0 + tx * scale]
        y_tangent = [y0 - ty * scale, y0 + ty * scale]
        tangent_line.set_data(x_tangent, y_tangent)

        # Obliczanie i wyświetlanie równania stycznej
        if tx != 0:
            m = ty / tx
            b = y0 - m * x0
            eq = f"y = {m:.2f}x + {b:.2f}"
        else:
            eq = f"x = {x0:.2f}"

        tangent_text.set_text(f"Styczna: {eq}")
        fig.canvas.draw()

# Podłącz kliknięcie myszką
fig.canvas.mpl_connect('button_press_event', on_click)

plt.legend()
plt.show()
