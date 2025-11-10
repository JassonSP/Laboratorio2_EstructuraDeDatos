import random
import pygame
import sys
from lista_Heroes import ListaHeroes
from lista_Turnos import ListaCircularTurnos

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
CAJA = (30, 30, 30)

fuente = pygame.font.SysFont("Segoe UI Emoji", 28)
fuente_titulo = pygame.font.SysFont("Segoe UI Emoji", 38)
fuente_mensaje = pygame.font.SysFont("Segoe UI Emoji", 20)

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

    def esta_clickeado(self, evento):
        return evento.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evento.pos)

lista = ListaHeroes()

mensajes = []

def mostrar_mensajes(texto):
    if len(mensajes) >= 4:
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
boton_eliminar = Boton(600, 210, 150, 40, "Eliminar", ROJO, (255, 100, 100))
boton_mejorar = Boton(600, 270, 150, 40, "Mejorar", AZUL, (100, 180, 255))
boton_batalla = Boton(600, 330, 150, 40, "Iniciar Batalla", (255, 230, 90), (255, 255, 150))
boton_salir = Boton(600, 390, 150, 40, "Salir", GRIS, (180, 180, 180))

def iniciar_batalla(turno_actual=None):
    pantalla.fill(NEGRO)
    titulo = fuente_titulo.render("⚔️ Batalla De Héroes ⚔️", True, VERDE)
    pantalla.blit(titulo, (40, 20))
    
    y = 110
    actual = lista.cabeza
    idx = 0
    while actual:
        color = BLANCO if actual.nombre != turno_actual else AZUL
        linea = f"🦸‍♂️ {actual.nombre} - Nivel: {actual.nivel} - Vida: {actual.vida} - Ataque: {actual.ataque}"
        render = fuente.render(linea, True, color)
        pantalla.blit(render, (40, y + idx*44))
        idx += 1
        actual = actual.siguiente

    pygame.draw.rect(pantalla, CAJA, (680, 100, 200, 360), border_radius=12)
    for b in [boton_agregar, boton_eliminar, boton_mejorar, boton_batalla, boton_salir]:
        b.dibujar(pantalla)

    pygame.draw.rect(pantalla, (18, 18, 18), (30, 420, 820, 200), border_radius=10)
    pantalla.blit(fuente.render("📜 Registro de eventos:", True, VERDE), (40, 455))

    y_texto = 490
    for mensaje in mensajes:
        texto_renderizado = fuente_mensaje.render(mensaje, True, BLANCO)
        pantalla.blit(texto_renderizado, (50, y_texto))
        y_texto += 20
    pygame.display.flip()


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

    y_texto = 490
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

def simular_batalla(rondas=5, turno_delay_ms=700):
    turnos = ListaCircularTurnos()
    actual = lista.cabeza
    count = 0
    while actual:
        if actual.vida > 0:
            turnos.agregar_turno(actual.nombre)
            count += 1
        actual = actual.siguiente

    if count <= 1:
        agregar_y_mostrar_mensajes("⚠️ No hay suficientes héroes para combatir.")
        return

    agregar_y_mostrar_mensajes("🔥 Comienza la batalla!")
    pygame.event.pump()

    for ronda in range(1, rondas + 1):
        agregar_y_mostrar_mensajes(f"🔁 Ronda {ronda} iniciada")
        jugadores_en_ronda = len(turnos.mostrar_turnos())
        for i in range(jugadores_en_ronda):
            nombre_turno = turnos.siguiente_turno()
            if nombre_turno is None:
                break

            dibujar_lista_heroes(turno_actual=nombre_turno)

            her = lista.buscar_heroe(nombre_turno)
            if not her or her.PV <= 0:
                if her and her.PV <= 0:
                    turnos.eliminar_turno(nombre_turno)
                agregar_y_mostrar_mensajes(f"❌ {nombre_turno} no disponible para turno.")
                pygame.event.pump()
                pygame.time.delay(150)
                continue

            accion = random.choice(["ataque", "curacion", "pasar"])
            valor = random.randint(5, 30)

            if accion == "curacion":
                her.PV += valor
                agregar_y_mostrar_mensajes(f"💚 {nombre_turno} se curó +{valor} PV (PV now: {her.PV})")
            elif accion == "ataque":
                objetivo = turnos.obtener_objetivo_aleatorio(nombre_turno, lista)
                if objetivo:
                    objetivo.PV -= valor
                    agregar_y_mostrar_mensajes(f"💥 {nombre_turno} atacó a {objetivo.nombre} (-{valor} PV, queda {max(0, objetivo.PV)})")
                    if objetivo.PV <= 0:
                        agregar_y_mostrar_mensajes(f"☠️ {objetivo.nombre} ha caído")
                        lista.eliminar_heroe(objetivo.nombre)
                        turnos.eliminar_turno(objetivo.nombre)
                else:
                    agregar_y_mostrar_mensajes(f"⚠️ {nombre_turno} no encontró objetivo")
            else:
                agregar_y_mostrar_mensajes(f"😐 {nombre_turno} pasó turno")

            dibujar_lista_heroes(turno_actual=nombre_turno)
            for i in range(3):
                pygame.event.pump()
                pygame.time.delay(int(turno_delay_ms/3))

            if not turnos.cabeza or len(turnos.mostrar_turnos()) <= 1:
                break

        if not turnos.cabeza or len(turnos.mostrar_turnos()) <= 1:
            break

    agregar_y_mostrar_mensajes("🏁 Fin de la batalla")
    actual = lista.cabeza
    ganador = None
    mayor_vida = -1
    while actual:
        if actual.vida > mayor_vida:
            mayor_vida = actual.vida
            ganador = actual.nombre
        actual = actual.siguiente

    if ganador:
        agregar_y_mostrar_mensajes(f"🏆 {ganador} es el héroe con mayor PV ({mayor_vida})")
    else:
        agregar_y_mostrar_mensajes("💀 No quedó ningún héroe vivo")

    for i in range(6):
        dibujar_lista_heroes()
        pygame.event.pump()
        pygame.time.delay(400)
    
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

        if boton_batalla.esta_clickeado(evento):
            simular_batalla(rondas=5, turno_delay_ms=700)

        if boton_salir.esta_clickeado(evento):
            ejecutando = False

pygame.quit()