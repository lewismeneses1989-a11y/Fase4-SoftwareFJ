"""
entidad_base.py
Parte 2 - Clase abstracta general del sistema Software FJ.
Autor: Luisa Fernanda Triana Cabezas

Todas las entidades del sistema (clientes, servicios y reservas) heredan
de EntidadSistema. Así comparten un identificador, una fecha de creación
y la obligación de saber describirse y validarse a sí mismas.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class EntidadSistema(ABC):
    """Clase abstracta: no se puede crear un objeto directamente de ella."""

    # Contador compartido por todas las entidades para generar IDs únicos.
    _contador_ids = 0

    def __init__(self):
        EntidadSistema._contador_ids += 1
        # Atributos "protegidos" (con _): solo se leen con propiedades.
        self._id = EntidadSistema._contador_ids
        self._fecha_creacion = datetime.now()

    # ---------- Propiedades de solo lectura (encapsulación) ----------
    @property
    def id(self):
        """Identificador único; no tiene setter, por eso no se puede cambiar."""
        return self._id

    @property
    def fecha_creacion(self):
        """Momento en que se creó la entidad."""
        return self._fecha_creacion

    # ---------- Métodos abstractos (abstracción) ----------
    # Cada clase hija está OBLIGADA a implementarlos; si no lo hace,
    # Python lanza TypeError al intentar crear un objeto de esa clase.
    @abstractmethod
    def describir(self):
        """Devuelve un texto con la información principal de la entidad."""

    @abstractmethod
    def validar(self):
        """Revisa que los datos de la entidad sean correctos.
        Debe lanzar una excepción de excepciones.py si algo está mal."""

    # ---------- Métodos comunes heredados por todas las hijas ----------
    def __str__(self):
        # Polimorfismo: cada hija responde con su propia versión de describir().
        return f"[{type(self).__name__} #{self._id}] {self.describir()}"

    def __eq__(self, otra):
        # Dos entidades son iguales si son del mismo tipo y tienen el mismo ID.
        return type(self) is type(otra) and self._id == otra._id

    def __hash__(self):
        return hash((type(self).__name__, self._id))