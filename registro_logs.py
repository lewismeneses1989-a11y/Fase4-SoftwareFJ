"""
registro_logs.py
Parte 1 - Registro de eventos y errores en un archivo de logs.
Autor: Luis Alfredo Adrada Meneses
"""
from datetime import datetime

from excepciones import SoftwareFJError, ServicioNoDisponibleError

# Nombre del archivo donde se guardan los eventos y errores.
RUTA_LOG = "software_fj.log"


def registrar(nivel, mensaje):
    """Escribe una línea en el log con el formato: fecha | nivel | mensaje."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{fecha} | {nivel} | {mensaje}\n"
    archivo = None
    try:
        # "a" (append) agrega al final sin borrar lo que ya existe.
        archivo = open(RUTA_LOG, "a", encoding="utf-8")
        archivo.write(linea)
    except OSError as error:
        # Si el log falla, avisamos en pantalla, pero el programa sigue.
        print(f"[AVISO] No se pudo escribir en el log: {error}")
    else:
        # Solo se ejecuta si el try terminó sin errores.
        print(f"[{nivel}] {mensaje}")
    finally:
        # Se ejecuta SIEMPRE: haya error o no, cerramos el archivo.
        if archivo is not None:
            archivo.close()


if __name__ == "__main__":
    registrar("INFO", "Iniciando sistema de logs Software FJ...")

    try:
        raise ServicioNoDisponibleError(
            "La sala 3 está en mantenimiento preventivo"
            )
    except SoftwareFJError as error:
        registrar("ERROR", f"{type(error).__name__}: {error}")

    registrar("INFO", "El programa continúa su ejecución normalmente.")
