from asyncio import events
import pygame
import sys
from lista_Heroes import ListaHeroes

pygame.init()
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("⚔️ BATALLA DE HEROES ⚔️")

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 80, 80)
VERDE = (80, 255, 120)
AZUL = (100, 160, 255)
GRIS = (50, 50, 50)

fuente = pygame.font.SysFont("Segoe UI Emoji", 32)
fuente_titulo = pygame.font.SysFont("Segoe UI Emoji", 48)
fuente_mensaje = pygame.font.SysFont("Segoe UI Emoji", 24)

class Boton:
    def __init__(self, x, y, w, h, texto, color_fondo, color_texto):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.color_fondo = color_fondo
        self.color_texto = color_texto

    def dibujar(self, pantalla):
        color = self.color_texto if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color_fondo
        pygame.draw.rect(pantalla, color, self.rect, border_radius=10)
        texto_renderizado = fuente.render(self.texto, True, NEGRO)
        pantalla.blit(texto_renderizado, (self.rect.x + 10, self.rect.y + 10))

    def esta_clickeado(self, posicion):
        return evento.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evento.pos)

lista = ListaHeroes()

mensajes = []

def mostrar_mensajes(texto):
    if len(mensajes) >= 6:
        mensajes.pop(0)
    mensajes.append(texto)

def agregar_y_mostrar_mensajes(nombre, nivel, vida, ataque):
    try:
        lista.agregar_heroe(nombre, nivel, vida, ataque)
        mostrar_mensajes(f"✨ Héroe {nombre} agregado.")
    except Exception as e:
        mostrar_mensajes(f"❌ Error al agregar héroe: {e}")

def eliminar_y_mostrar_mensajes(nombre):
    antes = lista.cabeza
    lista.eliminar_heroe(nombre)
    if antes == lista.cabeza:
        mostrar_mensajes(f"❌ Héroe {nombre} no encontrado o no eliminado.")
    else:
        mostrar_mensajes(f"💀 Héroe {nombre} eliminado.")

def mejorar_y_mostrar_mensajes(nombre, inc_vida, inc_ataque):
    heroe = lista.buscar_heroe(nombre)
    if heroe:
        lista.mejorar_heroe(nombre, inc_vida, inc_ataque)
        mostrar_mensajes(f"⚡ Héroe {nombre} mejorado: +{inc_vida} Vida, +{inc_ataque} Ataque.")
    else:
        mostrar_mensajes(f"❌ No se encontró al héroe {nombre}.")

boton_agregar = Boton(600, 150, 150, 40, "Agregar", VERDE, (0, 200, 0))
boton_eliminar = Boton(600, 210, 150, 40, "Eliminar", ROJO, (200, 0, 0))
boton_mejorar = Boton(600, 270, 150, 40, "Mejorar", AZUL, (0, 100, 200))
boton_salir = Boton(600, 330, 150, 40, "Salir", GRIS, (100, 100, 100))

def dibujar_lista_heroes():
    pantalla.fill(NEGRO)

    titulo = fuente_titulo.render("🧙‍♂️ Héroes en la Arena", True, BLANCO)
    pantalla.blit(titulo, (50, 30))

    actual = lista.cabeza
    y = 120
    while actual:
        texto = fuente.render(f"🦸‍♂️ {actual.nombre} - Nivel: {actual.nivel} - Vida: {actual.vida} - Ataque: {actual.ataque}", True, BLANCO)
        pantalla.blit(texto, (50, y))
        y += 40
        actual = actual.siguiente

    for b in [boton_agregar, boton_eliminar, boton_mejorar, boton_salir]:
        b.dibujar(pantalla)

    pygame.draw.rect(pantalla, (30, 30, 30), (30, 450, 740, 120), border_radius=10)
    pantalla.blit(fuente.render("📜 Registro de eventos:", True, VERDE), (40, 455))

    y_texto = 480
    for mensaje in mensajes:
        texto_renderizado = fuente_mensaje.render(mensaje, True, BLANCO)
        pantalla.blit(texto_renderizado, (50, y_texto))
        y_texto += 20

    pygame.display.flip()

def pedir_texto(mensaje):
    texto = ""
    activo = True
    while activo:
        pantalla.fill(NEGRO)
        render_mensaje = fuente.render(mensaje, True, BLANCO)
        render_texto = fuente.render(texto, True, VERDE)
        pantalla.blit(render_mensaje, (50, 250))
        pantalla.blit(render_texto, (50, 300))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    activo = False
                elif evento.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                else:
                    texto += evento.unicode
    return texto
    
ejecutando = True
while ejecutando:
    dibujar_lista_heroes()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        if boton_agregar.esta_clickeado(evento):
            nombre = pedir_texto("Ingrese el nombre del héroe:")
            nivel = int(pedir_texto("Ingrese el nivel del héroe:"))
            vida = int(pedir_texto("Ingrese la vida del héroe:"))
            ataque = int(pedir_texto("Ingrese el ataque del héroe:"))
            agregar_y_mostrar_mensajes(nombre, nivel, vida, ataque)

        if boton_eliminar.esta_clickeado(evento):
            nombre = pedir_texto("Ingrese el nombre del héroe a eliminar:")
            eliminar_y_mostrar_mensajes(nombre)
        
        if boton_mejorar.esta_clickeado(evento):
            nombre = pedir_texto("Ingrese el nombre del héroe a mejorar:")
            inc_vida = int(pedir_texto("Ingrese el incremento de vida:"))
            inc_ataque = int(pedir_texto("Ingrese el incremento de ataque:"))
            mejorar_y_mostrar_mensajes(nombre, inc_vida, inc_ataque)

        if boton_salir.esta_clickeado(evento):
            ejecutando = False

pygame.quit()