"""
CLI para cálculo y validación de NIT DIAN desde la terminal.
"""

import sys
import argparse
from .validator import calcular_dv, validar_nit, formatear_nit


def main():
    parser = argparse.ArgumentParser(
        description="Calcula o valida el Dígito de Verificación (DV) de un NIT según el algoritmo DIAN (Colombia)."
    )
    parser.add_argument(
        "nit",
        help="Número de NIT a evaluar (ej. '860007386', '860007386-1' o '860.007.386-1')."
    )
    parser.add_argument(
        "-v", "--validate",
        help="Dígito de verificación esperado para validar (opcional si el NIT ya incluye '-DV').",
        default=None
    )
    parser.add_argument(
        "-f", "--format",
        action="store_true",
        help="Imprime el NIT formateado con puntos de miles y guión de DV."
    )

    args = parser.parse_args()

    try:
        if args.format:
            print(formatear_nit(args.nit, incluir_dv=True))
            sys.exit(0)

        # Si el input contiene guión o se pasó --validate, validamos
        if '-' in args.nit or args.validate is not None:
            es_valido = validar_nit(args.nit, args.validate)
            if es_valido:
                print(f"✅ VÁLIDO: El NIT {args.nit} coincide con el algoritmo oficial DIAN.")
                sys.exit(0)
            else:
                print(f"❌ INVÁLIDO: El dígito de verificación del NIT {args.nit} es incorrecto.")
                sys.exit(1)
        else:
            # Modo cálculo de DV
            dv = calcular_dv(args.nit)
            print(f"Dígito de Verificación (DV): {dv}")
            print(f"NIT Completo: {formatear_nit(args.nit, incluir_dv=True)}")
            sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
