class NodoHeroe:
    def __init__(self, nombre, nivel, vida, ataque):
        self.nombre = nombre
        self.nivel = nivel
        self.vida = vida
        self.ataque = ataque
        self.siguiente = None

class ListaHeroes:
    def __init__(self):
        self.cabeza = None

    def agregar_heroe(self, nombre, nivel, vida, ataque):
        nuevo = NodoHeroe(nombre, nivel, vida, ataque)
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
        if self.cabeza is None:
            return

        if self.cabeza.nombre == nombre:
            self.cabeza = self.cabeza.siguiente
            return

        anterior = self.cabeza
        actual = self.cabeza.siguiente

        while actual:
            if actual.nombre == nombre:
                anterior.siguiente = actual.siguiente
                return
            anterior = actual
            actual = actual.siguiente


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