"""
Cálculo y Validación del Dígito de Verificación (DV) del NIT en Colombia.
Basado en el algoritmo oficial de la DIAN (Estatuto Tributario, Art. 375 y Decreto 2460 de 2013).
"""

from typing import Union, Tuple, Optional
import re

# Factores primos de ponderación oficial DIAN (hasta 15 dígitos, de derecha a izquierda)
PESOS_DIAN = [71, 67, 59, 53, 47, 43, 41, 37, 29, 23, 19, 17, 13, 7, 3]


def limpiar_nit(nit: Union[str, int]) -> str:
    """
    Limpia el NIT eliminando puntos, espacios y caracteres no numéricos.
    Si incluye guión separador de DV (e.g. 860007386-1), extrae únicamente el cuerpo del NIT.
    """
    nit_str = str(nit).strip()
    if '-' in nit_str:
        nit_str = nit_str.split('-')[0]

    # Remover cualquier caracter no numérico
    limpio = re.sub(r'\D', '', nit_str)
    if not limpio:
        raise ValueError(f"El NIT proporcionado '{nit}' no contiene dígitos numéricos válidos.")
    if len(limpio) > len(PESOS_DIAN):
        raise ValueError(
            f"El NIT '{nit}' excede la longitud máxima soportada por la DIAN ({len(PESOS_DIAN)} dígitos)."
        )
    return limpio


def calcular_dv(nit: Union[str, int]) -> int:
    """
    Calcula el Dígito de Verificación (DV) de un NIT según el algoritmo Módulo 11 de la DIAN.

    :param nit: Número de NIT (sin el dígito de verificación). Puede ser int o str.
    :return: Dígito de verificación entre 0 y 9.
    :raises ValueError: Si el NIT no contiene dígitos válidos o excede la longitud máxima.
    """
    cuerpo = limpiar_nit(nit)
    longitud = len(cuerpo)

    # Seleccionar la sublista de pesos alineada a la derecha
    pesos = PESOS_DIAN[-longitud:]

    suma = sum(int(digito) * peso for digito, peso in zip(cuerpo, pesos))
    residuo = suma % 11

    if residuo in (0, 1):
        return residuo
    return 11 - residuo


def validar_nit(nit: Union[str, int], dv: Optional[Union[str, int]] = None) -> bool:
    """
    Valida si un NIT y su dígito de verificación son correctos.

    Soporta múltiples formatos:
      - validar_nit("860007386-1")
      - validar_nit("860.007.386-1")
      - validar_nit(860007386, 1)
      - validar_nit("860007386", "1")

    :param nit: NIT con o sin formato, opcionalmente con '-DV' al final.
    :param dv: Dígito de verificación si no viene concatenado con guión.
    :return: True si el DV coincide con el cálculo matemático oficial, False en caso contrario.
    """
    nit_str = str(nit).strip()

    if dv is None:
        if '-' in nit_str:
            partes = nit_str.rsplit('-', 1)
            cuerpo = partes[0]
            dv_esperado = partes[1].strip()
        else:
            raise ValueError(
                "Debe proporcionar el dígito de verificación mediante el parámetro 'dv' "
                "o en el formato 'NIT-DV' (ej. '860007386-1')."
            )
    else:
        cuerpo = nit_str
        dv_esperado = str(dv).strip()

    try:
        dv_esperado_int = int(dv_esperado)
    except ValueError:
        return False

    try:
        dv_calculado = calcular_dv(cuerpo)
        return dv_calculado == dv_esperado_int
    except ValueError:
        return False


def formatear_nit(nit: Union[str, int], incluir_dv: bool = True) -> str:
    """
    Formatea un NIT con separadores de miles y guión de DV.
    Ejemplo: 860007386 -> "860.007.386-1"

    :param nit: NIT numérico o cadena.
    :param incluir_dv: Si es True, calcula y añade el "-DV" al final.
    :return: Cadena formateada.
    """
    cuerpo = limpiar_nit(nit)
    num = int(cuerpo)
    # Formato con puntos de miles
    formateado = f"{num:,}".replace(',', '.')

    if incluir_dv:
        dv = calcular_dv(cuerpo)
        return f"{formateado}-{dv}"
    return formateado


class NITValidator:
    """Clase utilitaria de conveniencia para validación y formateo de NITs."""

    @staticmethod
    def calcular_dv(nit: Union[str, int]) -> int:
        return calcular_dv(nit)

    @staticmethod
    def validar(nit: Union[str, int], dv: Optional[Union[str, int]] = None) -> bool:
        return validar_nit(nit, dv)

    @staticmethod
    def formatear(nit: Union[str, int], incluir_dv: bool = True) -> str:
        return formatear_nit(nit, incluir_dv)
