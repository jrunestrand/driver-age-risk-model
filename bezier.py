import numpy as np
import math
import matplotlib.pyplot as plt

def pascal(n):
    return [math.comb(n, i) for i in range(n + 1)]

def bezier_curve(points, num=100):
    points = np.array(points)
    n = len(points) - 1          # degree = number of points - 1
    coeffs = pascal(n)
    t = np.linspace(0, 1, num)

    curve = np.zeros((num, 2))
    for i in range(n + 1):
        term = coeffs[i] * (t**i) * ((1 - t)**(n - i))
        curve += term[:, None] * points[i]

    return curve

# --- Set up the interactive plot ---
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title("Click to add control points")

control_points = []

def on_click(event):
    if event.xdata is None or event.ydata is None:
        return  # ignore clicks outside the axes

    control_points.append([event.xdata, event.ydata])

    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Click to add control points")

    pts = np.array(control_points)
    ax.plot(pts[:, 0], pts[:, 1], 'o--', color='gray', label="Control points")

    if len(control_points) >= 2:
        curve = bezier_curve(control_points)
        ax.plot(curve[:, 0], curve[:, 1], color='blue', label="Bezier curve")

    ax.legend()
    fig.canvas.draw()

fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()