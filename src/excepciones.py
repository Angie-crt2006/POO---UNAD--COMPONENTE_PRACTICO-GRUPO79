"""
Módulo de excepciones personalizadas para el sistema de Software FJ.
Define la jerarquía de errores controlada para mantener la estabilidad de la aplicación.
"""


class ErrorSistemaFJ(Exception):
    """Clase base para todas las excepciones personalizadas del sistema Software FJ."""

    def __init__(self, mensaje: str, codigo: str = "ERR-000"):
        # Almacena el mensaje descriptivo del error ocurrido
        self.mensaje = mensaje
        # Almacena un código interno para facilitar su rastreo en el archivo de logs
        self.codigo = codigo
        # Inicializa la clase padre Exception con el mensaje formateado
        super().__init__(f"[{self.codigo}] {self.mensaje}")


class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un parámetro tiene un formato, tipo o rango no permitido."""

    def __init__(self, mensaje: str):
        # Llama al constructor padre asignando el código específico de datos inválidos
        super().__init__(mensaje, codigo="ERR-101")


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un dato obligatorio para crear una entidad o servicio."""

    def __init__(self, mensaje: str):
        # Llama al constructor padre asignando el código de parámetro faltante
        super().__init__(mensaje, codigo="ERR-102")


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando un servicio no tiene cupo, stock o disponibilidad activa."""

    def __init__(self, mensaje: str):
        # Llama al constructor padre asignando el código de indisponibilidad
        super().__init__(mensaje, codigo="ERR-201")


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza ante conflictos de estado, duración o reglas de negocio en reservas."""

    def __init__(self, mensaje: str):
        # Llama al constructor padre asignando el código de error en reservas
        super().__init__(mensaje, codigo="ERR-301")


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando una operación financiera arroja valores negativos o incoherentes."""

    def __init__(self, mensaje: str):
        # Llama al constructor padre asignando el código de error de cálculo
        super().__init__(mensaje, codigo="ERR-401")