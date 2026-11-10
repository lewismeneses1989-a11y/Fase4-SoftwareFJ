"""
excepciones.py
Parte 1 - Excepciones personalizadas del sistema Software FJ.
Autor: Luis Alfredo Adrada Meneses
"""


# Clase base: la "mamá" de todas las excepciones del sistema.
# Hereda de Exception, como recomienda el tutorial de Python (apartado 8.6).
class SoftwareFJError(Exception):
    """Error general del sistema Software FJ."""


# Cada hija representa un tipo de error que menciona el Anexo 3.
class DatoInvalidoError(SoftwareFJError):
    """Un dato no cumple el formato o el rango esperado (ej.: correo sin @)."""


class ParametroFaltanteError(SoftwareFJError):
    """Falta un dato obligatorio para crear un objeto u operar."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Se intenta hacer algo que el estado actual no permite."""


class ReservaInvalidaError(SoftwareFJError):
    """La reserva no se puede crear, confirmar o cancelar."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible."""


class CalculoInconsistenteError(SoftwareFJError):
    """Un cálculo de costos da un resultado imposible (ej.: costo negativo)."""


# Prueba rápida: solo se ejecuta si corremos este archivo directamente.
if __name__ == "__main__":
    try:
        raise DatoInvalidoError("El correo 'luisgmail.com' no tiene @")
    except SoftwareFJError as error:
        print("Se atrapó el error:", type(error).__name__, "-", error)
    print("El programa sigue funcionando.")
