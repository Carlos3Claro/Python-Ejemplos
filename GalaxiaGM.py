import numpy as np
import matplotlib.pyplot as plt

def create_galaxy(num_stars_inner=5000, num_stars_outer=15000, arm_tightness=1.5, arm_spread=0.1, num_arms=2, inner_radius_factor=0.2):
    """
    Crea datos para una galaxia espiral con dos poblaciones de estrellas de diferentes colores.

    Args:
        num_stars_inner (int): Número de estrellas para la población interior (amarilla).
        num_stars_outer (int): Número de estrellas para la población exterior (azul).
        arm_tightness (float): Qué tan apretados están los brazos espirales.
        arm_spread (float): Dispersión de las estrellas alrededor de los brazos.
        num_arms (int): Número de brazos espirales.
        inner_radius_factor (float): Factor que define el radio del bulbo interior.

    Returns:
        tuple: Tupla con las coordenadas x, y para la población interior y exterior.
    """

    # Población de estrellas interiores (amarillas - bulbo/halo)
    # Distribución más concéntrica y uniforme
    theta_inner = 2 * np.pi * np.random.rand(num_stars_inner)
    radius_inner = np.random.power(0.5, num_stars_inner) * inner_radius_factor * 10 # Más estrellas cerca del centro
    x_inner = radius_inner * np.cos(theta_inner)
    y_inner = radius_inner * np.sin(theta_inner)

    # Población de estrellas exteriores (azules - brazos espirales)
    x_outer, y_outer = [], []
    for i in range(num_arms):
        # Ángulo base para el brazo
        arm_angle = (2 * np.pi / num_arms) * i

        # Generar radios y ángulos para cada brazo
        r_arm = np.random.rand(num_stars_outer // num_arms) * (1 - inner_radius_factor) * 10 + inner_radius_factor * 10
        theta_arm = arm_tightness * np.log(r_arm + 1e-5) + arm_angle + (np.random.randn(num_stars_outer // num_arms) * arm_spread)

        # Convertir a coordenadas cartesianas
        x_arm = r_arm * np.cos(theta_arm)
        y_arm = r_arm * np.sin(theta_arm)

        x_outer.extend(x_arm)
        y_outer.extend(y_arm)

    return np.array(x_inner), np.array(y_inner), np.array(x_outer), np.array(y_outer)

def plot_galaxy(x_inner, y_inner, x_outer, y_outer):
    """
    Grafica la galaxia con las dos poblaciones de estrellas.
    """
    plt.figure(figsize=(10, 10))
    plt.style.use('dark_background') # Fondo oscuro para simular el espacio

    # Plot de la población interior (amarilla)
    plt.scatter(x_inner, y_inner, s=1, color='gold', alpha=0.6, label='Estrellas antiguas (bulbo/halo)')

    # Plot de la población exterior (azul)
    plt.scatter(x_outer, y_outer, s=0.5, color='cyan', alpha=0.4, label='Estrellas jóvenes (brazos espirales)')

    plt.title('Diseño de Galaxia Espiral (Inspirado en Andrómeda)', fontsize=16)
    plt.xlabel('Coordenada X', fontsize=12)
    plt.ylabel('Coordenada Y', fontsize=12)
    plt.axis('off') # Ocultar los ejes para una mejor visualización espacial
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    x_inner, y_inner, x_outer, y_outer = create_galaxy()
    plot_galaxy(x_inner, y_inner, x_outer, y_outer)