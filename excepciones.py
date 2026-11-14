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


# Función de apoyo: convierte un dato a número usando encadenamiento.
def convertir_a_numero(valor, campo):
    """Convierte valor a float o lanza DatoInvalidoError encadenada."""
    try:
        numero = float(valor)
    except (TypeError, ValueError) as error:
        # "from error" guarda el error original de Python como la causa.
        raise DatoInvalidoError(
            f"El campo '{campo}' debe ser numérico; se recibió {valor!r}"
        ) from error
    else:
        # Solo llega aquí si la conversión funcionó.
        return numero


# Prueba rápida: solo se ejecuta si corremos este archivo directamente.
if __name__ == "__main__":
    try:
        raise DatoInvalidoError("El correo 'luisgmail.com' no tiene @")
    except SoftwareFJError as error:
        print("Se atrapó el error:", type(error).__name__, "-", error)
    print("El programa sigue funcionando.")

    print("Conversión correcta:", convertir_a_numero("3.5", "duración"))

    try:
        convertir_a_numero("dos horas", "duración")
    except DatoInvalidoError as error:
        print("Error:", error)
        print("Causa original:", type(error.__cause__).__name__,
              "-", error.__cause__)
