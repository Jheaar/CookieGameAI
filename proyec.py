import pygame
import sys
import os
import random
import tkinter as tk
from tkinter import Label, PhotoImage, Button
from PIL import Image, ImageTk
import random
# Inicializar pygame
pygame.init()

#Parametros cambiables
nBombas = 3
nHielos = 10
nRayos = 3

# Constantes para el tamaño de la ventana y el tablero
ANCHO, ALTO = 700, 700
COLOR_FONDO = (255, 255, 255)  # Blanco
COLOR_LINEA = (0, 0, 0)  # Negro
COLOR_BLOQUEADO = (255, 0, 0)  # Rojo
ESPACIO_CUADRADO = ANCHO // 12
MARGEN = ESPACIO_CUADRADO // 2  # Centrar el tablero en la ventana
COLOR_LINEA_NUEVA = (255, 255, 255, 0.0)

COLOR_PREVISUALIZACION = (192, 192, 192)
COLOR_JUGADOR_1 = (0, 0, 255)  # Azul
COLOR_JUGADOR_2 = (0, 255, 0)  # Verde
TAMANO_INDICADOR = ESPACIO_CUADRADO // 2
FUENTE = pygame.font.SysFont('Arial', 24)

# Modificar las constantes para el tamaño de la ventana y el tablero
ANCHO_VENTANA, ALTO_VENTANA = 1100, 700  # Hacer la ventana más ancha
ESPACIO_CUADRADO1 = ALTO_VENTANA // 12
OFFSET_X = (ANCHO_VENTANA - ANCHO) // 2  # Espacio adicional a los lados
OFFSET_Y = (ALTO_VENTANA - ALTO) // 2
# Cargar las imágenes para cada jugador


# Crear la ventana con las nuevas dimensiones
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Juego de la Galletota")
# Rutas relativas desde la ubicación de proyec.py
# Cargar las imágenes para cada jugador (asegúrate de que las rutas sean correctas)
imagen_jugador1 = pygame.image.load('Imagen/jugador1.jpeg').convert_alpha()
imagen_jugador2 = pygame.image.load('Imagen/jugador2.jpeg').convert_alpha()
imagen_bomba = pygame.image.load('Imagen/Bomba.png').convert_alpha()
imagen_hielo = pygame.image.load('Imagen/Hielo.png').convert_alpha()
imagen_rayo = pygame.image.load('Imagen/Rayo.png').convert_alpha()
# Asegúrate de que las imágenes estén escaladas correctamente
imagen_jugador1 = pygame.transform.scale(imagen_jugador1, (ESPACIO_CUADRADO, ESPACIO_CUADRADO))
imagen_jugador2 = pygame.transform.scale(imagen_jugador2, (ESPACIO_CUADRADO, ESPACIO_CUADRADO))
imagen_bomba = pygame.transform.scale(imagen_bomba, (ESPACIO_CUADRADO, ESPACIO_CUADRADO))
imagen_hielo = pygame.transform.scale(imagen_hielo, (ESPACIO_CUADRADO, ESPACIO_CUADRADO))
imagen_rayo = pygame.transform.scale(imagen_rayo, (ESPACIO_CUADRADO, ESPACIO_CUADRADO))
tamaño = 11  # El tamaño del tablero (número de cuadrados por lado)

# Crear las matrices con 'v' para las posiciones vacías
lineas_horizontales = [['v' for _ in range(tamaño)] for _ in range(tamaño + 1)]
lineas_verticales = [['v' for _ in range(tamaño + 1)] for _ in range(tamaño)]

puntaje_jugador1 = 0
puntaje_jugador2 = 0
turno = 'Jugador 1'

cuadrados_completados = [[False] * tamaño for _ in range(tamaño)]

def reemplazar_valor_aleatorio(matriz, valor_antiguo, nuevo_valor, max_cambios):
    # Crear una lista de todas las posiciones donde el valor es igual al valor antiguo
    posiciones = [(i, j) for i, fila in enumerate(matriz) for j, valor in enumerate(fila) if valor == valor_antiguo]
    
    # Mezclar aleatoriamente las posiciones y seleccionar las primeras 'max_cambios' posiciones
    random.shuffle(posiciones)
    posiciones_seleccionadas = posiciones[:max_cambios]
    
    # Reemplazar los valores en las posiciones seleccionadas
    for i, j in posiciones_seleccionadas:
        matriz[i][j] = nuevo_valor

def tablero_lleno(cuadrados):
    for fila in cuadrados:
        if 'v' in fila:  # Si hay algún 'v', aún hay espacio vacío
            return False
    return True

def mostrar_ganador(puntaje_jugador1, puntaje_jugador2):
    # Crear una nueva ventana de tkinter
    root = tk.Tk()
    root.title("Fin del juego")

    # Cargar la imagen y ajustar su tamaño
    imagen_path = 'Imagen/Roller.png'  # Cambia esto por la ruta a tu imagen
    original_img = Image.open(imagen_path)
    resized_img = original_img.resize((150, 150), Image.Resampling.LANCZOS)  # Usar LANCZOS para un mejor resultado
    img = ImageTk.PhotoImage(resized_img)

    # Crear una etiqueta para la imagen
    label_imagen = Label(root, image=img)
    label_imagen.image = img  # Mantener una referencia
    label_imagen.pack()

    # Determinar el mensaje del ganador
    if puntaje_jugador1 > puntaje_jugador2:
        mensaje = "¡Jugador 1 es el ganador!"
    elif puntaje_jugador2 > puntaje_jugador1:
        mensaje = "¡Jugador 2 es el ganador!"
    else:
        mensaje = "¡Es un empate!"

    # Crear una etiqueta para el mensaje
    label_mensaje = Label(root, text=mensaje, font=("Arial", 14))
    label_mensaje.pack()

    # Botón para cerrar la ventana
    boton_cerrar = Button(root, text="Cerrar", command=root.destroy)
    boton_cerrar.pack()
    root.update_idletasks()  # Actualiza la interfaz para calcular el tamaño correcto
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    # Mostrar la ventana hasta que se cierre manualmente
    root.mainloop()

# Configurar los bordes y las áreas bloqueadas para formar un rombo
centro = tamaño // 2
for i in range(centro + 1):
    # Llenar las áreas bloqueadas con 'b'
    for j in range(centro - i):
        lineas_horizontales[i][j] = 'b'
        lineas_horizontales[i][-j - 1] = 'b'
        lineas_horizontales[-i - 1][j] = 'b'
        lineas_horizontales[-i - 1][-j - 1] = 'b'

        # Solo llenamos las verticales hasta el centro, ya que se repiten después
        if i != centro:  # Evitar llenar la línea central dos veces
            lineas_verticales[j][i] = 'b'
            lineas_verticales[j][-i - 1] = 'b'
            lineas_verticales[-j - 1][i] = 'b'
            lineas_verticales[-j - 1][-i - 1] = 'b'

    # Definir los bordes del rombo con '0'
    if i != centro:  # Evitar marcar la línea central dos veces
        lineas_horizontales[i][centro - i] = '0'
        lineas_horizontales[i][centro + i] = '0'
        lineas_horizontales[-i - 1][centro - i] = '0'
        lineas_horizontales[-i - 1][centro + i] = '0'

    lineas_verticales[centro - i][i] = '0'
    lineas_verticales[centro + i][i] = '0'
    lineas_verticales[centro - i][-i - 1] = '0'
    lineas_verticales[centro + i][-i - 1] = '0'

# Asegúrate de que las líneas del centro no tengan '0' si tu diseño no lo requiere
#lineas_horizontales[centro] = ['v' for _ in range(tamaño)]
lineas_horizontales[centro] = ['0'] + ['v'] * (tamaño - 2) + ['0']
lineas_horizontales[centro + 1] = ['0'] + ['v'] * (tamaño - 2) + ['0']
# Resto del código de Pygame...


cuadrados = [
    ['b', 'b', 'b', 'b', 'b', 'v', 'b', 'b', 'b', 'b', 'b'],  # Primera fila
    ['b', 'b', 'b', 'b', 'v', 'v', 'v', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'v', 'v', 'v', 'v', 'v', 'b', 'b', 'b'],
    ['b', 'b', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'b', 'b'],
    ['b', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'b'],
    ['v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v'],
    ['b', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'b'],
    ['b', 'b', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'b', 'b'],
    ['b', 'b', 'b', 'v', 'v', 'v', 'v', 'v', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'v', 'v', 'v', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'b', 'v', 'b', 'b', 'b', 'b', 'b'],
]
def mover_ia(nivel, lineas_horizontales, lineas_verticales, tamaño):
    if nivel == 'principiante':
        return mover_aleatorio(lineas_horizontales, lineas_verticales, tamaño)
    elif nivel == 'intermedio':
        # Implementar una estrategia más inteligente
        pass
    elif nivel == 'experto':
        # Implementar una estrategia aún más inteligente
        pass

def mover_aleatorio(lineas_horizontales, lineas_verticales, tamaño):
    movimientos_posibles = []
    for i in range(tamaño):
        for j in range(tamaño):
            if lineas_horizontales[i][j] == 'v':
                movimientos_posibles.append(('h', i, j))
            if lineas_verticales[i][j] == 'v':
                movimientos_posibles.append(('v', i, j))
    return random.choice(movimientos_posibles) if movimientos_posibles else None


def obtener_posicion_matriz(x, y):
    fila = (y - offset_y) // ESPACIO_CUADRADO
    columna = (x - offset_x) // ESPACIO_CUADRADO
    return fila, columna

def es_posicion_valida(fila, columna, matriz):
    if 0 <= fila < len(matriz) and 0 <= columna < len(matriz[0]):
        return matriz[fila][columna] == 'v'
    return False


def verificar_cuadrado_completo(fila, columna):
    global turno, puntaje_jugador1, puntaje_jugador2
    cuadrados_completados_ahora = 0

    # Verifica cuadrado directamente afectado por la línea actual y el cuadrado adyacente si existe
    cuadrados_para_verificar = [
        (fila, columna),  # Cuadrado inmediato si la línea es horizontal o izquierdo si es vertical
    ]
    if fila > 0:  # Añade el cuadrado superior si la línea es horizontal
        cuadrados_para_verificar.append((fila - 1, columna))
    if columna > 0:  # Añade el cuadrado a la izquierda si la línea es vertical
        cuadrados_para_verificar.append((fila, columna - 1))

    for f, c in cuadrados_para_verificar:
        if f < tamaño and c < tamaño:
            if (lineas_horizontales[f][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_horizontales[f + 1][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_verticales[f][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_verticales[f][c + 1] in ['Jugador 1', 'Jugador 2', '0']):
                if cuadrados[f][c] == 'pb':
                    if cuadrados[f-1][c+1]!='b':
                        cuadrados[f-1][c+1]='v'
                    if cuadrados[f][c+1]!='b':
                        cuadrados[f][c+1]='v'
                    if cuadrados[f+1][c+1]!='b':
                        cuadrados[f+1][c+1]='v'
                    if cuadrados[f-1][c]!='b':
                        cuadrados[f-1][c]='v'
                    if cuadrados[f][c]!='b':
                        cuadrados[f][c]='v'
                    if cuadrados[f+1][c]!='b':
                        cuadrados[f+1][c]='v'
                    if cuadrados[f-1][c-1]!='b':
                        cuadrados[f-1][c-1]='v'
                    if cuadrados[f][c-1]!='b':
                        cuadrados[f][c-1]='v'
                    if cuadrados[f+1][c-1]!='b':
                        cuadrados[f+1][c-1]='v'
                    #Eliminacion de lineas que rodean al cuadrado
                    if lineas_horizontales[f][c] != '0' and lineas_horizontales[f][c] != 'b':
                        lineas_horizontales[f][c] = 'v'
                    if lineas_horizontales[f+1][c] != '0' and lineas_horizontales[f+1][c] != 'b':
                        lineas_horizontales[f+1][c] = 'v'

                    # Corrigiendo las condiciones para lineas_verticales
                    if lineas_verticales[f][c] != '0' and lineas_verticales[f][c] != 'b':
                        lineas_verticales[f][c] = 'v'
                    if lineas_verticales[f][c+1] != '0' and lineas_verticales[f][c+1] != 'b':
                        lineas_verticales[f][c+1] = 'v'
                    if lineas_verticales[f-1][c+1] != '0' and lineas_verticales[f-1][c+1] != 'b':
                        lineas_verticales[f-1][c+1] = 'v'
                    if lineas_verticales[f+1][c+1] != '0' and lineas_verticales[f+1][c+1] != 'b':
                        lineas_verticales[f+1][c+1] = 'v'
                    if lineas_verticales[f-1][c] != '0' and lineas_verticales[f-1][c] != 'b':
                        lineas_verticales[f-1][c] = 'v'
                    if lineas_verticales[f+1][c] != '0' and lineas_verticales[f+1][c] != 'b':
                        lineas_verticales[f+1][c] = 'v'

                    # Corrigiendo las condiciones para lineas_horizontales exteriores
                    if lineas_horizontales[f][c+1] != '0' and lineas_horizontales[f][c+1] != 'b':
                        lineas_horizontales[f][c+1] = 'v'
                    if lineas_horizontales[f][c-1] != '0' and lineas_horizontales[f][c-1] != 'b':
                        lineas_horizontales[f][c-1] = 'v'
                    if lineas_horizontales[f+1][c+1] != '0' and lineas_horizontales[f+1][c+1] != 'b':
                        lineas_horizontales[f+1][c+1] = 'v'
                    if lineas_horizontales[f+1][c-1] != '0' and lineas_horizontales[f+1][c-1] != 'b':
                        lineas_horizontales[f+1][c-1] = 'v'

                elif cuadrados[f][c] == 'ph':
                    if turno == 'Jugador 1':
                        cuadrados[f][c] = '1'
                        turno = 'Jugador 2'
                    else:
                        cuadrados[f][c] = '2'
                        turno == 'Jugador 1'

                elif not cuadrados_completados[f][c]:  # Si el cuadrado no estaba ya completado
                    cuadrados_completados[f][c] = True
                    cuadrados_completados_ahora += 1
                    if turno == 'Jugador 1':
                        cuadrados[f][c]='1'
                    else:
                        cuadrados[f][c]='2'
    if cuadrados_completados_ahora == 0:
        turno = 'Jugador 2' if turno == 'Jugador 1' else 'Jugador 1'

def dibujar_cuadrados_completos():
    for fila in range(tamaño - 1):
        for columna in range(tamaño - 1):
            ganador = verificar_cuadrado_completo(fila, columna)
            if ganador:
                # Calcula la posición central del cuadrado
                x = columna * ESPACIO_CUADRADO + offset_x + ESPACIO_CUADRADO // 2
                y = fila * ESPACIO_CUADRADO + offset_y + ESPACIO_CUADRADO // 2
                imagen = imagen_jugador1 if ganador == 'Jugador 1' else imagen_jugador2
                imagen = pygame.transform.scale(imagen, (ESPACIO_CUADRADO, ESPACIO_CUADRADO))
                x -= imagen.get_width() // 2
                y -= imagen.get_height() // 2
                pantalla.blit(imagen, (x, y))

def dibujar_indicadores_jugadores():
    # Define el tamaño de las fichas para los jugadores
    ficha_tamaño = TAMANO_INDICADOR * 3

    # Calcular el puntaje basado en el número de '1' y '2' en la matriz cuadrados
    puntaje_jugador1 = sum(fila.count('1') for fila in cuadrados)
    puntaje_jugador2 = sum(fila.count('2') for fila in cuadrados)

    # Dibuja los indicadores para Jugador 1 a la izquierda
    texto_jugador_1 = FUENTE.render('Jugador 1', True, COLOR_JUGADOR_1)
    ficha_jugador_1 = pygame.transform.scale(imagen_jugador1, (ficha_tamaño, ficha_tamaño))
    pantalla.blit(texto_jugador_1, (OFFSET_X - texto_jugador_1.get_width() - 20 - ficha_jugador_1.get_width(), MARGEN))
    pantalla.blit(ficha_jugador_1, (OFFSET_X - texto_jugador_1.get_width() - 110, MARGEN + texto_jugador_1.get_height() + 10))
    texto_puntaje_1 = FUENTE.render(f'Puntaje: {puntaje_jugador1}', True, COLOR_JUGADOR_1)
    pantalla.blit(texto_puntaje_1, (OFFSET_X - texto_puntaje_1.get_width() - 20, MARGEN + ficha_jugador_1.get_height() + 70))

    # Dibuja los indicadores para Jugador 2 a la derecha
    texto_jugador_2 = FUENTE.render('Jugador 2', True, COLOR_JUGADOR_2)
    ficha_jugador_2 = pygame.transform.scale(imagen_jugador2, (ficha_tamaño, ficha_tamaño))
    pantalla.blit(texto_jugador_2, (ANCHO_VENTANA - OFFSET_X + 10, MARGEN))
    pantalla.blit(ficha_jugador_2, (ANCHO_VENTANA - OFFSET_X -80 + texto_jugador_2.get_width() + 10, MARGEN + texto_jugador_2.get_height() + 10))
    texto_puntaje_2 = FUENTE.render(f'Puntaje: {puntaje_jugador2}', True, COLOR_JUGADOR_2)
    pantalla.blit(texto_puntaje_2, (ANCHO_VENTANA - OFFSET_X + 10, MARGEN + ficha_jugador_2.get_height() + 70))

    # Dibuja el indicador de turno
    if turno == 'Jugador 1':
        pygame.draw.circle(pantalla, COLOR_JUGADOR_1, (OFFSET_X - 80, MARGEN + texto_jugador_1.get_height() // 2), TAMANO_INDICADOR // 2)
    else:
        pygame.draw.circle(pantalla, COLOR_JUGADOR_2, (ANCHO_VENTANA - OFFSET_X + texto_jugador_2.get_width() -50 + ficha_jugador_2.get_width(), MARGEN + texto_jugador_2.get_height() // 2), TAMANO_INDICADOR // 2)

# Calcula el ancho y alto del área del tablero
ancho_tablero = tamaño * ESPACIO_CUADRADO
alto_tablero = tamaño * ESPACIO_CUADRADO

# Calcula el desplazamiento necesario para centrar el tablero
offset_x = (ANCHO_VENTANA - ancho_tablero) // 2
offset_y = (ALTO_VENTANA - alto_tablero) // 2

def dibujar_tablero():
    pantalla.fill(COLOR_FONDO)
    max_hor = len(lineas_horizontales[0])
    max_ver = len(lineas_verticales[0])
    max_cua = len(cuadrados[0])
    for fila in range(11):  # Ajusta esto según el número de filas y columnas de tu matriz
        for columna in range(11):
            rect = pygame.Rect(columna * ESPACIO_CUADRADO+ offset_x, fila * ESPACIO_CUADRADO+ offset_y, ESPACIO_CUADRADO, ESPACIO_CUADRADO)
            pygame.draw.rect(pantalla, COLOR_LINEA_NUEVA, rect, 1)
            if cuadrados[fila][columna] == '1':
                pantalla.blit(imagen_jugador1, (columna * ESPACIO_CUADRADO+ offset_x, fila * ESPACIO_CUADRADO+ offset_y))
            elif cuadrados[fila][columna] == '2':
                pantalla.blit(imagen_jugador2, (columna * ESPACIO_CUADRADO+ offset_x, fila * ESPACIO_CUADRADO+ offset_y))
            elif cuadrados[fila][columna] == 'pb':
                pantalla.blit(imagen_bomba, (columna * ESPACIO_CUADRADO+ offset_x, fila * ESPACIO_CUADRADO+ offset_y))
            elif cuadrados[fila][columna] == 'ph':
                pantalla.blit(imagen_hielo, (columna * ESPACIO_CUADRADO+ offset_x, fila * ESPACIO_CUADRADO+ offset_y))
            elif cuadrados[fila][columna] == 'pr':
                pantalla.blit(imagen_rayo, (columna * ESPACIO_CUADRADO+ offset_x, fila * ESPACIO_CUADRADO+ offset_y))
    # Dibujar las líneas horizontales
    for i, fila in enumerate(lineas_horizontales):
        for j, valor in enumerate(fila):

            if valor == 'Jugador 1':
                # Dibuja la línea horizontal del Jugador 1
                inicio = (j * ESPACIO_CUADRADO + offset_x, (i) * ESPACIO_CUADRADO + offset_y)
                fin = ((j + 1) * ESPACIO_CUADRADO + offset_x, (i) * ESPACIO_CUADRADO + offset_y)
                pygame.draw.line(pantalla, COLOR_JUGADOR_1, inicio, fin, 5)
            elif valor == 'Jugador 2':
                # Dibuja la línea horizontal del Jugador 2
                inicio = (j * ESPACIO_CUADRADO + offset_x, (i) * ESPACIO_CUADRADO + offset_y)
                fin = ((j + 1) * ESPACIO_CUADRADO + offset_x, (i) * ESPACIO_CUADRADO + offset_y)
                pygame.draw.line(pantalla, COLOR_JUGADOR_2, inicio, fin, 5)

            inicio = (j * ESPACIO_CUADRADO + offset_x, i * ESPACIO_CUADRADO + offset_y)
            fin = ((j + 1) * ESPACIO_CUADRADO + offset_x, i * ESPACIO_CUADRADO + offset_y)
            if valor == '0':  # Borde
                pygame.draw.line(pantalla, COLOR_LINEA, inicio, fin, 5)
            elif valor == 'b':  # Bloqueado
                pygame.draw.line(pantalla, COLOR_BLOQUEADO, inicio, fin, 3)

    # Dibujar las líneas verticales
    for i, fila in enumerate(lineas_verticales):
        for j, valor in enumerate(fila):

            if valor == 'Jugador 1':
                # Dibuja la línea horizontal del Jugador 1
                inicio = (j * ESPACIO_CUADRADO + offset_x, i * ESPACIO_CUADRADO + offset_y)
                fin = (j * ESPACIO_CUADRADO + offset_x, (i + 1) * ESPACIO_CUADRADO + offset_y)
                pygame.draw.line(pantalla, COLOR_JUGADOR_1, inicio, fin, 5)
            elif valor == 'Jugador 2':
                # Dibuja la línea horizontal del Jugador 2
                inicio = (j * ESPACIO_CUADRADO + offset_x, i * ESPACIO_CUADRADO + offset_y)
                fin = (j * ESPACIO_CUADRADO + offset_x, (i + 1) * ESPACIO_CUADRADO + offset_y)
                pygame.draw.line(pantalla, COLOR_JUGADOR_2, inicio, fin, 5)

            inicio = (j * ESPACIO_CUADRADO + offset_x, i * ESPACIO_CUADRADO + offset_y)
            fin = (j * ESPACIO_CUADRADO + offset_x, (i + 1) * ESPACIO_CUADRADO + offset_y)
            if valor == '0':  # Borde
                pygame.draw.line(pantalla, COLOR_LINEA, inicio, fin, 5)
            elif valor == 'b':  # Bloqueado
                pygame.draw.line(pantalla, COLOR_BLOQUEADO, inicio, fin, 3)

    # No necesitas dibujar 'v' (vacío) o 'b' (bloqueado) para los cuadrados
    # Aquí iría cualquier lógica de dibujo para los cuadrados, si es necesario
    dibujar_indicadores_jugadores()

reemplazar_valor_aleatorio(cuadrados, 'v', 'pb', nBombas)
reemplazar_valor_aleatorio(cuadrados, 'v', 'ph', nHielos)

# Bucle principal

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Obtener la posición del mouse cuando se hace clic
            x, y = pygame.mouse.get_pos()

            # Calcular la posición de la línea en la matriz
            columna = (x - OFFSET_X) // ESPACIO_CUADRADO
            fila = (y - OFFSET_Y) // ESPACIO_CUADRADO
            pos_x_exacta = (x - OFFSET_X) % ESPACIO_CUADRADO
            pos_y_exacta = (y - OFFSET_Y) % ESPACIO_CUADRADO
            if columna < tamaño and fila < tamaño:
                if pos_x_exacta > pos_y_exacta:
                    if es_posicion_valida(fila, columna, lineas_horizontales):
                        lineas_horizontales[fila][columna] = turno
                        verificar_cuadrado_completo(fila, columna)
                else:
                    if es_posicion_valida(fila, columna, lineas_verticales):
                        lineas_verticales[fila][columna] = turno
                        verificar_cuadrado_completo(fila, columna)
    # Dibujar el tablero antes de previsualizar la línea
    pantalla.fill(COLOR_FONDO)
    dibujar_cuadrados_completos()
    dibujar_tablero()
    if tablero_lleno(cuadrados):
        mostrar_ganador(puntaje_jugador1, puntaje_jugador2)
        pygame.quit()
        sys.exit()

# Previsualizar la línea cuando el mouse se mueve sobre el tablero
    if pygame.mouse.get_focused() and pantalla.get_rect().collidepoint(pygame.mouse.get_pos()):
        x, y = pygame.mouse.get_pos()
        columna = (x - OFFSET_X) // ESPACIO_CUADRADO
        fila = (y - OFFSET_Y) // ESPACIO_CUADRADO

        # Calcular las coordenadas de la línea gris de previsualización
        inicio_x = columna * ESPACIO_CUADRADO + OFFSET_X
        inicio_y = fila * ESPACIO_CUADRADO + OFFSET_Y
        fin_x = columna * ESPACIO_CUADRADO + OFFSET_X
        fin_y = fila * ESPACIO_CUADRADO + OFFSET_Y

        # Ajustar la posición de la línea para que esté medio cuadrado a la derecha y medio cuadrado hacia abajo
        if columna < tamaño and fila < tamaño:
            pos_x_exacta = (x - OFFSET_X) % ESPACIO_CUADRADO
            pos_y_exacta = (y - OFFSET_Y) % ESPACIO_CUADRADO
            if pos_x_exacta > pos_y_exacta:
                fin_x += ESPACIO_CUADRADO  # Ajuste para cubrir un cuadrado completo
            else:
                fin_y += ESPACIO_CUADRADO  # Ajuste para cubrir un cuadrado completo

        # Dibujar la línea de previsualización en gris
        pygame.draw.line(pantalla, COLOR_PREVISUALIZACION, (inicio_x + (ESPACIO_CUADRADO/2), inicio_y + (ESPACIO_CUADRADO/2)), (fin_x + (ESPACIO_CUADRADO/2), fin_y + (ESPACIO_CUADRADO/2)), 3)
    # Actualizar la pantalla después de cada evento
    pygame.display.flip()