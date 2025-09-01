# 📜 Especificación de JCAU‑Lite

JCAU‑Lite es un *mini‑lenguaje* pensado para describir expresiones matemáticas y lógicas de forma legible.  
A continuación se describen sus **cuatro construcciones** y la **gramática** que las define.

## 1.  Operación `suma(a, b)`

- **Sintaxis**: `suma( <número>, <número> )`
- **Semántica**: devuelve la suma aritmética de los dos operandos.
- **Ejemplo**: `suma(2, 3) → 5`

## 2.  Ecuación lineal `eq_lineal(expr)`

- **Sintaxis**: `eq_lineal( <expresión> )`
- **Formato de `<expresión>`**: `ax + b = c` donde `a, b, c` pueden ser enteros o decimales (el signo de `a` puede omitirse; `a = 1` implícito).
- **Semántica**: resuelve para `x` y devuelve `x = <valor>`.
- **Ejemplo**: `eq_linea

l(2x + 3 = 7) → x = 2`

## 3.  Lógica proposicional

- **Operadores admitidos**  

| Símbolo | Significado |
|---------|-------------|
| `∧`     | **AND** (conjunción) |
| `∨`     | **OR** (disyunción) |
| `¬`     | **NOT** (negación) |
| `→`     | **IMPLICA** (implicación) |

- **Átomos**: cualquier letra minúscula (`p`, `q`, `r`, …) representa una proposición booleana.  
- **Ejemplo**: `p ∧ ¬q → r` se evalúa como `True` si `p` es verdadero, `q` es falso y `r` es verdadero.

## 4.  Unión de conjuntos `A ∪ B`

- **Representación de conjuntos**: `{1,2,3}` o una lista separada por comas sin llaves (`1,2,3`).  
- **Operador**: `∪` (U) devuelve la unión (todos los elementos distintos).  
- **Ejemplo**: `{1,2} ∪ {2,3,4} → {1,2,3,4}`

---

## Gramática (BNF‑like)

::= ::= | <eq_lineal> | |

::= "suma" "(" "," ")" <eq_lineal> ::= "eq_lineal" "(" ")" ::= { ("∧" | "∨" | "→") }* ::= "∪"

::= [-+]?[0-9]+(.[0-9]+)? ::= "x" ( "+" | "-" ) "=" ::= | "" // si está vacío = 1 ::= | "¬" ::= [a-z] ::= "{" [ ] "}" ::= { "," }* ::= |


---

## Cómo usar la spec

1. **Lee la sección “Gramática”.**  
2. **Implementa un parser** en el lenguaje que prefieras siguiendo esas reglas.  
3. **Evalúa** usando la semántica descrita en cada bloque.  

> La spec es **autocontenida**; no depende de Python, de `auto_jcau_inference.py` ni de ningún otro archivo. Cualquier IA que reciba este fichero podrá generar automáticamente un intérprete para la plataforma que necesite.  

---  

© 2025 Julio César Adame Urias – Todos los derechos reservados.
