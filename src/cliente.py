"""
Módulo que implementa la clase Cliente con encapsulación y validaciones estrictas.
"""

import re  # Importa expresiones regulares para validar formatos de correo y teléfono
from src.entidad import Entidad  # Importa la clase abstracta padre Entidad
from src.excepciones import DatoInvalidoError, ParametroFaltanteError  # Importa excepciones personalizadas


class Cliente(Entidad):
    """Representa a un cliente de Software FJ con validación de datos personales."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        try:
            # Llama al constructor de la clase abstracta Entidad para validar el ID
            super().__init__(id_cliente)
        except ValueError as error_base:
            # Encadena la excepción estándar hacia nuestra excepción personalizada ParametroFaltanteError
            raise ParametroFaltanteError("ID de cliente obligatorio o inválido.") from error_base

        # Asigna los atributos mediante sus setters para ejecutar las validaciones desde el inicio
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        """Getter que retorna el nombre completo del cliente."""
        # Devuelve el atributo privado __nombre
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Setter que valida y asigna el nombre del cliente."""
        # Verifica que el nombre exista y sea una cadena de texto
        if not valor or not isinstance(valor, str):
            # Lanza ParametroFaltanteError si el dato está ausente
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        # Elimina espacios sobrantes a los extremos
        nombre_limpio = valor.strip()
        # Verifica que el nombre tenga al menos 3 caracteres válidos
        if len(nombre_limpio) < 3:
            # Lanza DatoInvalidoError si el nombre es demasiado corto
            raise DatoInvalidoError(f"El nombre '{nombre_limpio}' debe tener al menos 3 caracteres.")
        # Almacena el nombre validado en el atributo privado
        self.__nombre = nombre_limpio

    @property
    def correo(self) -> str:
        """Getter que retorna el correo electrónico del cliente."""
        # Devuelve el atributo privado __correo
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Setter que valida el formato estructural del correo electrónico."""
        # Verifica que el correo no esté vacío
        if not valor or not isinstance(valor, str):
            # Lanza excepción por parámetro faltante
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        # Limpia espacios y convierte a minúsculas
        correo_limpio = valor.strip().lower()
        # Define una expresión regular estándar para correos electrónicos
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        # Evalúa si el correo cumple con el patrón establecido
        if not re.match(patron_correo, correo_limpio):
            # Lanza DatoInvalidoError si el formato del correo es incorrecto
            raise DatoInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        # Guarda el correo validado en el atributo privado
        self.__correo = correo_limpio

    @property
    def telefono(self) -> str:
        """Getter que retorna el número telefónico del cliente."""
        # Devuelve el atributo privado __telefono
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Setter que valida que el teléfono contenga únicamente dígitos válidos."""
        # Verifica que el teléfono sea una cadena no vacía
        if not valor or not isinstance(valor, str):
            # Lanza excepción si falta el teléfono
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        # Elimina espacios en blanco
        tel_limpio = valor.strip()
        # Valida que sean solo números y tengan entre 7 y 15 dígitos
        if not tel_limpio.isdigit() or not (7 <= len(tel_limpio) <= 15):
            # Lanza DatoInvalidoError si contiene letras o longitud incorrecta
            raise DatoInvalidoError(f"El teléfono '{valor}' debe contener entre 7 y 15 dígitos numéricos.")
        # Guarda el teléfono validado
        self.__telefono = tel_limpio

    def obtener_resumen(self) -> str:
        """Implementación polimórfica del resumen de datos del cliente."""
        # Retorna una cadena formateada con los datos encapsulados del cliente
        return f"Cliente [{self.id_entidad}] {self.nombre} | Email: {self.correo} | Tel: {self.telefono}"