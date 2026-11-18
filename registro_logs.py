"""
registro_logs.py
Parte 1 - Registro de eventos y errores en un archivo de logs.
Autor: Luis Alfredo Adrada Meneses

Todas las partes del sistema llaman a registrar() para dejar constancia
de cada evento (INFO) y de cada error controlado (ERROR).
"""
# datetime permite obtener la fecha y hora actual de cada registro.
from datetime import datetime

# Se importan las excepciones propias solo para la prueba del final.
from excepciones import SoftwareFJError, ServicioNoDisponibleError

# Nombre del archivo donde se guardan los eventos y errores.
# Se crea solo la primera vez que se registra algo.
RUTA_LOG = "software_fj.log"


def registrar(nivel, mensaje):
    """Escribe una línea en el log con el formato: fecha | nivel | mensaje."""
    # Fecha y hora con formato año-mes-día hora:minuto:segundo.
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Línea completa del log; "\n" hace el salto a la siguiente línea.
    linea = f"{fecha} | {nivel} | {mensaje}\n"
    # Se inicia en None para saber en el finally si se alcanzó a abrir.
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


# Prueba rápida: solo se ejecuta al correr este archivo directamente.
if __name__ == "__main__":
    # Prueba 1: registrar un evento normal.
    registrar("INFO", "Iniciando sistema de logs Software FJ...")

    # Prueba 2: provocar un error propio y registrarlo como ERROR.
    try:
        raise ServicioNoDisponibleError(
            "La sala 3 está en mantenimiento preventivo"
        )
    except SoftwareFJError as error:
        registrar("ERROR", f"{type(error).__name__}: {error}")

    # Prueba 3: el programa continúa después del error controlado.
    registrar("INFO", "El programa continúa su ejecución normalmente.")
