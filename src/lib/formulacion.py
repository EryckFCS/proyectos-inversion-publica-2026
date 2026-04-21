def proyectar_demanda(demanda_inicial, tasa_crecimiento, periodos):
    """
    Proyecta la demanda de un servicio público basándose en una tasa de crecimiento.

    Args:
        demanda_inicial (float): Valor inicial de la demanda (Año 0).
        tasa_crecimiento (float): Tasa de crecimiento anual (ej. 0.02 para 2%).
        periodos (int): Número de años a proyectar.

    Returns:
        list: Lista de demanda proyectada [Año 0, Año 1, ..., Año n].
    """
    proyeccion = [demanda_inicial]
    for _ in range(1, periodos + 1):
        demanda_inicial *= 1 + tasa_crecimiento
        proyeccion.append(demanda_inicial)
    return proyeccion


def calcular_brecha(demanda_proyectada, capacidad_existente):
    """
    Calcula la brecha (déficit) de servicio.
    """
    return [max(0, d - capacidad_existente) for d in demanda_proyectada]
