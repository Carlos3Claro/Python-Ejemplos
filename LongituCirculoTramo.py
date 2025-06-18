import math
import turtle

def calcular_rotaciones(radio, tramo):
    """Calcula el número de rotaciones de un círculo en un tramo dado."""
    circunferencia = 2 * math.pi * radio
    rotaciones = tramo / circunferencia
    return rotaciones

def animar_rotacion(radio, tramo, direccion="izquierda"):
    """Anima la rotación de un círculo en un tramo dado."""

    ventana = turtle.Screen()
    ventana.title("Rotación de un círculo")
    ventana.setup(width=800, height=400)

    # Configuración del círculo
    circulo = turtle.Turtle()
    circulo.shape("circle")
    circulo.shapesize(radio)
    circulo.color("blue")
    circulo.penup()
    circulo.goto(-300, 0)  # Posición inicial a la izquierda
    circulo.pendown()

    # Parámetros de movimiento
    circunferencia = 2 * math.pi * radio
    distancia_por_paso = 1  # Ajustable para suavizar la animación
    grados_por_paso = (360 * distancia_por_paso) / circunferencia

    # Animación
    if direccion == "derecha":
        grados_por_paso *= -1  # Rotación horaria

    for _ in range(int(tramo / distancia_por_paso)):
        circulo.forward(distancia_por_paso)
        circulo.left(grados_por_paso)

    ventana.mainloop()

def main():
    """Función principal del programa."""

    print("=== Simulación de rotación de círculo ===")
    radio = float(input("Radio del círculo (metros): "))
    tramo = float(input("Longitud del tramo (metros, predeterminado = 1): ") or 1)

    rotaciones = calcular_rotaciones(radio, tramo)
    print("\nResultados:")
    print(f"- Rotaciones completas: {rotaciones:.2f}")
    print(f"- Distancia recorrida: {tramo} metros")

    # Opciones adicionales
    tiempo = float(input("\nTiempo total de recorrido (segundos, opcional): ") or 0)
    if tiempo > 0:
        velocidad_lineal = tramo / tiempo
        velocidad_angular = (rotaciones * 360) / tiempo

        print(f"- Velocidad lineal: {velocidad_lineal:.2f} m/s")
        print(f"- Velocidad angular: {velocidad_angular:.2f} grados/s")

        direccion = input("\nDirección de rotación (izquierda/derecha): ").lower()
        animar_rotacion(radio, tramo, direccion)

if __name__ == "__main__":
    main()