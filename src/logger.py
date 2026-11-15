"""
Módulo encargado de registrar eventos y errores en un archivo de texto plano (logs),
cumpliendo el requisito de no utilizar bases de datos.
"""

import os  # Permite verificar y crear directorios en el sistema de archivos
from datetime import datetime  # Permite obtener la fecha y hora exacta de cada evento


class RegistradorLogs:
    """Gestiona la escritura secuencial de eventos y excepciones en el archivo de logs."""

    def __init__(self, ruta_archivo: str = "logs/sistema.log"):
        # Guarda la ruta donde se almacenará el historial de eventos
        self.ruta_archivo = ruta_archivo
        # Asegura que la carpeta contenedora exista antes de intentar escribir
        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    def registrar_evento(self, nivel: str, modulo: str, mensaje: str) -> None:
        """Escribe una línea formateada en el archivo de logs sin detener la ejecución."""
        # Genera la marca de tiempo actual en formato Año-Mes-Día Hora:Minuto:Segundo
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Construye la línea estructurada del log
        linea = f"[{marca_tiempo}] [{nivel.upper()}] [{modulo}] -> {mensaje}\n"
        # Abre el archivo en modo 'a' (append) con codificación UTF-8 para agregar al final
        with open(self.ruta_archivo, mode="a", encoding="utf-8") as archivo:
            # Escribe la línea en el archivo de texto
            archivo.write(linea)

    def registrar_error(self, modulo: str, error: Exception) -> None:
        """Registra una excepción capturada junto con su causa encadenada si existe."""
        # Obtiene el nombre de la clase de la excepción (ej. DatoInvalidoError)
        tipo_error = type(error).__name__
        # Verifica si existe una excepción original encadenada mediante 'raise ... from ...'
        causa = f" | Causa original: {repr(error.__cause__)}" if error.__cause__ else ""
        # Delega la escritura al método registrar_evento con nivel ERROR
        self.registrar_evento("ERROR", modulo, f"{tipo_error}: {str(error)}{causa}")