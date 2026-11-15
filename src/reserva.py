"""
Módulo de gestión de reservas y administración en memoria del sistema Software FJ.
"""

from src.entidad import Entidad  # Importa la clase base Entidad
from src.cliente import Cliente  # Importa la clase Cliente para validación de tipos
from src.servicios import Servicio, AlquilerEquipo  # Importa Servicio y AlquilerEquipo para control de stock
from src.logger import RegistradorLogs  # Importa el registrador de eventos y errores
from src.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ReservaInvalidaError,
)


class Reserva(Entidad):
    """Integra un Cliente, un Servicio, la duración y gestiona el ciclo de vida de la reserva."""

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: int,
        descuento: float = 0.0,
    ):
        try:
            # Inicializa el identificador de la reserva en Entidad
            super().__init__(id_reserva)
        except ValueError as err:
            # Encadena la excepción de ID inválido
            raise ParametroFaltanteError("El ID de la reserva es obligatorio.") from err

        # Verifica que el objeto recibido sea efectivamente una instancia de Cliente
        if not isinstance(cliente, Cliente):
            # Lanza DatoInvalidoError si se pasa un tipo incorrecto
            raise DatoInvalidoError("La reserva requiere una instancia válida de Cliente.")

        # Verifica que el objeto recibido sea una subclase válida de Servicio
        if not isinstance(servicio, Servicio):
            # Lanza DatoInvalidoError si el servicio no es válido
            raise DatoInvalidoError("La reserva requiere una instancia válida de Servicio.")

        # Asigna los objetos relacionados
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.descuento = descuento
        # Inicia toda reserva en estado 'PENDIENTE'
        self.estado = "PENDIENTE"
        # Calcula el costo total invocando el método polimórfico del servicio (esto también valida reglas)
        self.costo_total = self.servicio.calcular_costo(self.duracion, descuento=self.descuento)

    def confirmar(self) -> None:
        """Cambia el estado de la reserva a CONFIRMADA y actualiza inventario si aplica."""
        # Impide confirmar una reserva que ya fue cancelada
        if self.estado == "CANCELADA":
            # Lanza ReservaInvalidaError ante transición de estado prohibida
            raise ReservaInvalidaError(f"No se puede confirmar la reserva {self.id_entidad} porque está CANCELADA.")
        # Impide confirmar dos veces la misma reserva
        if self.estado == "CONFIRMADA":
            # Lanza ReservaInvalidaError por duplicidad de confirmación
            raise ReservaInvalidaError(f"La reserva {self.id_entidad} ya se encuentra CONFIRMADA.")

        # Valida nuevamente que el servicio siga disponible al momento de confirmar
        self.servicio.validar_parametros(self.duracion)

        # Si el servicio es alquiler de equipos, descuenta 1 unidad del stock disponible
        if isinstance(self.servicio, AlquilerEquipo):
            # Resta una unidad del inventario
            self.servicio.stock -= 1
            # Si el stock llega a cero, marca el servicio como no disponible
            if self.servicio.stock == 0:
                # Actualiza disponibilidad a False
                self.servicio.disponible = False

        # Actualiza el estado de la reserva a CONFIRMADA
        self.estado = "CONFIRMADA"

    def cancelar(self) -> None:
        """Cancela la reserva y restaura inventario si había sido confirmada previamente."""
        # Impide cancelar una reserva que ya está cancelada
        if self.estado == "CANCELADA":
            # Lanza ReservaInvalidaError
            raise ReservaInvalidaError(f"La reserva {self.id_entidad} ya fue cancelada previamente.")

        # Si estaba confirmada y era un equipo alquilado, devuelve la unidad al inventario
        if self.estado == "CONFIRMADA" and isinstance(self.servicio, AlquilerEquipo):
            # Incrementa el stock en 1 unidad
            self.servicio.stock += 1
            # Reactiva la disponibilidad del equipo
            self.servicio.disponible = True

        # Cambia el estado de la reserva a CANCELADA
        self.estado = "CANCELADA"

    def obtener_resumen(self) -> str:
        """Retorna el detalle completo de la reserva y su estado actual."""
        # Formatea la información consolidada de la reserva
        return (
            f"Reserva [{self.id_entidad}] | Estado: {self.estado} | "
            f"Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} | Total: ${self.costo_total:,.2f}"
        )


class GestorSoftwareFJ:
    """Administra en memoria (listas) los clientes, servicios y reservas de la empresa."""

    def __init__(self, logger: RegistradorLogs):
        # Almacena referencia al registrador de logs
        self.logger = logger
        # Lista interna para almacenar objetos Cliente (sin base de datos)
        self.clientes: list[Cliente] = []
        # Lista interna para almacenar objetos Servicio
        self.servicios: list[Servicio] = []
        # Lista interna para almacenar objetos Reserva
        self.reservas: list[Reserva] = []

    def registrar_cliente(self, cliente: Cliente) -> None:
        """Agrega un cliente a la lista verificando que no exista un ID duplicado."""
        # Recorre los clientes registrados para evitar duplicidad de ID
        if any(c.id_entidad == cliente.id_entidad for c in self.clientes):
            # Lanza DatoInvalidoError si el ID ya está registrado
            raise DatoInvalidoError(f"Ya existe un cliente registrado con el ID '{cliente.id_entidad}'.")
        # Añade el cliente a la lista en memoria
        self.clientes.append(cliente)
        # Registra el evento exitoso en el archivo de logs
        self.logger.registrar_evento("INFO", "GestorClientes", f"Registrado: {cliente.obtener_resumen()}")

    def registrar_servicio(self, servicio: Servicio) -> None:
        """Agrega un servicio al catálogo en memoria verificando ID único."""
        # Verifica si el ID del servicio ya existe en la lista
        if any(s.id_entidad == servicio.id_entidad for s in self.servicios):
            # Lanza DatoInvalidoError por duplicidad
            raise DatoInvalidoError(f"Ya existe un servicio registrado con el ID '{servicio.id_entidad}'.")
        # Añade el servicio a la lista interna
        self.servicios.append(servicio)
        # Registra el evento en el log
        self.logger.registrar_evento("INFO", "GestorServicios", f"Registrado: {servicio.obtener_resumen()}")

    def procesar_reserva(self, reserva: Reserva, confirmar_inmediato: bool = True) -> None:
        """Registra una reserva en la lista y opcionalmente la confirma."""
        # Verifica que no exista una reserva con el mismo identificador
        if any(r.id_entidad == reserva.id_entidad for r in self.reservas):
            # Lanza ReservaInvalidaError si el ID está repetido
            raise ReservaInvalidaError(f"Ya existe una reserva con el ID '{reserva.id_entidad}'.")
        # Si se solicita confirmación inmediata, ejecuta el método confirmar()
        if confirmar_inmediato:
            # Confirma la reserva (puede lanzar excepciones si no hay disponibilidad)
            reserva.confirmar()
        # Guarda la reserva en la lista en memoria
        self.reservas.append(reserva)
        # Registra la operación en el archivo de logs
        self.logger.registrar_evento("INFO", "GestorReservas", f"Procesada: {reserva.obtener_resumen()}")