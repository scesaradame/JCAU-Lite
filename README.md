# 🌟 JCAU Lite

**JCAU Lite** es la versión ligera del lenguaje matemático y lógico **JCAU**.  
Su objetivo es ser *autónomo*: cualquiera puede clonar el repositorio y probar
las funcionalidades sin instalar paquetes externos.

---

## 🚀 Propósito

- Ofrecer un lenguaje matemático **simple, claro y didáctico**.  
- Servir como **puerta de entrada** al ecosistema JCAU (Lite → Full → Pro).  
- Compatible con educación, docencia, divulgación y proyectos pequeños.

---

## 📚 Bibliotecas incluidas (implementadas en puro Python)

| Área | Funciones |
|------|-----------|
| **Aritmética básica** | `suma(a,b)` |
| **Álgebra elemental** | `eq_lineal("2x+3=7")` |
| **Lógica proposicional** | `p ∧ ¬q → r` |
| **Teoría de conjuntos básica** | `A ∪ B` |

---

## 🛠️ Instalación (¡cero dependencias!)

```bash
git clone https://github.com/scesaradame/JCAU-Lite.git
cd JCAU-Lite
chmod +x jcau_universal_adapter.sh
```

***Requisito: Python 3.9 o superior (ya viene con la mayoría de distribuciones).***

---

## 📖 Uso rápido

```bash
# 1. Usando el adaptador Bash (recomendado)
./jcau_universal_adapter.sh "suma(2,3)"
# → Resultado (nativo): 5

./jcau_universal_adapter.sh "eq_lineal(2x+3=7)"
# → Resultado (nativo): x = 2

./jcau_universal_adapter.sh "p ∧ ¬q"
# → Resultado (nativo): True

./jcau_universal_adapter.sh "A ∪ B"   # A="{1,2}" B="{2,3,4}"
# → Resultado (nativo): {'1', '2', '3', '4'}
```

---

## 🤖 Usar LLaMA (opcional)

Si ya tienes **llama.cpp** compilado y el modelo `llama2-7b-chat.gguf` en el directorio, puedes solicitar que la respuesta provenga del modelo:

```bash
./jcau_universal_adapter.sh "¿Cuál es la derivada de x^2?" --llama
```

---

## 🔮 Futuro del proyecto

- **JCAU Full** → versión avanzada (álgebra, funciones, probabilidad, física).
- **JCAU Pro** → versión para IA, investigación y laboratorios.

---

## 📄 Licencia

© 2025 **Julio César Adame Urias** Todos los derechos reservados.
