#!/usr/bin/env bash
# ----------------------------------------------------------------------
# jcau_universal_adapter.sh – Adaptador universal para JCAU‑Lite
# ----------------------------------------------------------------------
# Uso:
#   ./jcau_universal_adapter.sh "suma(2,3)"
#   ./jcau_universal_adapter.sh "eq_lineal(2x+3=7)" --llama   # opcional
#
# El script delega la mayor parte del trabajo a auto_jcau_inference.py.
# ----------------------------------------------------------------------

# Detectar si se pasó la opción --llama
USE_LLAMA=0
for arg in "$@"; do
    if [[ "$arg" == "--llama" ]]; then
        USE_LLAMA=1
        break
    fi
done

# Construir el argumento de prompt (todo salvo la opción --llama)
PROMPT=$(printf "%s " "$@" | sed -E 's/--llama//g' | xargs)

# Ejecutar el script Python
if [[ $USE_LLAMA -eq 1 ]]; then
    python3 "$(dirname "$0")/auto_jcau_inference.py" "$PROMPT" --use-llama
else
    python3 "$(dirname "$0")/auto_jcau_inference.py" "$PROMPT"
fi
