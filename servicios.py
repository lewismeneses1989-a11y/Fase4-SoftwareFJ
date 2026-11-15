"""
servicios.py
Parte 3 - Clase abstracta Servicio y servicios especializados.
Autor: Luis Alfredo Adrada Meneses
"""
from abc import ABC, abstractmethod

from excepciones import (CalculoInconsistenteError, DatoInvalidoError,
                         ParametroFaltanteError, convertir_a_numero)

IVA = 0.19  # Impuesto que se suma cuando el cliente lo pide


class Servicio(ABC):
    """Molde de todos los servicios: no se puede crear un Servicio suelto."""

    def __init__(self, nombre, tarifa_hora, disponible=True):
        if not nombre:
            raise ParametroFaltanteError("El servicio necesita un nombre")
        self.nombre = nombre
        self.tarifa_hora = convertir_a_numero(tarifa_hora, "tarifa por hora")
        if self.tarifa_hora <= 0:
            raise DatoInvalidoError("La tarifa por hora debe ser mayor a 0")
        self.disponible = disponible

    @abstractmethod
    def describir(self):
        """Cada servicio debe decir qué es."""

    @abstractmethod
    def validar_parametros(self, horas):
        """Cada servicio revisa las horas a su manera."""

    @abstractmethod
    def calcular_costo(self, horas, con_iva=False, descuento=0):
        """Cada servicio calcula su costo a su manera."""

    def aplicar_ajustes(self, subtotal, con_iva=False, descuento=0):
        """Resta el descuento (%), suma el IVA y revisa el total."""
        descuento = convertir_a_numero(descuento, "descuento")
        if not 0 <= descuento <= 100:
            raise DatoInvalidoError("El descuento debe estar entre 0 y 100")
        total = subtotal * (1 - descuento / 100)
        if con_iva:
            total = total * (1 + IVA)
        if total < 0:
            raise CalculoInconsistenteError(
                "El costo total no puede ser negativo")
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio de reserva de salas por horas."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        self.capacidad = int(convertir_a_numero(capacidad, "capacidad"))

    def describir(self):
        return f"Sala '{self.nombre}' para {self.capacidad} personas"

    def validar_parametros(self, horas):
        horas = convertir_a_numero(horas, "horas")
        if not 1 <= horas <= 12:
            raise DatoInvalidoError("Una sala se reserva entre 1 y 12 horas")
        return horas

    def calcular_costo(self, horas, con_iva=False, descuento=0):
        horas = self.validar_parametros(horas)
        subtotal = self.tarifa_hora * horas
        return self.aplicar_ajustes(subtotal, con_iva, descuento)


if __name__ == "__main__":
    try:
        # Intentamos crear un "Servicio" suelto, lo cual debería fallar
        # por ser abstracto
        prueba_servicio = Servicio("Genérico", 1000)
    except TypeError as error:
        print(f"No se puede crear un Servicio suelto: {error}")

    # 1. Se crea una sala de ejemplo para probar los cálculos
    sala = ReservaSala("Sala Andes", 50000, 10)

    # 2. Se imprime la descripción de la sala
    print(sala.describir())

    # 3. Costo con las tres formas de llamar a calcular_costo (sobrecarga)
    print(f"2 horas: {sala.calcular_costo(2)}")
    print(f"2 horas con IVA: {sala.calcular_costo(2, con_iva=True)}")
    costo = sala.calcular_costo(2, con_iva=True, descuento=10)
    print(f"2 horas, IVA y 10 %: {costo}")

    # 4. Se fuerza un error: 20 horas supera el máximo de 12
    try:
        sala.calcular_costo(20)
    except DatoInvalidoError as error:
        print(f"Error: {error}")
