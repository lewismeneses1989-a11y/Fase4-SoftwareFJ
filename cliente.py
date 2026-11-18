"""
cliente.py
Parte 2 - Clase Cliente del sistema Software FJ.
Autor: Luisa Fernanda Triana Cabezas
Cliente hereda de EntidadSistema y protege sus datos personales con
atributos privados y propiedades que validan cada valor antes de guardarlo.
Se crea así: Cliente("CLI-001", "Laura Martínez", "laura.martinez@correo.com")
"""
import re

from entidad_base import EntidadSistema
from excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    SoftwareFJError,
)
from registro_logs import registrar

# Patrón sencillo para correos: texto@texto.dominio
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(EntidadSistema):
    """Persona o empresa que solicita servicios a Software FJ."""

    def __init__(self, id_cliente, nombre, correo):
        super().__init__()  # Genera el ID interno y la fecha de creación.
        try:
            # Al asignar se ejecutan los setters, que validan cada dato.
            self.id_cliente = id_cliente
            self.nombre = nombre
            self.correo = correo
        except SoftwareFJError as error:
            # Registramos el fallo y lo encadenamos para no perder la causa.
            registrar("ERROR", f"No se pudo crear el cliente: {error}")
            raise DatoInvalidoError(
                f"Cliente rechazado ({type(error).__name__}): {error}"
            ) from error
        else:
            registrar("INFO", f"Cliente creado: {self.describir()}")

    # ---------- Validación auxiliar (privada) ----------
    @staticmethod
    def _texto_obligatorio(valor, campo):
        """Verifica que el valor exista y no sea un texto vacío."""
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError(f"El campo '{campo}' es obligatorio")
        return str(valor).strip()

    # ---------- Propiedades con validación (encapsulación) ----------
    @property
    def id_cliente(self):
        return self.__id_cliente

    @id_cliente.setter
    def id_cliente(self, valor):
        self.__id_cliente = self._texto_obligatorio(valor, "id_cliente").upper()

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self._texto_obligatorio(valor, "nombre")
        if len(valor) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 letras")
        if not all(c.isalpha() or c.isspace() for c in valor):
            raise DatoInvalidoError(f"El nombre '{valor}' solo admite letras")
        self.__nombre = valor.title()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        valor = self._texto_obligatorio(valor, "correo")
        if not PATRON_CORREO.match(valor):
            raise DatoInvalidoError(f"El correo '{valor}' no es válido")
        self.__correo = valor.lower()

    # ---------- Implementación de los métodos abstractos ----------
    def describir(self):
        return (f"{self.__id_cliente} | {self.__nombre} | "
                f"Correo: {self.__correo}")

    def validar(self):
        # Vuelve a pasar cada dato por su setter; si algo cambió mal, falla.
        self.id_cliente = self.__id_cliente
        self.nombre = self.__nombre
        self.correo = self.__correo
        return True


# Prueba rápida: un cliente válido y varios inválidos.
if __name__ == "__main__":
    clientes = []
    datos_prueba = [
        ("CLI-001", "Laura Martínez", "laura.martinez@correo.com"),
        ("CLI-002", "Ana", "anagmail.com"),            # correo sin @
        ("CLI-003", "", "pedro@unad.edu.co"),          # sin nombre
        ("CLI-004", "María López 2", "maria@unad.edu.co"),  # nombre con número
    ]

    for datos in datos_prueba:
        try:
            clientes.append(Cliente(*datos))
        except SoftwareFJError as error:
            print(f"   -> Causa original: {type(error.__cause__).__name__}")

    print("\nClientes registrados correctamente:")
    for c in clientes:
        print("  ", c)  # Usa __str__ heredado de EntidadSistema.

    # Intentar modificar un dato con un valor inválido también se controla.
    try:
        clientes[0].correo = "correo-malo"
    except DatoInvalidoError as error:
        registrar("ERROR", f"Modificación rechazada: {error}")

    print("\nEl programa sigue funcionando.")

