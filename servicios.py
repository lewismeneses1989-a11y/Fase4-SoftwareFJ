"""
servicios.py
Parte 3 - Clase abstracta Servicio y servicios especializados.
Autor: Luis Alfredo Adrada Meneses

Define la clase abstracta Servicio y tres servicios que heredan de ella:
ReservaSala, AlquilerEquipo y Asesoria. Cada uno sobrescribe describir(),
validar_parametros() y calcular_costo() (polimorfismo).
"""
# ABC y abstractmethod permiten crear clases y métodos abstractos.
from abc import ABC, abstractmethod

# Excepciones propias (Parte 1) para cada tipo de error del servicio.
from excepciones import (CalculoInconsistenteError, DatoInvalidoError,
                         ParametroFaltanteError, ServicioNoDisponibleError,
                         convertir_a_numero)

IVA = 0.19  # Impuesto que se suma cuando el cliente lo pide


class Servicio(ABC):
    """Molde de todos los servicios: no se puede crear un Servicio suelto."""

    def __init__(self, nombre, tarifa_hora, disponible=True):
        # Validación 1: el nombre es obligatorio.
        if not nombre:
            raise ParametroFaltanteError(
                "El servicio necesita un nombre")
        self.nombre = nombre
        # Validación 2: la tarifa debe ser un número (encadenamiento).
        self.tarifa_hora = convertir_a_numero(tarifa_hora, "tarifa por hora")
        # Validación 3: la tarifa debe ser positiva.
        if self.tarifa_hora <= 0:
            raise DatoInvalidoError(
                "La tarifa por hora debe ser mayor a 0")
        # Indica si el servicio se puede prestar en este momento.
        self.disponible = disponible

    # Métodos abstractos: cada clase hija está OBLIGADA a escribirlos.
    # Si alguna no lo hace, Python no deja crear objetos de esa clase.
    @abstractmethod
    def describir(self):
        """Cada servicio debe decir qué es."""

    @abstractmethod
    def validar_parametros(self, horas):
        """Cada servicio revisa las horas a su manera."""

    # Sobrecarga simulada: con_iva y descuento tienen valores por
    # defecto, así el método se puede llamar de tres formas distintas:
    # calcular_costo(2), calcular_costo(2, con_iva=True) o
    # calcular_costo(2, con_iva=True, descuento=10).
    @abstractmethod
    def calcular_costo(self, horas, con_iva=False, descuento=0):
        """Cada servicio calcula su costo a su manera."""

    # Método concreto: lo heredan las tres hijas tal cual, sin repetirlo.
    def aplicar_ajustes(self, subtotal, con_iva=False, descuento=0):
        """Resta el descuento (%), suma el IVA y revisa el total."""
        # El descuento debe ser un número entre 0 y 100 (porcentaje).
        descuento = convertir_a_numero(descuento, "descuento")
        if not 0 <= descuento <= 100:
            raise DatoInvalidoError(
                "El descuento debe estar entre 0 y 100")
        # Primero se aplica el descuento: 10 % deja el 90 % del subtotal.
        total = subtotal * (1 - descuento / 100)
        # Luego, si se pidió, se suma el IVA del 19 %.
        if con_iva:
            total = total * (1 + IVA)
        # Control final: un costo negativo es un cálculo imposible.
        if total < 0:
            raise CalculoInconsistenteError(
                "El costo total no puede ser negativo")
        # Se redondea a 2 decimales, como un valor en pesos.
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio de reserva de salas por horas."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        # super() reutiliza las validaciones de nombre y tarifa del padre.
        super().__init__(nombre, tarifa_hora, disponible)
        # Atributo propio de la sala: número de personas que caben.
        self.capacidad = int(convertir_a_numero(capacidad, "capacidad"))

    # Sobrescritura: versión propia de describir() para salas.
    def describir(self):
        return f"Sala '{self.nombre}' para {self.capacidad} personas"

    # Regla propia: una sala se reserva entre 1 y 12 horas.
    def validar_parametros(self, horas):
        horas = convertir_a_numero(horas, "horas")
        if not 1 <= horas <= 12:
            raise DatoInvalidoError(
                "Una sala se reserva entre 1 y 12 horas")
        return horas

    # Costo de la sala: tarifa por hora x horas.
    def calcular_costo(self, horas, con_iva=False, descuento=0):
        horas = self.validar_parametros(horas)
        subtotal = self.tarifa_hora * horas
        return self.aplicar_ajustes(subtotal, con_iva, descuento)


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos por horas."""

    def __init__(self, nombre, tarifa_hora, cantidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        # Atributo propio: cuántas unidades del equipo se alquilan.
        self.cantidad = int(convertir_a_numero(cantidad, "cantidad"))
        if self.cantidad < 1:
            raise DatoInvalidoError(
                "La cantidad de equipos no puede ser menor a 1")

    # Sobrescritura: versión propia de describir() para equipos.
    def describir(self):
        return f"Equipo '{self.nombre}' x {self.cantidad} unidades"

    # Regla propia: el alquiler va de 1 a 72 horas (3 días).
    def validar_parametros(self, horas):
        horas = convertir_a_numero(horas, "horas")
        if not 1 <= horas <= 72:
            raise DatoInvalidoError(
                "El alquiler es de mínimo 1 y máximo 72 horas")
        return horas

    # Costo del equipo: tarifa por hora x horas x cantidad de unidades.
    def calcular_costo(self, horas, con_iva=False, descuento=0):
        horas = self.validar_parametros(horas)
        subtotal = self.tarifa_hora * horas * self.cantidad
        return self.aplicar_ajustes(subtotal, con_iva, descuento)


class Asesoria(Servicio):
    """Servicio de asesoría especializada por horas."""

    def __init__(self, nombre, tarifa_hora, especialista, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        # Atributo propio y obligatorio: quién presta la asesoría.
        if not especialista:
            raise ParametroFaltanteError(
                "La asesoría requiere un especialista")
        self.especialista = especialista

    # Sobrescritura: versión propia de describir() para asesorías.
    def describir(self):
        return f"Asesoría '{self.nombre}' con {self.especialista}"

    # Regla propia: una asesoría dura entre 1 y 8 horas (una jornada).
    def validar_parametros(self, horas):
        horas = convertir_a_numero(horas, "horas")
        if not 1 <= horas <= 8:
            raise DatoInvalidoError(
                "La asesoría debe ser entre 1 y 8 horas")
        return horas

    # Costo de la asesoría: tarifa por hora x horas, si hay especialista.
    def calcular_costo(self, horas, con_iva=False, descuento=0):
        # Primero se revisa la disponibilidad: sin especialista no se cobra.
        if not self.disponible:
            raise ServicioNoDisponibleError(
                "El especialista no está disponible")
        horas = self.validar_parametros(horas)
        subtotal = self.tarifa_hora * horas
        return self.aplicar_ajustes(subtotal, con_iva, descuento)


# Pruebas: solo se ejecutan al correr este archivo directamente.
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

    # 5. Alquiler de equipos: tarifa x horas x cantidad
    equipo = AlquilerEquipo("Portátil", 5000, 3)
    print(equipo.describir())
    print(f"Costo 10 horas: {equipo.calcular_costo(10)}")

    # 6. Asesoría especializada
    asesoria = Asesoria("Ciberseguridad", 150000, "Ana Pérez")
    print(asesoria.describir())
    print(f"Costo 4 horas: {asesoria.calcular_costo(4)}")

    # 7. Se fuerza un error: el especialista no está disponible
    try:
        no_disponible = Asesoria("Redes", 70000, "Juan", disponible=False)
        no_disponible.calcular_costo(1)
    except ServicioNoDisponibleError as error:
        print(f"Error: {error}")
    