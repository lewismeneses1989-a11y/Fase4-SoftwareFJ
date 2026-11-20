"""
main.py
Parte 5 - Simulación Integral del Sistema de Gestión de Clientes, Servicios y Reservas.
Curso: Programación (213023) - UNAD.
Autora: Valentina Jaramillo

Este módulo ejecuta la simulación completa de 10 operaciones (válidas e inválidas)
sobre el sistema de Software FJ sin uso de bases de datos, demostrando:
  - Gestión de entidades en memoria mediante listas internas.
  - Manejo robusto de excepciones (try/except, try/except/else, try/except/finally).
  - Registro persistente de eventos y errores en el archivo de logs.
  - Continuidad y estabilidad de la aplicación ante fallos controlados.
"""

from excepciones import (
    SoftwareFJError,
    DatoInvalidoError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from registro_logs import registrar
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reservas import Reserva
from cliente import Cliente


def ejecutar_simulacion():
    """Simula 10 operaciones completas demostrando estabilidad y control de errores."""
    print("=" * 78)
    print(" SOFTWARE FJ - SIMULACIÓN INTEGRAL DE CLIENTES, SERVICIOS Y RESERVAS ".center(78, "="))
    print("=" * 78)
    registrar("INFO", "=== INICIO DE SIMULACIÓN DEL SISTEMA SOFTWARE FJ (10 OPERACIONES) ===")

    # Listas internas en memoria (sin uso de bases de datos)
    clientes = []
    servicios = []
    reservas = []

    # --------------------------------------------------------------------------
    # OPERACIÓN 1: Registro válido de cliente
    # --------------------------------------------------------------------------
    print("\n[Operación 1] Registrando cliente válido...")
    try:
        cliente_1 = Cliente("CLI-001", "Laura Martínez", "laura.martinez@correo.com")
    except SoftwareFJError as error:
        registrar("ERROR", f"Op 1 fallida: {error}")
        print(f"  -> Error inesperado: {error}")
    else:
        clientes.append(cliente_1)
        registrar("INFO", f"Op 1 exitosa: {cliente_1}")
        print(f"  -> Éxito: {cliente_1}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 2: Registro inválido de cliente (correo sin formato válido)
    # --------------------------------------------------------------------------
    print("\n[Operación 2] Intentando registrar cliente con correo inválido...")
    try:
        cliente_invalido = Cliente("CLI-002", "Pedro Ramírez", "pedro-sin-arroba")
        clientes.append(cliente_invalido)
    except SoftwareFJError as error:
        registrar("ERROR", f"Op 2 controlada (Cliente inválido): {error}")
        print(f"  -> Excepción capturada [{type(error).__name__}]: {error}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 3: Registro de segundo cliente válido
    # --------------------------------------------------------------------------
    print("\n[Operación 3] Registrando segundo cliente válido...")
    try:
        cliente_2 = Cliente("CLI-003", "Carlos Rodríguez", "carlos.rodriguez@correo.com")
    except SoftwareFJError as error:
        registrar("ERROR", f"Op 3 fallida: {error}")
    else:
        clientes.append(cliente_2)
        registrar("INFO", f"Op 3 exitosa: {cliente_2}")
        print(f"  -> Éxito: {cliente_2}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 4: Creación válida de los 3 tipos de servicios especializados
    # --------------------------------------------------------------------------
    print("\n[Operación 4] Creando catálogo de servicios especializados...")
    try:
        sala = ReservaSala("Sala Ejecutiva Norte", tarifa_hora=50000, capacidad=12)
        equipo = AlquilerEquipo("Portátil Dell Latitude", tarifa_hora=8000, cantidad=3)
        asesoria = Asesoria("Arquitectura Cloud", tarifa_hora=120000, especialista="Ing. Sofía Vega")
        asesoria_ocupada = Asesoria(
            "Auditoría de Seguridad", tarifa_hora=150000, especialista="Dr. Andrés Silva", disponible=False
        )
    except SoftwareFJError as error:
        registrar("ERROR", f"Op 4 fallida: {error}")
    else:
        servicios.extend([sala, equipo, asesoria, asesoria_ocupada])
        registrar("INFO", "Op 4 exitosa: 4 servicios registrados en memoria.")
        for srv in servicios:
            print(f"  -> Servicio creado: {srv.describir()}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 5: Creación incorrecta de servicio (tarifa negativa)
    # --------------------------------------------------------------------------
    print("\n[Operación 5] Intentando crear servicio con tarifa negativa...")
    try:
        servicio_erroneo = ReservaSala("Sala Inválida", tarifa_hora=-30000, capacidad=5)
        servicios.append(servicio_erroneo)
    except SoftwareFJError as error:
        registrar("ERROR", f"Op 5 controlada (Servicio inválido): {error}")
        print(f"  -> Excepción capturada [{type(error).__name__}]: {error}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 6: Reserva exitosa completa (Creación -> Confirmación -> Procesamiento)
    # --------------------------------------------------------------------------
    print("\n[Operación 6] Creando, confirmando y procesando reserva exitosa (Sala)...")
    try:
        reserva_1 = Reserva("RES-001", clientes[0], servicios[0], duracion=4)
        reserva_1.confirmar()
        total_r1 = reserva_1.procesar(descuento=10, impuesto=19)
    except SoftwareFJError as error:
        registrar("ERROR", f"Op 6 fallida: {error}")
        print(f"  -> Error: {error}")
    else:
        reservas.append(reserva_1)
        print(f"  -> Éxito: {reserva_1}")
        print(f"  -> Total facturado (10% desc + 19% IVA): ${total_r1:,.2f}")
    finally:
        print("  -> Auditoría Op 6: Bloque de liquidación finalizado correctamente.")

    # --------------------------------------------------------------------------
    # OPERACIÓN 7: Intento de reserva fallida por duración inválida (0 horas)
    # --------------------------------------------------------------------------
    print("\n[Operación 7] Intentando crear reserva con duración igual a 0...")
    try:
        reserva_invalida = Reserva("RES-002", clientes[1], servicios[1], duracion=0)
        reservas.append(reserva_invalida)
    except SoftwareFJError as error:
        registrar("ERROR", f"Op 7 controlada (Duración inválida): {error}")
        print(f"  -> Excepción capturada [{type(error).__name__}]: {error}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 8: Cancelación válida de reserva y reintento inválido de cancelación
    # --------------------------------------------------------------------------
    print("\n[Operación 8] Creando reserva, cancelándola y probando doble cancelación...")
    try:
        reserva_2 = Reserva("RES-003", clientes[1], servicios[1], duracion=5)
        reservas.append(reserva_2)
        reserva_2.cancelar(motivo="Cambio de agenda del cliente")
        print(f"  -> Cancelación inicial exitosa: {reserva_2}")
        # Intentamos cancelar por segunda vez para provocar OperacionNoPermitidaError
        reserva_2.cancelar(motivo="Segundo intento")
    except OperacionNoPermitidaError as error:
        registrar("ERROR", f"Op 8 controlada (Doble cancelación): {error}")
        print(f"  -> Excepción capturada [{type(error).__name__}]: {error}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 9: Intento fallido de procesar una reserva sin confirmar (PENDIENTE)
    # --------------------------------------------------------------------------
    print("\n[Operación 9] Intentando procesar una reserva en estado PENDIENTE...")
    try:
        reserva_3 = Reserva("RES-004", clientes[0], servicios[2], duracion=2)
        reservas.append(reserva_3)
        reserva_3.procesar()
    except ReservaInvalidaError as error:
        registrar("ERROR", f"Op 9 controlada (Procesamiento sin confirmar): {error}")
        print(f"  -> Excepción capturada [{type(error).__name__}]: {error}")
        if error.__cause__:
            print(f"  -> Causa encadenada [{type(error.__cause__).__name__}]: {error.__cause__}")

    # --------------------------------------------------------------------------
    # OPERACIÓN 10: Intento fallido de procesar reserva con servicio no disponible
    # --------------------------------------------------------------------------
    print("\n[Operación 10] Intentando procesar reserva de servicio NO disponible...")
    try:
        reserva_4 = Reserva("RES-005", clientes[1], servicios[3], duracion=2)
        reservas.append(reserva_4)
        reserva_4.confirmar()
        reserva_4.procesar()
    except ReservaInvalidaError as error:
        registrar("ERROR", f"Op 10 controlada (Servicio no disponible): {error}")
        print(f"  -> Excepción capturada [{type(error).__name__}]: {error}")
        if error.__cause__:
            print(f"  -> Causa encadenada [{type(error.__cause__).__name__}]: {error.__cause__}")
    finally:
        print("  -> Auditoría Op 10: Verificación de disponibilidad finalizada.")

    # --------------------------------------------------------------------------
    # RESUMEN FINAL EN MEMORIA
    # --------------------------------------------------------------------------
    print("\n" + "=" * 78)
    print(
        f" SIMULACIÓN COMPLETADA | Clientes: {len(clientes)} | "
        f"Servicios: {len(servicios)} | Reservas: {len(reservas)} ".center(78)
    )
    print(" El sistema se mantuvo estable y todos los eventos quedaron en logs. ".center(78))
    print("=" * 78)
    registrar("INFO", "=== FIN DE SIMULACIÓN: EJECUCIÓN COMPLETA SIN INTERRUPCIONES ===")


if __name__ == "__main__":
    ejecutar_simulacion()