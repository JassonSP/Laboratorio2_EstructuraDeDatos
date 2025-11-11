class NodoHeroe:
    def __init__(self, nombre, nivel, vida, ataque, tipo):
        self.nombre = nombre
        self.nivel = nivel
        self.vida = vida
        self.ataque = ataque
        self.exp = 0
        self.max_vida = vida
        self.tipo = tipo
        self.siguiente = None

    def experiencia(self, cantidad):
        self.exp += cantidad
        if self.exp >= self.nivel * 100:
            self.exp -= self.nivel * 100
            self.nivel += 1
            self.max_vida += 10
            self.vida = min(self.vida + 10, self.max_vida)
            self.ataque += 5
            return True
        return False

class ListaHeroes:
    def __init__(self):
        self.cabeza = None

    def agregar_heroe(self, nombre, nivel, vida, ataque, tipo):
        nuevo = NodoHeroe(nombre, nivel, vida, ataque, tipo)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def buscar_heroe(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None

    def eliminar_heroe(self, nombre):
        actual = self.cabeza
        anterior = None
        while actual:
            if actual.nombre == nombre:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def mejorar_heroe(self, nombre, incremento_vida, incremento_ataque):
        heroe = self.buscar_heroe(nombre)
        if heroe:
            heroe.vida += incremento_vida
            heroe.ataque += incremento_ataque

    def mostrar_lista(self):
        if self.cabeza is None:
            return
        actual = self.cabeza
        while actual:
            actual = actual.siguiente
        print()