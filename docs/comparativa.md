# ⚖️ Comparativa de versiones JCAU  

| Característica | **JCAU Lite** (actual) | **JCAU Full** (próximo) | **JCAU Pro** (visión a largo plazo) |
|----------------|------------------------|--------------------------|--------------------------------------|
| **Enfoque** | Didáctico, ultra‑ligero | Extensión académica y de investigación | Plataforma de IA y computación de alto rendimiento |
| **Peso** | < 1 KB (solo texto) | ~ 5 KB (añade álgebra, geometría, estadística) | > 10 KB (incluye wrappers a NumPy/JAX, símbolos avanzados) |
| **Aritmética básica** | ✅ `suma`, `resta`, `multiplicación`, `división`, `potencia` | ✅ (igual) | ✅ (igual) |
| **Lógica proposicional** | ✅ Conectores `¬, ∧, ∨, →` | ✅ + cuantificadores `∀, ∃` | ✅ + razonamiento simbólico avanzado, pruebas automáticas |
| **Conjuntos** | ✅ Pertenencia, unión, intersección, vacío | ✅ + diferencia, producto cartesiano, potencia | ✅ + operaciones de teoría de tipos y categorías |
| **Álgebra** | ❌ Sólo notación informal | ✅ Ecuaciones lineales y cuadráticas, identidades notables, factorización, Cramer 2×2 | ✅ + álgebra lineal n × n, eigen‑valores, SVD, cálculo simbólico |
| **Cálculo** | ❌ | ✅ Derivadas e integrales de polinomios, límites, series geométricas | ✅ + cálculo multivariable, integración simbólica, series de Taylor |
| **Trigonometría** | ❌ | ✅ Seno, coseno, tangente, arcos, conversiones grados↔rad | ✅ + identidades trigonométricas avanzadas, funciones especiales |
| **Geometría** | ❌ | ✅ Área/perímetro de figuras planas, volumen de sólidos básicos | ✅ + geometría diferencial, curvas paramétricas |
| **Estadística y Probabilidad** | ❌ | ✅ Media, varianza, desviación, combinaciones, binomial | ✅ + distribuciones continuas, regresión lineal, inferencia bayesiana |
| **Números complejos** | ❌ | ✅ Módulo, conjugado, parte real/imaginaria, operaciones básicas | ✅ + funciones de variable compleja, transformadas de Fourier |
| **Back‑ends** | ❌ (solo Python std‑lib) | ❌ (todavía independiente) | ✅ Integración opcional con **NumPy**, **JAX**, **PyTorch**, GPU/TPU |
| **Interfaz IA** | ❌ | ❌ | ✅ API para LLMs (prompt → código JCAU), generación automática de pruebas |
| **Público objetivo** | • Estudiantes <br>• Docentes <br>• Modelos de lenguaje que necesiten un “lenguaje universal” simple | • Académicos <br>• Investigadores <br>• Desarrolladores de software educativo | • Científicos de datos <br>• Laboratorios de investigación <br>• Empresas tecnológicas que integren IA y cálculo simbólico |

---

## Resumen rápido

| Versión | Pros | Contras |
|--------|------|---------|
| **Lite** | ✔️ Muy ligera, sin dependencias. <br>✔️ Ideal para introducción y para que cualquier LLM la lea sin complicaciones. | ✖️ No cubre álgebra avanzada, cálculo, probabilidad, etc. |
| **Full** | ✔️ Añade todo el *cuerpo* de matemáticas de nivel medio‑alto (álgebra, geometría, estadística, trigonometría). <br>✔️ Sigue sin depender de paquetes externos. | ✖️ El archivo se vuelve más grande (≈ 5 KB) pero sigue siendo portátil. |
| **Pro** | ✔️ Conecta JCAU con ecosistemas de IA y cálculo de alto rendimiento. <br>✔️ Permite razonamiento simbólico avanzado y uso de GPUs/TPUs. | ✖️ Requiere opcionalmente librerías externas (NumPy, JAX, etc.) y una capa de integración más compleja. |

---

> **Nota:** Cada versión mantiene la **sintaxis “nombre(parámetros) → expresión”**; solo se añaden nuevas definiciones.  Por ello la transición de **Lite → Full → Pro** es **compatible hacia atrás**: los scripts escritos para la versión Lite continúan funcionando sin cambios en las versiones más avanzadas. 

---  

*¡Listo! Copia este bloque en un archivo llamado `comparativa.md` y tendrás la tabla comparativa lista para ser incluida en la documentación de tu proyecto.* 🚀
