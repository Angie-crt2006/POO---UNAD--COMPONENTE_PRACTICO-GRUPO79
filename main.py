"""
Punto de entrada principal del sistema Software FJ.
Ejecuta secuencialmente 12 operaciones simuladas (válidas e inválidas) demostrando
estabilidad, manejo de excepciones (try/except/else/finally) y registro en logs.
"""

from src.logger import RegistradorLogs  # Importa el gestor de archivo de logs
from src.cliente import Cliente  # Importa la clase Cliente
from src.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada  # Importa los servicios
from src.reserva import Reserva, GestorSoftwareFJ  # Importa Reserva y el gestor principal
from src.excepciones import ErrorSistemaFJ  # Importa la excepción base personalizada


def ejecutar_simulacion() -> None:
    """Orquesta las pruebas secuenciales del sistema sin detener la ejecución ante fallos."""
    # Inicializa el registrador de logs apuntando a logs/sistema.log
    logger = RegistradorLogs("logs/sistema.log")
    # Registra el inicio de la sesión de ejecución en el log
    logger.registrar_evento("INFO", "Main", "=== INICIO DE SIMULACIÓN DEL SISTEMA SOFTWARE FJ ===")
    # Instancia el gestor central en memoria
    gestor = GestorSoftwareFJ(logger)

    print("=================================================================")
    print("   SISTEMA INTEGRAL SOFTWARE FJ - SIMULACIÓN DE OPERACIONES      ")
    print("=================================================================\n")

    # -------------------------------------------------------------------------
    # OPERACIÓN 1: Registro válido de Cliente 1 (uso de try / except / else)
    # -------------------------------------------------------------------------
    print("[Operación 1] Registrando cliente válido (CLI-01)...")
    try:
        # Crea un objeto Cliente con todos sus datos cumpliendo las validaciones
        cliente1 = Cliente("CLI-01", "Laura Gómez", "laura.gomez@empresa.com", "3001234567")
        # Registra el cliente en el gestor
        gestor.registrar_cliente(cliente1)
    except ErrorSistemaFJ as e:
        # Captura cualquier error controlado y lo guarda en el log
        logger.registrar_error("Operacion1", e)
        print(f"  -> Error controlado: {e}")
    else:
        # Se ejecuta únicamente si el bloque try no lanzó ninguna excepción
        print(f"  -> Éxito: {cliente1.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 2: Registro válido de Cliente 2
    # -------------------------------------------------------------------------
    print("\n[Operación 2] Registrando cliente válido (CLI-02)...")
    try:
        # Crea un segundo cliente válido
        cliente2 = Cliente("CLI-02", "Carlos Mendoza", "cmendoza@tech.co", "3159876543")
        # Lo agrega al sistema
        gestor.registrar_cliente(cliente2)
    except ErrorSistemaFJ as e:
        # Registra error en caso de ocurrir
        logger.registrar_error("Operacion2", e)
        print(f"  -> Error controlado: {e}")
    else:
        # Confirma éxito en consola
        print(f"  -> Éxito: {cliente2.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 3: Registro inválido de Cliente (correo mal formado)
    # -------------------------------------------------------------------------
    print("\n[Operación 3] Intentando registrar cliente con correo inválido...")
    try:
        # Intenta crear un cliente con correo sin arroba ni dominio válido
        cliente_malo = Cliente("CLI-03", "Pedro Pérez", "pedro-sin-arroba.com", "3001112233")
        # Intenta registrarlo
        gestor.registrar_cliente(cliente_malo)
    except ErrorSistemaFJ as e:
        # Captura DatoInvalidoError sin que el programa se detenga
        logger.registrar_error("Operacion3", e)
        print(f"  -> Excepción capturada correctamente: {e}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 4: Registro inválido de Cliente (parámetro faltante)
    # -------------------------------------------------------------------------
    print("\n[Operación 4] Intentando registrar cliente con nombre vacío...")
    try:
        # Intenta crear un cliente omitiendo el nombre
        cliente_vacio = Cliente("CLI-04", "", "ana@dominio.com", "3105556677")
        # Intenta registrarlo
        gestor.registrar_cliente(cliente_vacio)
    except ErrorSistemaFJ as e:
        # Captura ParametroFaltanteError y lo envía al archivo de logs
        logger.registrar_error("Operacion4", e)
        print(f"  -> Excepción capturada correctamente: {e}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 5: Creación válida de Servicio 1 (Reserva de Sala)
    # -------------------------------------------------------------------------
    print("\n[Operación 5] Creando servicio válido: Sala de Juntas...")
    try:
        # Instancia una sala con tarifa de $80.000/hora y capacidad de 12 personas
        sala1 = ReservaSala("SRV-01", "Sala Ejecutiva Norte", 80000.0, capacidad=12)
        # Registra el servicio en el catálogo
        gestor.registrar_servicio(sala1)
    except ErrorSistemaFJ as e:
        # Registra cualquier fallo
        logger.registrar_error("Operacion5", e)
        print(f"  -> Error: {e}")
    else:
        # Muestra el resumen del servicio creado
        print(f"  -> Éxito: {sala1.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 6: Creación válida de Servicio 2 (Alquiler de Equipo con stock=1)
    # -------------------------------------------------------------------------
    print("\n[Operación 6] Creando servicio válido: Alquiler de Servidor Portátil...")
    try:
        # Instancia un equipo con 1 unidad en stock
        equipo1 = AlquilerEquipo("SRV-02", "Workstation Dell Precision", 120000.0, stock=1)
        # Registra el equipo en el gestor
        gestor.registrar_servicio(equipo1)
    except ErrorSistemaFJ as e:
        # Guarda error en log
        logger.registrar_error("Operacion6", e)
        print(f"  -> Error: {e}")
    else:
        # Confirma creación
        print(f"  -> Éxito: {equipo1.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 7: Creación válida de Servicio 3 (Asesoría Especializada)
    # -------------------------------------------------------------------------
    print("\n[Operación 7] Creando servicio válido: Asesoría en Arquitectura Cloud...")
    try:
        # Instancia una asesoría técnica
        asesoria1 = AsesoriaEspecializada("SRV-03", "Consultoría DevOps", 150000.0, "Cloud & CI/CD")
        # Registra el servicio
        gestor.registrar_servicio(asesoria1)
    except ErrorSistemaFJ as e:
        # Guarda error en log
        logger.registrar_error("Operacion7", e)
        print(f"  -> Error: {e}")
    else:
        # Confirma creación
        print(f"  -> Éxito: {asesoria1.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 8: Creación inválida de Servicio (tarifa no numérica -> encadenamiento)
    # -------------------------------------------------------------------------
    print("\n[Operación 8] Intentando crear servicio con tarifa no numérica...")
    try:
        # Pasa texto en lugar de número en la tarifa para probar encadenamiento de excepciones
        servicio_malo = ReservaSala("SRV-99", "Sala Defectuosa", "gratis", capacidad=5)
        # Intenta registrarlo
        gestor.registrar_servicio(servicio_malo)
    except ErrorSistemaFJ as e:
        # Registra el error junto con su causa original (__cause__) en el log
        logger.registrar_error("Operacion8", e)
        print(f"  -> Excepción encadenada capturada: {e}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 9: Reserva exitosa de Sala (con recargo por >4h y descuento sobrecargado)
    # -------------------------------------------------------------------------
    print("\n[Operación 9] Procesando reserva exitosa de Sala por 6 horas con 10% descuento...")
    try:
        # Crea la reserva asociando cliente1 y sala1 por 6 horas con descuento del 10%
        res1 = Reserva("RES-01", cliente1, sala1, duracion=6, descuento=0.10)
        # Procesa y confirma la reserva
        gestor.procesar_reserva(res1, confirmar_inmediato=True)
    except ErrorSistemaFJ as e:
        # Captura error si ocurre
        logger.registrar_error("Operacion9", e)
        print(f"  -> Error: {e}")
    else:
        # Muestra el resumen con el costo calculado
        print(f"  -> Éxito: {res1.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 10: Reserva exitosa de Equipo (agota el único stock disponible)
    # -------------------------------------------------------------------------
    print("\n[Operación 10] Procesando reserva de Equipo (consume último stock)...")
    try:
        # Reserva el equipo por 3 días
        res2 = Reserva("RES-02", cliente2, equipo1, duracion=3)
        # Confirma la reserva (el stock de equipo1 baja de 1 a 0)
        gestor.procesar_reserva(res2, confirmar_inmediato=True)
    except ErrorSistemaFJ as e:
        # Registra error en log
        logger.registrar_error("Operacion10", e)
        print(f"  -> Error: {e}")
    else:
        # Muestra el detalle de la reserva confirmada
        print(f"  -> Éxito: {res2.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 11: Reserva fallida por servicio sin stock disponible
    # -------------------------------------------------------------------------
    print("\n[Operación 11] Intentando reservar el mismo Equipo sin stock disponible...")
    try:
        # Intenta reservar nuevamente equipo1 cuyo stock ya es 0
        res3 = Reserva("RES-03", cliente1, equipo1, duracion=2)
        # Intenta procesarla
        gestor.procesar_reserva(res3)
    except ErrorSistemaFJ as e:
        # Captura ServicioNoDisponibleError y mantiene la app funcionando
        logger.registrar_error("Operacion11", e)
        print(f"  -> Excepción controlada (sin stock): {e}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 12: Cancelación de reserva + prueba de doble cancelación (try/except/finally)
    # -------------------------------------------------------------------------
    print("\n[Operación 12] Cancelando reserva RES-02 y probando doble cancelación...")
    try:
        # Cancela la reserva res2 (esto devuelve el equipo al stock automáticamente)
        res2.cancelar()
        # Registra la primera cancelación exitosa
        logger.registrar_evento("INFO", "Operacion12", f"Reserva cancelada: {res2.obtener_resumen()}")
        print(f"  -> Primera cancelación exitosa. Stock restaurado a: {equipo1.stock}")
        # Intenta cancelar nuevamente la misma reserva para forzar ReservaInvalidaError
        res2.cancelar()
    except ErrorSistemaFJ as e:
        # Captura el intento de doble cancelación
        logger.registrar_error("Operacion12", e)
        print(f"  -> Segunda cancelación bloqueada correctamente: {e}")
    finally:
        # El bloque finally se ejecuta siempre para cerrar el ciclo de auditoría
        logger.registrar_evento("INFO", "Main", "=== FIN DE SIMULACIÓN DEL SISTEMA SOFTWARE FJ ===")
        print("\n=================================================================")
        print(f"Resumen Final en Memoria -> Clientes: {len(gestor.clientes)} | "
              f"Servicios: {len(gestor.servicios)} | Reservas: {len(gestor.reservas)}")
        print("Revisa el archivo 'logs/sistema.log' para ver la trazabilidad completa.")
        print("=================================================================")


# Punto de entrada estándar cuando se ejecuta el script directamente
# Inicio de la ejecución principal del proyecto.
if __name__ == "__main__":
    # Llama a la función principal de simulación
    ejecutar_simulacion()
