# --------------------------------------------------------------
# auto_jcau_inference.py  — Todo en uno
# --------------------------------------------------------------
# Requisitos:
#   - Python >= 3.9
#   - numpy
#   - llama.cpp compilado con -DLLAMA_SHARED_LIBRARY
# --------------------------------------------------------------

import os
import subprocess
import numpy as np
import ctypes
import requests
from typing import List, Tuple

# -----------------------------
# 1️⃣ Descarga modelo GGUF (Hugging Face)
# -----------------------------
MODEL_NAME = "TheBloke/Llama-2-7B-Chat-GGUF"
MODEL_FILE = "llama2-7b-chat.gguf"

if not os.path.exists(MODEL_FILE):
    url = f"https://huggingface.co/{MODEL_NAME}/resolve/main/llama-2-7b-chat.Q4_K_M.gguf?download=true"
    print("[auto] Descargando modelo:", MODEL_NAME)
    r = requests.get(url, stream=True)
    with open(MODEL_FILE, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print("[auto] Descarga completa:", MODEL_FILE)

# -----------------------------
# 2️⃣ Cuantización (opcional si ya GGUF)
# -----------------------------
def cuantizar(ckpt_path: str, bits: int = 4) -> str:
    out_path = ckpt_path.replace('.gguf', f'.q{bits}_0.gguf')
    if os.path.exists(out_path):
        return out_path
    cmd = ["./llama.cpp/convert", "-i", ckpt_path, "-o", out_path, f"-q{bits}"]
    print("[auto] Cuantizando:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    return out_path

# MODEL_FILE = cuantizar(MODEL_FILE, bits=4)  # Descomenta si quieres re-cuantiar

# -----------------------------
# 3️⃣ mmap + wrapper llama.cpp
# -----------------------------
class ModelMMap:
    def __init__(self, gguf_path: str):
        self.file = open(gguf_path, "rb")
        self.m = mmap.mmap(self.file.fileno(), length=0, access=mmap.ACCESS_READ)
    def leer_capa(self, offset: int, length: int) -> np.ndarray:
        self.m.seek(offset)
        buf = self.m.read(length)
        return np.frombuffer(buf, dtype=np.uint8)
    def cerrar(self):
        self.m.close()
        self.file.close()

class LlamaInference:
    def __init__(self, gguf_path: str, n_ctx: int = 4096, n_gpu_layers: int = 0):
        lib_path = "./llama.cpp/libllama.so"  # Linux, ajustar Windows: libllama.dll
        self.lib = ctypes.CDLL(lib_path)
        self.lib.llama_init_from_file.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self.lib.llama_init_from_file.restype = ctypes.c_void_p
        self.ctx = self.lib.llama_init_from_file(gguf_path.encode('utf-8'), n_gpu_layers)
        self.lib.llama_set_context_params.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self.lib.llama_set_context_params(self.ctx, n_ctx)

    def tokenizar(self, texto: str) -> List[int]:
        max_len = 1024
        out = (ctypes.c_int * max_len)()
        n = self.lib.llama_tokenize(self.ctx, texto.encode('utf-8'), out, max_len, True)
        return [out[i] for i in range(n)]

    def detokenizar(self, token_id: int) -> str:
        self.lib.llama_token_to_piece.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self.lib.llama_token_to_piece.restype = ctypes.c_char_p
        return self.lib.llama_token_to_piece(self.ctx, token_id).decode('utf-8')

    def forward(self, input_ids: List[int]) -> List[float]:
        token_arr = (ctypes.c_int * len(input_ids))(*input_ids)
        self.lib.llama_eval.argtypes = [
            ctypes.c_void_p, ctypes.POINTER(ctypes.c_int),
            ctypes.c_int, ctypes.c_int, ctypes.c_int
        ]
        self.lib.llama_eval(self.ctx, token_arr, len(input_ids), 0, 4)
        self.lib.llama_get_logits.argtypes = [ctypes.c_void_p]
        self.lib.llama_get_logits.restype = ctypes.POINTER(ctypes.c_float)
        logits_ptr = self.lib.llama_get_logits(self.ctx)
        vocab_size = self.lib.llama_n_vocab(self.ctx)
        return [logits_ptr[i] for i in range(vocab_size)]

    def cerrar(self):
        self.lib.llama_free(self.ctx)

# -----------------------------
# 4️⃣ Inicializar
# -----------------------------
INFER = LlamaInference(MODEL_FILE, n_ctx=1024, n_gpu_layers=0)

# -----------------------------
# 5️⃣ Forward + muestreo top-p
# -----------------------------
def forward_step(prompt: str, estado: dict) -> Tuple[str, dict]:
    ids = INFER.tokenizar(prompt)
    logits = INFER.forward(ids)
    temp = 0.7
    probs = np.exp(np.array(logits)/temp)
    probs /= probs.sum()
    sorted_idx = np.argsort(probs)[::-1]
    cumulative = np.cumsum(probs[sorted_idx])
    cutoff = sorted_idx[cumulative <= 0.9]
    if len(cutoff) == 0:
        cutoff = sorted_idx[:1]
    probs_cut = probs[cutoff]/probs[cutoff].sum()
    import random
    token_id = random.choices(cutoff, weights=probs_cut, k=1)[0]
    token_str = INFER.detokenizar(token_id)
    nuevo_estado = {"tokens_usados": estado.get("tokens_usados",0)+1}
    return token_str, nuevo_estado

# -----------------------------
# 6️⃣ Ejemplo de uso
# -----------------------------
estado = {}
prompt = "Hola, ¿cómo estás?"
print(">>> Generando texto para prompt:", prompt)
for _ in range(20):  # Genera 20 tokens
    t, estado = forward_step(prompt, estado)
    print(t, end="", flush=True)
print("\n[auto] Tokens generados:", estado["tokens_usados"])

# -----------------------------
# 7️⃣ Cerrar
# -----------------------------
INFER.cerrar()
print("[auto] Proceso terminado.")
