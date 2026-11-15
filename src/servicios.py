"""
Módulo de servicios de Software FJ.
Implementa abstracción, herencia, polimorfismo y métodos sobrecargados de cálculo de costos.
"""

from abc import abstractmethod  # Importa decorador para métodos abstractos
from src.entidad import Entidad  # Importa la clase base Entidad
from src.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


class Servicio(Entidad):
    """Clase abstracta que modela cualquier servicio ofrecido por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        try:
            # Inicializa el ID heredado de Entidad
            super().__init__(id_servicio)
        except ValueError as err:
            # Encadena la excepción si el ID del servicio es vacío
            raise ParametroFaltanteError("El ID del servicio es obligatorio.") from err

        # Valida que el nombre del servicio sea una cadena válida
        if not nombre or not isinstance(nombre, str) or not nombre.strip():
            # Lanza excepción si falta el nombre
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")

        try:
            # Intenta convertir la tarifa base a flotante para asegurar operaciones matemáticas
            tarifa_num = float(tarifa_base)
        except (TypeError, ValueError) as err:
            # Encadena el error de conversión a DatoInvalidoError
            raise DatoInvalidoError(f"La tarifa base '{tarifa_base}' debe ser numérica.") from err

        # Valida que la tarifa base sea estrictamente mayor que cero
        if tarifa_num <= 0:
            # Lanza DatoInvalidoError ante tarifas negativas o nulas
            raise DatoInvalidoError("La tarifa base del servicio debe ser mayor a 0.")

        # Asigna los atributos protegidos del servicio
        self._nombre = nombre.strip()
        self._tarifa_base = tarifa_num
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        """Retorna el nombre comercial del servicio."""
        # Devuelve el atributo protegido _nombre
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        """Retorna la tarifa base por unidad de tiempo."""
        # Devuelve el atributo protegido _tarifa_base
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está habilitado para ser reservado."""
        # Devuelve el estado de disponibilidad
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        """Permite activar o desactivar la disponibilidad del servicio."""
        # Actualiza el indicador booleano de disponibilidad
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, duracion: int) -> None:
        """Método abstracto para validar reglas específicas de cada tipo de servicio."""
        # Cada subclase definirá sus propios límites de tiempo o capacidad
        pass

    @abstractmethod
    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """
        Método abstracto y sobrecargado mediante parámetros opcionales (descuento e impuesto)
        para calcular el valor total del servicio.
        """
        # Será sobrescrito polimórficamente por cada servicio especializado
        pass

    def _aplicar_ajustes_financieros(self, subtotal: float, descuento: float, impuesto: float) -> float:
        """Método auxiliar protegido que aplica descuentos e impuestos validando consistencia."""
        # Valida que el porcentaje de descuento esté entre 0% (0.0) y 100% (1.0)
        if not (0.0 <= descuento <= 1.0):
            # Lanza CalculoInconsistenteError si el descuento es inválido
            raise CalculoInconsistenteError(f"Descuento inválido ({descuento}). Debe estar entre 0.0 y 1.0.")
        # Valida que el impuesto no sea negativo ni exagerado
        if not (0.0 <= impuesto <= 1.0):
            # Lanza CalculoInconsistenteError si el impuesto está fuera de rango
            raise CalculoInconsistenteError(f"Impuesto inválido ({impuesto}). Debe estar entre 0.0 y 1.0.")

        # Calcula el valor después de restar el descuento
        valor_con_descuento = subtotal * (1 - descuento)
        # Calcula el monto final sumando el impuesto (ej. IVA 19%)
        total = round(valor_con_descuento * (1 + impuesto), 2)

        # Verifica que el resultado final nunca sea negativo
        if total < 0:
            # Lanza excepción si ocurre una inconsistencia numérica
            raise CalculoInconsistenteError("El cálculo financiero produjo un total negativo.")
        # Retorna el valor final redondeado a dos decimales
        return total


class ReservaSala(Servicio):
    """Servicio especializado para el alquiler de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, disponible: bool = True):
        # Inicializa los atributos comunes mediante el constructor padre
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        # Valida que la capacidad de personas sea un entero positivo
        if not isinstance(capacidad, int) or capacidad <= 0:
            # Lanza DatoInvalidoError si la capacidad no es válida
            raise DatoInvalidoError("La capacidad de la sala debe ser un número entero mayor a 0.")
        # Almacena la capacidad máxima de la sala
        self.capacidad = capacidad

    def validar_parametros(self, duracion: int) -> None:
        """Valida disponibilidad y que la reserva de sala sea entre 1 y 12 horas."""
        # Verifica si la sala está disponible actualmente
        if not self.disponible:
            # Lanza ServicioNoDisponibleError si la sala está ocupada o en mantenimiento
            raise ServicioNoDisponibleError(f"La sala '{self.nombre}' no se encuentra disponible.")
        # Verifica que la duración en horas esté dentro del rango permitido (1 a 12 horas)
        if not isinstance(duracion, int) or not (1 <= duracion <= 12):
            # Lanza DatoInvalidoError si la duración está fuera de rango
            raise DatoInvalidoError("La reserva de sala debe tener una duración entre 1 y 12 horas.")

    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula el costo de la sala incluyendo un recargo de limpieza fijo si supera 4 horas."""
        # Ejecuta primero las validaciones específicas del servicio
        self.validar_parametros(duracion)
        # Calcula el subtotal multiplicando la tarifa por las horas reservadas
        subtotal = self.tarifa_base * duracion
        # Si la reserva supera las 4 horas, añade un cargo logístico fijo de 15.000
        if duracion > 4:
            # Suma el recargo de logística al subtotal
            subtotal += 15000.0
        # Aplica descuentos e impuestos usando el método financiero común
        return self._aplicar_ajustes_financieros(subtotal, descuento, impuesto)

    def obtener_resumen(self) -> str:
        """Describe los detalles específicos de la sala."""
        # Retorna cadena descriptiva de la sala
        return f"Sala '{self.nombre}' (Capacidad: {self.capacidad} pers.) - ${self.tarifa_base:,.2f}/hora"


class AlquilerEquipo(Servicio):
    """Servicio especializado para el alquiler diario de equipos tecnológicos."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_dia: float, stock: int, disponible: bool = True):
        # Inicializa atributos comunes desde Servicio
        super().__init__(id_servicio, nombre, tarifa_dia, disponible)
        # Valida que el inventario inicial no sea negativo
        if not isinstance(stock, int) or stock < 0:
            # Lanza DatoInvalidoError si el stock es negativo
            raise DatoInvalidoError("El stock de equipos no puede ser negativo.")
        # Almacena la cantidad de equipos disponibles en inventario
        self.stock = stock
        # Si el stock es cero, marca automáticamente el servicio como no disponible
        if self.stock == 0:
            # Actualiza disponibilidad a False
            self.disponible = False

    def validar_parametros(self, duracion: int) -> None:
        """Valida existencia de stock y duración en días (mínimo 1 día, máximo 30 días)."""
        # Verifica disponibilidad y existencia física en inventario
        if not self.disponible or self.stock <= 0:
            # Lanza ServicioNoDisponibleError si no hay unidades disponibles
            raise ServicioNoDisponibleError(f"No hay stock disponible para el equipo '{self.nombre}'.")
        # Verifica que la duración en días sea un entero entre 1 y 30
        if not isinstance(duracion, int) or not (1 <= duracion <= 30):
            # Lanza DatoInvalidoError si los días solicitados son inválidos
            raise DatoInvalidoError("El alquiler de equipos debe ser entre 1 y 30 días.")

    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula el costo del alquiler incluyendo póliza de seguro del 5% sobre el subtotal."""
        # Valida los parámetros antes de calcular
        self.validar_parametros(duracion)
        # Calcula el costo base por los días solicitados
        base = self.tarifa_base * duracion
        # Añade un 5% obligatorio por concepto de seguro del equipo
        subtotal_con_seguro = base * 1.05
        # Aplica descuentos e impuestos
        return self._aplicar_ajustes_financieros(subtotal_con_seguro, descuento, impuesto)

    def obtener_resumen(self) -> str:
        """Describe los detalles del equipo y su stock disponible."""
        # Retorna cadena formateada con el stock y tarifa diaria
        return f"Equipo '{self.nombre}' (Stock: {self.stock} und.) - ${self.tarifa_base:,.2f}/día"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica o ingeniería por sesiones/horas."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_sesion: float, especialidad: str, disponible: bool = True):
        # Llama al constructor padre
        super().__init__(id_servicio, nombre, tarifa_sesion, disponible)
        # Valida que se especifique el área de especialidad
        if not especialidad or not isinstance(especialidad, str) or not especialidad.strip():
            # Lanza ParametroFaltanteError si falta la especialidad
            raise ParametroFaltanteError("La especialidad de la asesoría es obligatoria.")
        # Guarda el área de especialidad limpia
        self.especialidad = especialidad.strip()

    def validar_parametros(self, duracion: int) -> None:
        """Valida disponibilidad y duración de la asesoría (entre 1 y 8 horas)."""
        # Comprueba si el consultor/servicio está disponible
        if not self.disponible:
            # Lanza ServicioNoDisponibleError si la agenda está cerrada
            raise ServicioNoDisponibleError(f"La asesoría '{self.nombre}' no está disponible actualmente.")
        # Valida que la duración esté entre 1 y 8 horas
        if not isinstance(duracion, int) or not (1 <= duracion <= 8):
            # Lanza DatoInvalidoError si el tiempo es inválido
            raise DatoInvalidoError("Las asesorías especializadas se programan entre 1 y 8 horas.")

    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula el costo de la asesoría aplicando tarifa preferencial si supera 5 horas."""
        # Valida parámetros de entrada
        self.validar_parametros(duracion)
        # Calcula el subtotal normal
        subtotal = self.tarifa_base * duracion
        # Si contrata más de 5 horas, otorga un bono adicional de 10% sobre el descuento
        descuento_efectivo = min(1.0, descuento + 0.10) if duracion > 5 else descuento
        # Retorna el cálculo financiero final
        return self._aplicar_ajustes_financieros(subtotal, descuento_efectivo, impuesto)

    def obtener_resumen(self) -> str:
        """Describe el servicio de asesoría y su rama técnica."""
        # Retorna descripción de la asesoría
        return f"Asesoría '{self.nombre}' [Área: {self.especialidad}] - ${self.tarifa_base:,.2f}/hora"