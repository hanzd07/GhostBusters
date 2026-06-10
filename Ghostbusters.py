import tkinter as tk
import random
import time

# --- Configuración del Juego ---
ANCHO = 800
ALTO = 600

# Duración del fantasma en pantalla (segundos) - ¡Ajusta para cambiar la dificultad!
DURACION_FANTASMA = 1.5 
OBJETIVO_CAPTURAS = 10
LIMITE_FALLOS_SEGUIDOS = 3
PUNTOS_POR_CAPTURA = 100

# --- Variables de Control ---
capturas = 0
fallos_seguidos = 0
puntuacion = 0
juego_activo = True
tiempo_siguiente_fantasma = 0 

# --- Datos de los Fantasmas (Colores Estilo Retro/Pac-Man) ---
fantasmas_datos = [
    {"color": "#FF0000", "nombre": "Blinky"},    # Rojo
    {"color": "#00FFFF", "nombre": "Inky"},      # Cian
    {"color": "#FF00FF", "nombre": "Pinky"},     # Rosa
    {"color": "#FFA500", "nombre": "Clyde"},     # Naranja
    {"color": "#00FF00", "nombre": "Spooky"}     # Verde Retro
]

# --- Configuración de la Ventana Principal ---
ventana = tk.Tk()
ventana.title("GHOST HUNTER - CODE IN PLACE")

# Canvas con fondo gris muy oscuro (Casi negro retro)
canvas = tk.Canvas(ventana, width=ANCHO, height=ALTO, bg="#111111")
canvas.pack()

# Variables globales para los objetos gráficos
fantasma_forma = None
texto_mensaje = None
texto_puntuacion = None

# --- Funciones del Juego ---

def limpiar_fantasma_actual():
    """Borra todos los elementos del fantasma actual del canvas y resetea su estado."""
    global fantasma_forma
    if fantasma_forma:
        canvas.delete(fantasma_forma)
        fantasma_forma = None  # Marcamos que ya no hay un fantasma activo en pantalla
    canvas.delete("cuerpo_fantasma")
    canvas.delete("ojo_fantasma")
    canvas.delete("pupila_fantasma")

def crear_fantasma(datos):
    """Dibuja un fantasma con estética retro en el lienzo."""
    global fantasma_forma
    
    # Limpiamos el fantasma anterior antes de pintar uno nuevo
    limpiar_fantasma_actual()

    # Coordenadas aleatorias seguras (evitando los bordes del canvas)
    x = random.randint(50, ANCHO - 100)
    y = random.randint(50, ALTO - 100)
    
    tamano = 50
    color = datos["color"]

    # Parte superior del fantasma (Cabeza redonda)
    fantasma_forma = canvas.create_oval(x, y, x + tamano, y + tamano, fill=color, outline=color)
    
    # Cuerpo inferior (Rectángulo para darle la forma clásica de Pac-Man)
    canvas.create_rectangle(x, y + tamano/2, x + tamano, y + tamano * 1.2, fill=color, outline=color, tags="cuerpo_fantasma")

    # Ojos blancos retro
    canvas.create_oval(x + 10, y + 12, x + 20, y + 24, fill="white", outline="white", tags="ojo_fantasma")
    canvas.create_oval(x + 30, y + 12, x + 40, y + 24, fill="white", outline="white", tags="ojo_fantasma")
    
    # Pupilas azules mirando hacia un lado
    canvas.create_oval(x + 14, y + 16, x + 18, y + 20, fill="blue", outline="blue", tags="pupila_fantasma")
    canvas.create_oval(x + 34, y + 16, x + 38, y + 20, fill="blue", outline="blue", tags="pupila_fantasma")

def al_dar_clic(event):
    """Maneja los clics del usuario en la pantalla."""
    global capturas, fallos_seguidos, puntuacion, juego_activo, tiempo_siguiente_fantasma

    if not juego_activo:
        return

    # Verificar si el clic cayó dentro del área del fantasma
    if fantasma_forma:
        coords = canvas.coords(fantasma_forma)
        if (coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3] + 20):
            # ¡Captura exitosa!
            capturas += 1
            fallos_seguidos = 0  # Resetea los fallos consecutivos de inmediato
            puntuacion += PUNTOS_POR_CAPTURA
            actualizar_marcador()
            
            limpiar_fantasma_actual()
            revisar_estado_juego()
            
            if juego_activo:
                # Hace que aparezca otro fantasma inmediatamente sin esperar el contador viejo
                tiempo_siguiente_fantasma = time.time()
            return

    # ¡Fallo! El usuario hizo clic en la pantalla vacía o erró el tiro
    fallos_seguidos += 1
    actualizar_marcador()  # ¡CORRECCIÓN! Actualiza el marcador visual de inmediato al fallar
    mostrar_mensaje_temporal("Missed! Click on a ghost! Haha!", "red")
    revisar_estado_juego()

def mostrar_mensaje_temporal(texto, color):
    """Muestra un texto rápido en pantalla y lo borra después."""
    global texto_mensaje
    if texto_mensaje:
        canvas.delete(texto_mensaje)
    texto_mensaje = canvas.create_text(ANCHO/2, ALTO/2, text=texto, fill=color, font=("Courier", 28, "bold"))
    ventana.after(600, lambda: canvas.delete(texto_mensaje))

def actualizar_marcador():
    """Actualiza la puntuación en la esquina superior izquierda."""
    global texto_puntuacion
    if texto_puntuacion:
        canvas.delete(texto_puntuacion)
    texto_puntuacion = canvas.create_text(180, 30, text=f"SCORE: {puntuacion} | CAUGHT: {capturas}/{OBJETIVO_CAPTURAS} | MISSES: {fallos_seguidos}/3", fill="white", font=("Courier", 12, "bold"))

def revisar_estado_juego():
    """Revisa las condiciones de victoria o derrota."""
    global juego_activo
    if capturas >= OBJETIVO_CAPTURAS:
        juego_activo = False
        limpiar_fantasma_actual()
        canvas.create_text(ANCHO/2, ALTO/2 - 30, text="YOU WIN!", fill="#00FF00", font=("Courier", 60, "bold"))
        canvas.create_text(ANCHO/2, ALTO/2 + 50, text=f"FINAL SCORE: {puntuacion}", fill="white", font=("Courier", 20, "bold"))
    elif fallos_seguidos >= LIMITE_FALLOS_SEGUIDOS:
        juego_activo = False
        limpiar_fantasma_actual()
        canvas.create_text(ANCHO/2, ALTO/2 - 30, text="GAME OVER", fill="#FF0000", font=("Courier", 60, "bold"))
        canvas.create_text(ANCHO/2, ALTO/2 + 50, text=f"Too many misses! Final Score: {puntuacion}", fill="white", font=("Courier", 20, "bold"))

def bucle_principal():
    """Bucle del juego que controla los tiempos de aparición usando .after de tkinter."""
    global juego_activo, tiempo_siguiente_fantasma, fallos_seguidos

    if not juego_activo:
        return

    tiempo_actual = time.time()
    
    # Si el tiempo en pantalla del fantasma expiró
    if tiempo_actual >= tiempo_siguiente_fantasma:
        # Solo contará como fallo por tiempo si REALMENTE había un fantasma vivo en pantalla
        if fantasma_forma is not None:
            fallos_seguidos += 1
            actualizar_marcador()
            mostrar_mensaje_temporal("Too Slow! Haha!", "orange")
            revisar_estado_juego()

        if juego_activo:
            # Selecciona un fantasma aleatorio de la lista y lo dibuja
            fantasma_aleatorio = random.choice(fantasmas_datos)
            crear_fantasma(fantasma_aleatorio)
            # Define cuándo debe desaparecer/cambiar el siguiente
            tiempo_siguiente_fantasma = tiempo_actual + DURACION_FANTASMA

    # Se ejecuta a sí misma cada 100 milisegundos para revisar el estado del tiempo
    ventana.after(100, bucle_principal)

# --- Inicio del Juego ---
actualizar_marcador()
canvas.bind("<Button-1>", al_dar_clic) # Vincula el clic izquierdo del ratón
bucle_principal()

# Levanta la ventana gráfica
ventana.mainloop()