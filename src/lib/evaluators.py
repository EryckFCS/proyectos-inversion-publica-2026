from src.core.config import lpi_settings


def calcular_van_social(flujo_neto_social):
    """
    Calcula el Valor Actual Neto (VAN) Social usando la tasa centralizada.

    Args:
        flujo_neto_social (list): Lista de flujos desde el año 0 (inversión) hasta el final.

    Returns:
        float: VAN Social calculado.
    """
    tasa = lpi_settings.get("evaluacion_social.tasa_social_descuento", 0.12)

    van = 0
    for t, flujo in enumerate(flujo_neto_social):
        van += flujo / ((1 + tasa) ** t)

    return van


def obtener_factores_correccion():
    """Retorna el diccionario de factores de corrección oficiales."""
    return lpi_settings.get("evaluacion_social.factores_correccion", {})
