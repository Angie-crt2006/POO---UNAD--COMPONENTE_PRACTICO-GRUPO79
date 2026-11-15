"""
Módulo que define la clase abstracta base Entidad para todas las estructuras del sistema.
"""

from abc import ABC, abstractmethod  # Importa herramientas para crear clases y métodos abstractos
from datetime import datetime  # Importa datetime para registrar la fecha de creación de cada entidad


class Entidad(ABC):
    """Clase abstracta que representa cualquier entidad general dentro de Software FJ."""

    def __init__(self, id_entidad: str):
        # Valida que el identificador de la entidad no sea nulo ni una cadena vacía
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            # Lanza ValueError si el ID no cumple con el formato básico esperado
            raise ValueError("El identificador de la entidad debe ser un texto no vacío.")
        # Almacena el identificador limpio como atributo protegido
        self._id_entidad = id_entidad.strip()
        # Registra la fecha y hora exacta en que se instanció el objeto
        self._fecha_registro = datetime.now()

    @property
    def id_entidad(self) -> str:
        """Propiedad de solo lectura para acceder al identificador único de la entidad."""
        # Retorna el valor del atributo protegido _id_entidad
        return self._id_entidad

    @property
    def fecha_registro(self) -> datetime:
        """Propiedad de solo lectura para consultar cuándo fue creada la entidad."""
        # Retorna la marca de tiempo de creación
        return self._fecha_registro

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que obliga a las clases hijas a describir su información."""
        # No tiene implementación en la clase base; se delega a las subclases
        pass