import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la galaxia
num_stars = 1000
arms = 2
spread = 0.5
rotation = 5

# Generar estrellas
r = np.random.rand(num_stars) ** 0.5  # distribuye más estrellas en el centro
theta = r * rotation * 2 * np.pi

x = r * np.cos(theta)
y = r * np.sin(theta)

# Añadir curvatura tipo espiral
arm_offset = (2 * np.pi) / arms
x_all, y_all, colors = [], [], []

for i in range(arms):
    angle_offset = i * arm_offset
    x_rot = x * np.cos(angle_offset) - y * np.sin(angle_offset)
    y_rot = x * np.sin(angle_offset) + y * np.cos(angle_offset)

    x_all.extend(x_rot + np.random.normal(0, spread, num_stars))
    y_all.extend(y_rot + np.random.normal(0, spread, num_stars))

    # Color alterno por brazo
    color = ['deepskyblue' if i % 2 == 0 else 'orchid'] * num_stars
    colors.extend(color)

# Graficar
plt.figure(figsize=(8, 8))
plt.scatter(x_all, y_all, c=colors, s=1, alpha=0.7)
plt.axis('off')
plt.title("🌌 Galaxia estilo Andrómeda", fontsize=14)
plt.show()