#!/usr/bin/env python3
# ----------------------------------------------------------------------
# hybrid_jcau_engine.py – La fusión de dos filosofías.
# ----------------------------------------------------------------------
# Propósito:
#   * Crear un motor robusto que combine la precisión del código nativo
#     con la flexibilidad de un LLM como fallback.
#   * Capa 1: Un motor de composición dinámica para evaluar JCAU estricto.
#   * Capa 2: Un LLM (llama.cpp) para interpretar prompts ambiguos o
#     en lenguaje natural.
#
# Dependencias:
#   * Python ≥ 3.9 (solo la librería estándar)
# ----------------------------------------------------------------------

import argparse
import os
import re
import sys
import ctypes
from typing import Dict, Callable, Any, List

# --------------------------------------------------------------
# 1️⃣  Biblioteca de Funciones Nativas JCAU
# --------------------------------------------------------------

def suma(a: float, b: float) -> float:
    """Devuelve a + b."""
    return a + b

def eq_lineal(expr: str) -> float:
    """Resuelve ecuaciones «ax+b=c» y devuelve solo el valor numérico."""
    expr = expr.replace(' ', '')
    match = re.fullmatch(r'(?P<a>-?\d*\.?\d*)x(?P<sign>[+-])(?P<b>\d*\.?\d*)=(?P<c>-?\d*\.?\d*)', expr)
    if not match:
        raise ValueError(f"Ecuación no soportada: {expr}")
    a = float(match.group('a') if match.group('a') not in ('', '-') else 1.0)
    b = float(match.group('b'))
    if match.group('sign') == '-':
        b = -b
    c = float(match.group('c'))
    if a == 0:
        raise ZeroDivisionError("Coeficiente de x no puede ser 0")
    return (c - b) / a

def logica(expr: str) -> bool:
    """Evaluación de lógica proposicional."""
    py_expr = expr.replace('∧', ' and ').replace('∨', ' or ').replace('¬', ' not ').replace('→', ' <= ')
    literals = set(re.findall(r'\b[p-z]\b', py_expr, flags=re.I))
    env = {lit: True for lit in literals} # Asignación por defecto
    return eval(py_expr, {"__builtins__": {}}, env)

def union(set_a_str: str, set_b_str: str) -> str:
    """Calcula la unión de dos conjuntos representados como strings."""
    def parse_set(s: str) -> set:
        s = s.strip().strip('{}')
        if not s: return set()
        return {e.strip() for e in s.split(',')}
    
    set_a = parse_set(set_a_str)
    set_b = parse_set(set_b_str)
    result_set = set_a | set_b
    return '{' + ', '.join(sorted(list(result_set))) + '}'

# --------------------------------------------------------------
# 2️⃣  Motor Híbrido JCAU
# --------------------------------------------------------------

class HybridJCAUEngine:
    """
    Un motor que primero intenta resolver una expresión JCAU de forma nativa
    y puede delegar a un LLM si falla o se le solicita.
    """
    def __init__(self):
        self._functions: Dict[str, Callable[..., Any]] = {}
        self.register_default_functions()

    def register_function(self, name: str, func: Callable[..., Any]):
        """Registra una nueva función nativa en el motor."""
        self._functions[name.lower()] = func

    def register_default_functions(self):
        """Registra las funciones JCAU estándar."""
        self.register_function("suma", suma)
        self.register_function("eq_lineal", eq_lineal)
        self.register_function("logica", logica)
        self.register_function("union", union)

    def evaluate_native(self, prompt: str) -> str:
        """
        Evalúa la expresión usando el motor de composición dinámica.
        Lanza una excepción si no puede resolverla de forma nativa.
        """
        expr = prompt.strip()
        
        innermost_call = re.compile(r'(\b\w+\b)\s*\(([^()]*)\)')

        MAX_ITERATIONS = 100
        iterations = 0

        while (match := innermost_call.search(expr)) and iterations < MAX_ITERATIONS:
            func_name = match.group(1).lower()
            args_str = match.group(2)
            
            if func_name in self._functions:
                func = self._functions[func_name]
                
                try:
                    args = [arg.strip() for arg in args_str.split(',')] if args_str else []
                    
                    processed_args = []
                    for arg in args:
                        try:
                            processed_args.append(float(arg))
                        except ValueError:
                            processed_args.append(arg)

                    result = func(*processed_args)
                    expr = expr.replace(match.group(0), str(result), 1)
                except Exception as e:
                    raise RuntimeError(f"Error al ejecutar '{func_name}': {e}")
            else:
                raise ValueError(f"Función nativa desconocida: '{func_name}'")
            
            iterations += 1
        
        if innermost_call.search(expr):
             raise RuntimeError("Expresión demasiado compleja o malformada (posible bucle infinito).")
        
        try:
            float(expr)
            return expr
        except ValueError:
             if expr.lower() in ['true', 'false'] or expr.startswith('{'):
                 return expr
             raise ValueError("La expresión final no pudo ser resuelta a un valor simple.")

# --------------------------------------------------------------
# 3️⃣  Lógica de Inferencia y Fallback a LLaMA
# --------------------------------------------------------------

def _cargar_modelo_llama(gguf_path: str):
    """
    Carga la librería compartida de llama.cpp si está presente.
    Si algo falla, simplemente devolvemos None y el programa continúa.
    """
    lib_path = "./llama.cpp/libllama.so"
    if not os.path.isfile(lib_path):
        print("[Motor LLaMA] libllama.so no encontrado → se omite LLaMA.", file=sys.stderr)
        return None

    try:
        lib = ctypes.CDLL(lib_path)
        lib.llama_init_from_file.argtypes = [ctypes.c_char_p, ctypes.c_int]
        lib.llama_init_from_file.restype = ctypes.c_void_p
        ctx = lib.llama_init_from_file(gguf_path.encode(), 0)
        if not ctx:
            raise RuntimeError("No se pudo crear el contexto LLaMA")
        print("[Motor LLaMA] Modelo LLaMA cargado correctamente.")
        return (lib, ctx)
    except Exception as e:
        print(f"[Motor LLaMA] Error al cargar llama.cpp: {e}", file=sys.stderr)
        return None


def _generar_con_llama(prompt: str, lib_ctx) -> str:
    """
    Generación simplificada con LLaMA.
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

    # Forward (inferencia)
    lib.llama_eval.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int),
                               ctypes.c_int, ctypes.c_int, ctypes.c_int]
    lib.llama_eval(ctx, (ctypes.c_int * n)(*tokens), n, 0, 4)

    # Obtener el token más probable
    lib.llama_get_logits.restype = ctypes.POINTER(ctypes.c_float)
    logits = lib.llama_get_logits(ctx)
    vocab = lib.llama_n_vocab(ctx)
    probs = [logits[i] for i in range(vocab)]
    best_id = max(range(vocab), key=lambda i: probs[i])

    lib.llama_token_to_piece.argtypes = [ctypes.c_void_p, ctypes.c_int]
    lib.llama_token_to_piece.restype = ctypes.c_char_p
    out = lib.llama_token_to_piece(ctx, best_id).decode()
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="hybrid_jcau_engine",
        description="Motor Híbrido JCAU: precisión nativa con fallback a IA."
    )
    parser.add_argument(
        "prompt",
        help="Expresión JCAU o pregunta en lenguaje natural."
    )
    parser.add_argument(
        "--use-llama",
        action="store_true",
        help="Permitir el uso de LLaMA como fallback si la evaluación nativa falla."
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    engine = HybridJCAUEngine()

    print(f"▶️  Procesando prompt: '{args.prompt}'")
    
    native_result = None
    native_error = None

    # --- Capa 1: Intento de Ejecución Nativa ---
    try:
        native_result = engine.evaluate_native(args.prompt)
        print(f"✅ [Motor Nativo] Resultado: {native_result}")
    except Exception as e:
        native_error = e
        print(f"⚠️  [Motor Nativo] Falló: {e}")

    # --- Capa 2: Fallback a Inferencia con LLM ---
    if native_error and args.use_llama:
        print("\n🔄  Delegando al motor de inferencia LLaMA...")
        gguf = "llama2-7b-chat.gguf"
        if not os.path.isfile(gguf):
            print(f"⚠️  [Motor LLaMA] Modelo GGUF '{gguf}' no encontrado.", file=sys.stderr)
        else:
            lib_ctx = _cargar_modelo_llama(gguf)
            if lib_ctx:
                llama_out = _generar_con_llama(args.prompt, lib_ctx)
                print(f"🧠 [Motor LLaMA] Respuesta: {llama_out}")

if __name__ == "__main__":
    main()

