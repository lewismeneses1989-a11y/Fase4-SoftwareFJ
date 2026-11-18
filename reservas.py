"""
reservas.py
Fase 4 - Sistema Integral de Gestión de Clientes, Servicios y Reservas.
Curso: Programación (213023) - UNAD.
Autor: Sebastian (Módulo de Reservas: creación, confirmación, cancelación y procesamiento)

Este módulo implementa la clase Reserva aplicando los principios de la POO:
  - Abstracción y Encapsulamiento: atributos protegidos expuestos mediante @property
    y setters con validaciones estrictas.
  - Relación de Agregación: integra instancias de Cliente y Servicio.
  - Sobrecarga de Métodos: cálculo de costos con parámetros opcionales (descuentos e impuestos).
  - Manejo Avanzado de Excepciones: uso de bloques try/except, try/except/else,
    try/except/finally y encadenamiento de excepciones (raise ... from error).
  - Persistencia de eventos: registro de operaciones y fallos en archivo de logs.
"""

from excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    CalculoInconsistenteError,
    ServicioNoDisponibleError,
    convertir_a_numero
)

from registro_logs import registrar


class Reserva:
    """
    Representa una reserva de servicio realizada por un cliente en Software FJ.
    Ciclo de vida: PENDIENTE -> CONFIRMADA -> PROCESADA (o CANCELADA).

        @property: solo lectura
        @"nombre-funcion".setter: se puede sobreecribir
    """

    # Constante de clase: tupla con los únicos 4 estados permitidos en el sistema
    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    # ──────────────────────────────────────────────────────────────────────────
    # CONSTRUCTOR (__init__)
    # ──────────────────────────────────────────────────────────────────────────
    def __init__(self, id_reserva, cliente, servicio, duracion):
        """
        Inicializa una nueva reserva.
        Nota: Se asignan los atributos SIN guion bajo (self.id_reserva, self.cliente...)
        para obligar a que pasen por sus respectivos @setters y ejecuten las validaciones.
        """

        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion

        # Estado inicial fijo: Toda reserva nace en PENDIENTE.
        self._estado = "PENDIENTE"

        # Registro de creación de la reserva en el archivo de logs.
        registrar("INFO", 
                  f"Reserva #{self._id_reserva} creada en estado PENDIENTE.")

    # ──────────────────────────────────────────────────────────────────────────
    # ENCAPSULAMIENTO: PROPIEDADES Y SETTERS (GETTERS Y SETTERS)
    # ──────────────────────────────────────────────────────────────────────────
    # --- Atributo: id_reserva ---
    @property
    def id_reserva(self): 
        return self._id_reserva

    @id_reserva.setter
    def id_reserva(self, valor):
        if not valor:
            raise ParametroFaltanteError("El ID de la reserva es obligatorio y no puede estar vacío.")
        self._id_reserva = str(valor)

    # --- Atributo: cliente ---
    @property
    def cliente(self):
        """Getter: Devuelve el objeto cliente asociado a la reserva."""
        return self._cliente

    @cliente.setter
    def cliente(self, valor):
        """Setter: Valida que la reserva tenga un cliente asignado obligatoriamente."""
        if valor is None:
            raise ParametroFaltanteError("La reserva debe tener un cliente asignado.")
        
        self._cliente = valor

    # --- Atributo: servicio ---
    @property
    def servicio(self):
        """Getter: Devuelve el objeto servicio asociado (Sala, Equipo o Asesoría)."""
        return self._servicio

    @servicio.setter
    def servicio(self, valor):
        """Setter: Valida que la reserva tenga un servicio asignado obligatoriamente."""
        if valor is None:
            raise ParametroFaltanteError("La reserva debe tener un servicio asignado.")

        self._servicio = valor

    # --- Atributo: duracion ---
    @property
    def duracion(self):
        """Getter: Devuelve las horas de duración de la reserva."""
        return self._duracion

    @duracion.setter
    def duracion(self, valor):
        duracion_float = convertir_a_numero(valor, "duracion")

        if duracion_float <= 0:
            raise DatoInvalidoError(f"La duración de la reserva debe ser mayor a 0, Se recibió: {duracion_float}")
        
        self._duracion = duracion_float

    # --- Atributo: estado ---
    @property
    def estado(self):
        """
        Getter: Devuelve el estado actual de la reserva.
        Nota: NO tiene setter público para evitar que alguien modifique el estado.
        El estado solo se puede cambiar mediante confirmar(), cancelar() o procesar().
        """
        return self._estado

    # ──────────────────────────────────────────────────────────────────────────
    # MÉTODOS AUXILIARES INTERNOS
    # ──────────────────────────────────────────────────────────────────────────
    def nombre_cliente(self):
        """Obtiene el nombre del cliente de forma segura mediante getattr (escudo contra errores)."""
        return getattr(self._cliente, "nombre", str(self._cliente))

    def nombre_servicio(self):
        return getattr(self._servicio, "nombre", str(self._servicio))

    
    # ──────────────────────────────────────────────────────────────────────────
    # MÉTODOS DE OPERACIÓN (MÁQUINA DE ESTADOS Y NEGOCIO)
    # ──────────────────────────────────────────────────────────────────────────
    def confirmar(self):
        """
        Transición: PENDIENTE -> CONFIRMADA.
        Valida que la reserva se encuentre en PENDIENTE.
        Demuestra la estructura: try / except / else.
        """
        try:
            # Solo una reserva PENDIENTE puede ser confirmada
            if self._estado != "PENDIENTE":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar la reserva #{self._id_reserva}. "
                    f"Estado actual: {self._estado}. "
                    f"Solo se pueden confirmar reservas en estado PENDIENTE."
                )

            # Si pasa la validación, cambiamos el estado interno
            self._estado = "CONFIRMADA"

        except OperacionNoPermitidaError as error:
            registrar("ERROR", f"Fallo al confirmar la reserva #{self._id_reserva}: {error}")
            raise

        else:
            registrar("INFO", f"Reserva #{self._id_reserva} CONFIRMADA exitosamente.")

    def cancelar(self, motivo="No especificado"):
        """
        Transición: PENDIENTE o CONFIRMADA -> CANCELADA.
        Valida que la reserva no haya sido procesada ni esté previamente cancelada.
        Demuestra la estructura: try / except / else.
        """
        try:
            if self._estado == "PROCESADA":
                raise OperacionNoPermitidaError(
                    f"La reserva #{self.id_reserva} No puede ser cancelada porque ya fue procesada")

            if self._estado == "CANCELADA":
                raise OperacionNoPermitidaError(
                    f"La reserva #{self.id_reserva}: Ya se encuentra cancelada")

            # Transición válida a estado final CANCELADA
            self._estado = "CANCELADA"

        except OperacionNoPermitidaError as error:
            registrar("ERROR", f"Fallo al cancelar reserva #{self._id_reserva}: {error}")
            raise

        else:
            registrar("INFO", f"Reserva #{self._id_reserva} cancelada. Motivo: {motivo}")

    def procesar(self, descuento=0.0, impuesto=0.19):
        """
        Transición: CONFIRMADA -> PROCESADA.
        Calcula el costo total y finaliza la reserva.
        Acepta tanto porcentajes enteros (ej: 19 o 10) como factores decimales (ej: 0.19 o 0.10).
        """
        total = None
        try:
            # Solo reservas CONFIRMADAS pueden ser procesadas
            if self._estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    f"Solo se pueden procesar reservas CONFIRMADAS. Estado actual: {self._estado}."
                )

            # Calcula el total invocando el método sobrecargado de cálculo de costos
            total = self.calcular_costo_total(descuento=descuento, impuesto=impuesto)

            # Transición válida a estado final PROCESADA
            self._estado = "PROCESADA"

        except OperacionNoPermitidaError as error:
            registrar("ERROR", f"Error de operación al procesar reserva #{self._id_reserva}: {error}")
            # ENCADENAMIENTO DE EXCEPCIONES: 'from error' preserva la causa original
            raise ReservaInvalidaError(
                f"No fue posible procesar la reserva #{self._id_reserva}."
            ) from error

        except ServicioNoDisponibleError as error:
            registrar("ERROR", f"Servicio no disponible al procesar reserva #{self._id_reserva}: {error}")
            # ENCADENAMIENTO DE EXCEPCIONES: la falta de disponibilidad invalida el procesamiento
            raise ReservaInvalidaError(
                f"No fue posible procesar la reserva #{self._id_reserva}: el servicio no está disponible."
            ) from error

        except (DatoInvalidoError, CalculoInconsistenteError) as error:
            registrar("ERROR", f"Error de cálculo en reserva #{self._id_reserva}: {error}")
            raise

        else:
            # Solo se ejecuta si la reserva se procesó correctamente
            registrar("INFO", f"Reserva #{self._id_reserva} PROCESADA con éxito. Total: ${total:,.2f}")

        finally:
            # Se ejecuta SIEMPRE (haya ocurrido error o no): limpia recursos o cierra procesos
            registrar("INFO", f"Fin del procesamiento de reserva #{self._id_reserva}. Estado: {self._estado}.")

        return total

    def calcular_costo_total(self, descuento=0.0, impuesto=0.19):
        """
        Demuestra SOBRECARGA DE MÉTODOS en Python mediante parámetros con valores por defecto:
            - descuento: por defecto 0.0 (acepta porcentaje como 10 o decimal como 0.10)
            - impuesto: por defecto 0.19 (acepta porcentaje como 19 o decimal como 0.19)
        Aplica POLIMORFISMO al invocar 'self._servicio.calcular_costo(self._duracion)'.
        Normaliza automáticamente los valores para permitir ambas notaciones.
        """
        descuento = convertir_a_numero(descuento, "descuento")
        impuesto = convertir_a_numero(impuesto, "impuesto")

        # Normalización: Si el usuario ingresa valores enteros porcentuales (ej: 19 o 10), se convierten a factor decimal
        if descuento > 1.0:
            descuento = descuento / 100.0

        if impuesto > 1.0:
            impuesto = impuesto / 100.0

        if not (0.0 <= descuento <= 1.0):
            raise DatoInvalidoError(
                f"El descuento debe estar entre 0% y 100% (o 0.0 y 1.0). Se recibió: {descuento}"
            )

        if impuesto < 0:
            raise DatoInvalidoError(f"El impuesto no puede ser negativo. Se recibió: {impuesto}")

        # POLIMORFISMO: Le pide al objeto servicio que calcule su tarifa base según las horas.
        costo_base = self._servicio.calcular_costo(self._duracion)

        # Fórmula de liquidación: aplica primero el descuento y luego el impuesto
        subtotal = costo_base * (1.0 - descuento)
        total = subtotal * (1.0 + impuesto)

        if total < 0:
            raise CalculoInconsistenteError(f"Cálculo inconsistente con resultado negativo: ${total:,.2f}")

        # Devuelve el total redondeado a 2 decimales
        return round(total, 2)

    # ──────────────────────────────────────────────────────────────────────────
    # REPRESENTACIÓN EN TEXTO (__str__)
    # ──────────────────────────────────────────────────────────────────────────
    def __str__(self):
        """
        Devuelve una cadena legible con el resumen de la reserva.
        Llama automáticamente a la representación de Cliente y Servicio.
        """
        nombre_cliente = self.nombre_cliente()
        nombre_servicio = self.nombre_servicio()

        return (
            f"Reserva [ID: {self._id_reserva} | "
            f"Cliente: {nombre_cliente} | "
            f"Servicio: {nombre_servicio} | "
            f"Duración: {self._duracion}h | "
            f"Estado: {self._estado}]"
        )


# ──────────────────────────────────────────────────────────────────────────
# BLOQUE DE PRUEBAS DEL MÓDULO (Demostración de ciclo de vida e integración)
# ──────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 75)
    print(" PRUEBAS DEL MÓDULO DE RESERVAS - SOFTWARE FJ ".center(75, "="))
    print("=" * 75)

    # 1. Integración con el módulo de servicios (desarrollado por Luis Adrada)
    from servicios import ReservaSala, AlquilerEquipo, Asesoria

    # Clase auxiliar para representar a un Cliente en las pruebas unitarias
    # (Permite probar Reservas de forma autónoma e independiente)
    class cliente_provicional:
        """Representación simulada de cliente para pruebas unitarias de reservas."""
        def __init__(self, id_cliente, nombre, correo):
            self.id_cliente = id_cliente
            self.nombre = nombre
            self.correo = correo

        def __str__(self):
            return f"{self.nombre} (ID: {self.id_cliente})"

    cliente_demo = cliente_provicional("CLI-101", "Sebastian Gomez", "sebas@example.com")

    # Instanciamos los 3 tipos de servicios especializados
    sala = ReservaSala("Sala de Conferencias", 50000, 15)
    equipo = AlquilerEquipo("Portatil Dell", 8000, 3)
    asesoria = Asesoria("Ciberseguridad", 120000, "Ing. Carlos Mendoza")
    asesoria_agotada = Asesoria("Auditoria Forense", 150000, "Dra. Gomez", disponible=False)

    print("\n--- CASO 1: Creacion, Confirmacion y Procesamiento Exitoso (ReservaSala) ---")
    reserva1 = Reserva("RES-001", cliente_demo, sala, duracion=4)
    print("Estado inicial :", reserva1)
    reserva1.confirmar()
    print("Tras confirmar :", reserva1)
    total1 = reserva1.procesar()  # Usa valores por defecto (0% descuento, 19% impuesto)
    print(f"Total liquidado: ${total1:,.2f}")
    print("Tras procesar  :", reserva1)

    print("\n--- CASO 2: Sobrecarga y Polimorfismo con Descuento e Impuesto (AlquilerEquipo) ---")
    reserva2 = Reserva("RES-002", cliente_demo, equipo, duracion=5)
    reserva2.confirmar()
    # Demuestra normalización: acepta enteros (10, 19) o decimales (0.10, 0.19)
    total2 = reserva2.procesar(descuento=10, impuesto=19)
    print("Reserva equipo :", reserva2)
    print(f"Total liquidado (10% desc, 19% IVA): ${total2:,.2f}")

    print("\n--- CASO 3: Cancelacion de una Reserva (Asesoria) ---")
    reserva3 = Reserva("RES-003", cliente_demo, asesoria, duracion=2)
    print("Antes de cancelar:", reserva3)
    reserva3.cancelar(motivo="Reagendamiento de cronograma")
    print("Tras cancelar    :", reserva3)

    print("\n--- CASO 4: Manejo de Excepcion - Intento de procesar sin confirmar ---")
    reserva4 = Reserva("RES-004", cliente_demo, sala, duracion=2)
    try:
        reserva4.procesar()
    except ReservaInvalidaError as error:
        print(f"Capturado correctamente: {type(error).__name__} -> {error}")
        print(f"Causa original encadenada: {type(error.__cause__).__name__} -> {error.__cause__}")

    print("\n--- CASO 5: Manejo de Excepcion - Servicio no disponible ---")
    reserva5 = Reserva("RES-005", cliente_demo, asesoria_agotada, duracion=2)
    reserva5.confirmar()
    try:
        reserva5.procesar()
    except ReservaInvalidaError as error:
        print(f"Capturado correctamente: {type(error).__name__} -> {error}")
        print(f"Causa original encadenada: {type(error.__cause__).__name__} -> {error.__cause__}")

    print("\n--- CASO 6: Validacion de Parametros (Duracion invalida) ---")
    try:
        Reserva("RES-006", cliente_demo, sala, duracion=-3)
    except DatoInvalidoError as error:
        print(f"Capturado correctamente: {type(error).__name__} -> {error}")

    print("\n" + "=" * 75)
    print(" TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE ".center(75, "="))
    print("=" * 75)