"""
Módulo de compatibilidad hacia atrás con el script histórico verification.py.
Delega al paquete modular nit_validator.
"""

from nit_validator.validator import (
    calcular_dv,
    validar_nit,
    formatear_nit,
    PESOS_DIAN,
)

# Alias de compatibilidad con código histórico
digit_list = PESOS_DIAN[-9:]


def products_sum(n_list, d_list):
    return sum(n * d for n, d in zip(n_list, d_list))


def verificar_nit(NIT, digito):
    return validar_nit(NIT, digito)


if __name__ == '__main__':
    # Bancolombia S.A.
    print("Verificación NIT 860007386 - 1:", verificar_nit(860007386, 1))
    print("DV Calculado:", calcular_dv(860007386))
