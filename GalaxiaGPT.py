import numpy as np
import matplotlib.pyplot as plt

def generar_bulbo(n, radio_bulbo):
    coords = np.random.normal(scale=radio_bulbo, size=(n, 3))
    coords[:,2] *= 0.1  # aplanar ligeramente en Z
    return coords

def generar_brazos(n, n_brazos, rotacion=2, dispersión=0.5, radio_max=10):
    coords = []
    for i in range(n_brazos):
        θ = np.linspace(0, rotacion * 2*np.pi, n//n_brazos) + (i * 2*np.pi/n_brazos)
        r = np.linspace(0, radio_max, len(θ))
        xs = r * np.cos(θ) + np.random.normal(scale=dispersión, size=len(θ))
        ys = r * np.sin(θ) + np.random.normal(scale=dispersión, size=len(θ))
        zs = np.random.normal(scale=dispersión*0.1, size=len(θ))
        coords.append(np.vstack((xs, ys, zs)).T)
    return np.vstack(coords)

# parámetros
n_bulbo = 2000
n_brazos = 3
n_estrellas = 8000

bulbo = generar_bulbo(n_bulbo, radio_bulbo=2)
brazos = generar_brazos(n_estrellas, n_brazos, rotacion=2.5, dispersión=0.8, radio_max=12)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(bulbo[:,0], bulbo[:,1], bulbo[:,2], s=1, color='gold', alpha=0.7, label='bulbo')
ax.scatter(brazos[:,0], brazos[:,1], brazos[:,2], s=0.5, color='blue', alpha=0.5, label='brazos')
ax.set_axis_off()
plt.legend()
plt.show()
