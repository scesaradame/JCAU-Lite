#!/usr/bin/env python3
# ----------------------------------------------------------------------
# auto_jcau_inference.py – Versión ligera y autocontenida
# ----------------------------------------------------------------------
# Propósito:
#   * Ofrecer una forma de probar JCAU sin depender de librerías externas.
#   * Si el usuario tiene instalado llama.cpp y desea usar un modelo LLaMA,
#     basta con pasar la opción --use-llama y el script intentará cargarlo.
#
# Dependencias:
#   * Python ≥ 3.9 (solo la librería estándar)
# ----------------------------------------------------------------------

import argparse
import os
import random
import re
import sys
import textwrap
from typing import List, Tuple

# --------------------------------------------------------------
# 1️⃣  Mini‑motor “JCAU” que implementa las 4 funciones básicas.
# --------------------------------------------------------------

def suma(a: float, b: float) -> float:
    """Devuelve a + b."""
    return a + b


def eq_lineal(expr: str) -> str:
    """
    Resuelve ecuaciones lineales del tipo «ax + b = c».
    Sólo soporta una incógnita “x” y coeficientes enteros/decimales.
    """
    # Normalizamos la expresión
    expr = expr.replace(' ', '')
    match = re.fullmatch(r'(?P<a>-?\d*\.?\d*)x(?P<sign>[+-])(?P<b>\d*\.?\d*)=(?P<c>-?\d*\.?\d*)', expr)
    if not match:
        raise ValueError(f"Ecuación no soportada: {expr}")

    a = float(match.group('a') or 1)          # “x” → a=1
    b = float(match.group('b'))
    if match.group('sign') == '-':
        b = -b
    c = float(match.group('c'))

    if a == 0:
        raise ZeroDivisionError("Coeficiente de x no puede ser 0")
    x = (c - b) / a
    return f"x = {x:g}"


def lógica(expr: str) -> bool:
    """
    Evaluación muy básica de lógica proposicional.
    Operadores admitidos:
        ∧  → and
        ∨  → or
        ¬  → not
        →  → implies (a → b == (not a) or b)
    Los operandos deben ser los literales «p», «q», «r», etc.
    """
    # Reemplazamos los símbolos por operadores de Python
    py_expr = expr.replace('∧', ' and ') \
                  .replace('∨', ' or ') \
                  .replace('¬', ' not ') \
                  .replace('→', ' <= ')  # a → b ≡ (not a) or b → a <= b en bool
    # Convertimos cada literal en una variable booleana arbitraria (True)
    # El usuario puede cambiar los valores en la línea inferior si lo desea.
    literals = set(re.findall(r'\b[prqstuvwxyz]\b', py_expr, flags=re.I))
    env = {lit: True for lit in literals}
    return eval(py_expr, {}, env)


def union(set_a: str, set_b: str) -> set:
    """
    Recibe dos conjuntos escritos como listas de números o strings:
        "{1,2,3}" o "a,b,c"
    Devuelve la unión como objeto `set`.
    """
    def parse(s):
        s = s.strip()
        s = s.strip('{}')
        if not s:
            return set()
        return {e.strip() for e in s.split(',')}

    return parse(set_a) | parse(set_b)


# --------------------------------------------------------------
# 2️⃣  Interfaz de línea de comandos
# --------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="auto_jcau_inference",
        description="Demo ligera de JCAU. Funciona sin dependencias externas."
    )
    parser.add_argument(
        "prompt",
        help="Expresión JCAU a evaluar (ej.: 'suma(2,3)')"
    )
    parser.add_argument(
        "--use-llama",
        action="store_true",
        help="Si está disponible, usar un modelo LLaMA (requiere llama.cpp y modelo GGUF)."
    )
    return parser.parse_args()


# --------------------------------------------------------------
# 3️⃣  Lógica de "inferencia automática"
# --------------------------------------------------------------

def evaluar_jcau(prompt: str) -> str:
    """
    Detecta qué función se está llamando y la ejecuta.
    Si la cadena no corresponde a ninguna de nuestras cuatro funciones
    devuelve un mensaje de ayuda.
    """
    # 1) suma
    m = re.fullmatch(r'\s*suma\(\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\)\s*', prompt, flags=re.I)
    if m:
        a, b = map(float, m.groups())
        return str(suma(a, b))

    # 2) ecuación lineal
    m = re.fullmatch(r'\s*eq_lineal\(\s*([^\)]+)\s*\)\s*', prompt, flags=re.I)
    if m:
        return eq_lineal(m.group(1))

    # 3) lógica proposicional
    m = re.fullmatch(r'\s*\(?\s*([^\)]+)\s*\)?\s*', prompt, flags=re.I)
    if '∧' in prompt or '∨' in prompt or '¬' in prompt or '→' in prompt:
        try:
            return str(lógica(prompt))
        except Exception as e:
            return f"Error en lógica: {e}"

    # 4) unión de conjuntos
    if '∪' in prompt:
        left, right = map(str.strip, prompt.split('∪', 1))
        try:
            return str(union(left, right))
        except Exception as e:
            return f"Error en unión: {e}"

    return "Prompt no reconocido. Consulta la sección 'Ejemplo rápido' del README."


# --------------------------------------------------------------
# 4️⃣  (Opcional) Compatibilidad con LLaMA – *muy ligera*
# --------------------------------------------------------------

def _cargar_modelo_llama(gguf_path: str):
    """
    Carga la librería compartida de llama.cpp si está presente.
    Si algo falla, simplemente devolvemos None y el programa continúa.
    """
    lib_path = "./llama.cpp/libllama.so"
    if not os.path.isfile(lib_path):
        print("[auto] libllama.so no encontrado → se usará el motor nativo.", file=sys.stderr)
        return None

    try:
        import ctypes
        lib = ctypes.CDLL(lib_path)
        # Sólo inicializamos para comprobar que la API básica está disponible
        lib.llama_init_from_file.argtypes = [ctypes.c_char_p, ctypes.c_int]
        lib.llama_init_from_file.restype = ctypes.c_void_p
        ctx = lib.llama_init_from_file(gguf_path.encode(), 0)
        if not ctx:
            raise RuntimeError("No se pudo crear el contexto LLaMA")
        print("[auto] Modelo LLaMA cargado correctamente.")
        return (lib, ctx)
    except Exception as e:
        print(f"[auto] Error al cargar llama.cpp: {e}", file=sys.stderr)
        return None


def _generar_con_llama(prompt: str, lib_ctx) -> str:
    """
    Generación simplificada con LLaMA. No es un wrapper completo,
    solo muestra cómo se podría integrar. Si el usuario decide usarlo,
    asumimos que conoce las limitaciones.
    """
    lib, ctx = lib_ctx
    # Tokenizar
    lib.llama_tokenize.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                   ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_bool]
    lib.llama_tokenize.restype = ctypes.c_int
    max_len = 1024
    buffer = (ctypes.c_int * max_len)()
    n = lib.llama_tokenize(ctx, prompt.encode(), buffer, max_len, True)
    tokens = [buffer[i] for i in range(n)]

    # Forward (inferencia) – solo una pasada rápida
    lib.llama_eval.argtypes = [ctypes.c_void_p,
                               ctypes.POINTER(ctypes.c_int),
                               ctypes.c_int, ctypes.c_int, ctypes.c_int]
    lib.llama_eval(ctx, (ctypes.c_int * n)(*tokens), n, 0, 4)

    # Obtener el token ‘más probable’
    lib.llama_get_logits.restype = ctypes.POINTER(ctypes.c_float)
    logits = lib.llama_get_logits(ctx)
    vocab = lib.llama_n_vocab(ctx)
    probs = [logits[i] for i in range(vocab)]
    best_id = max(range(vocab), key=lambda i: probs[i])

    lib.llama_token_to_piece.argtypes = [ctypes.c_void_p, ctypes.c_int]
    lib.llama_token_to_piece.restype = ctypes.c_char_p
    out = lib.llama_token_to_piece(ctx, best_id).decode()
    return out


# --------------------------------------------------------------
# 5️⃣  Entrada principal
# --------------------------------------------------------------

def main() -> None:
    args = parse_args()

    # 1) Intentamos la evaluación nativa (sin LLaMA)
    resultado = evaluar_jcau(args.prompt)
    print("[auto] Resultado (nativo):", resultado)

    # 2) Si el usuario lo solicita y existen los binarios, usamos LLaMA
    if args.use_llama:
        gguf = "llama2-7b-chat.gguf"          # nombre por defecto
        if not os.path.isfile(gguf):
            print(f"[auto] Modelo GGUF \"{gguf}\" no encontrado → se omite LLaMA.", file=sys.stderr)
        else:
            lib_ctx = _cargar_modelo_llama(gguf)
            if lib_ctx:
                llama_out = _generar_con_llama(args.prompt, lib_ctx)
                print("[auto] Resultado (LLaMA):", llama_out)

if __name__ == "__main__":
    main()

