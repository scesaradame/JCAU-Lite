# 📚 Bibliotecas Lite – Todo el ecosistema matemático (un solo archivo)

> **Formato usado:** `nombre(parámetros) → expresión`.  
> Cada línea es auto‑contenida, no requiere dependencias externas y puede ser interpretada por cualquier motor que siga la regla “una definición por línea”.

---  

## 1️⃣ Aritmética básica  

| Definición | Comentario |
|------------|------------|
| `suma(a,b) → a + b` | Suma de dos números |
| `resta(a,b) → a - b` | Resta |
| `multiplicacion(a,b) → a * b` | Producto |
| `division(a,b) → a / b` | División (b ≠ 0) |
| `potencia(a,n) → a ^ n` | Potencia con exponente entero `n ≥ 0` |
| `modulo(a,b) → a % b` | Resto de la división entera |

---  

## 2️⃣ Álgebra elemental  

| Definición | Comentario |
|------------|------------|
| `eq_lineal(ax+b=0) → -b / a` | Solución de la ecuación lineal `ax + b = 0` |
| `evaluar_lineal(a,b,x) → a * x + b` | Valor de una expresión lineal |
| `discriminante(a,b,c) → b ^ 2 - 4 * a * c` | Discriminante de la cuadrática |
| `raiz_cuadratica_mas(a,b,c) → (-b + sqrt(discriminante(a,b,c))) / (2 * a)` | Raíz +  |
| `raiz_cuadratica_menos(a,b,c) → (-b - sqrt(discriminante(a,b,c))) / (2 * a)` | Raíz ‑  |
| `cuadrado_suma(a,b) → (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2` | Identidad del cuadrado de una suma |
| `cuadrado_resta(a,b) → (a - b) ^ 2 = a ^ 2 - 2 * a * b + b ^ 2` | Identidad del cuadrado de una resta |
| `producto_suma_resta(a,b) → (a + b) * (a - b) = a ^ 2 - b ^ 2` | Diferencia de cuadrados |
| `factor_diferencia_cuadrados(a,b) → (a - b) * (a + b)` | Factorización de `a²‑b²` |
| `expandir_diferencia_cuadrados(a,b) → a ^ 2 - b ^ 2` | Expansión inversa |
| `det2(a,b,c,d) → a * d - b * c` | Determinante de una matriz 2 × 2 |
| `cramer_x(a,b,c,d,e,f) → det2(e,b,f,d) / det2(a,b,c,d)` | Solución x por regla de Cramer |
| `cramer_y(a,b,c,d,e,f) → det2(a,e,c,f) / det2(a,b,c,d)` | Solución y por regla de Cramer |

---  

## 3️⃣ Cálculo elemental  

| Definición | Comentario |
|------------|------------|
| `derivada_polinomio(k,n) → k * n * x ^ (n-1)` | Derivada de `k·xⁿ` (asume variable `x`) |
| `integral_polinomio(k,n) → k * x ^ (n+1) / (n+1)` | Integral indefinida de `k·xⁿ` (n ≠ ‑1) |
| `limite_constante(c) → c` | Límite de una constante |
| `limite_x_a(x,a) → a` | Límite de `x` cuando `x→a` |
| `serie_geometrica(r,n) → (1 - r ^ (n+1)) / (1 - r)` | Suma de los primeros `n+1` términos de `1 + r + r² + …` |
| `factorial(n) → n!` | Factorial (n entero ≥ 0) |

---  

## 4️⃣ Trigonometría básica  

| Definición | Comentario |
|------------|------------|
| `seno(x) → sin(x)` | Seno (x en radianes) |
| `coseno(x) → cos(x)` | Coseno |
| `tangente(x) → tan(x)` | Tangente |
| `cotangente(x) → 1 / tan(x)` | Cotangente |
| `arcseno(x) → asin(x)` | Arco‑seno |
| `arccoseno(x) → acos(x)` | Arco‑coseno |
| `arctangente(x) → atan(x)` | Arco‑tangente |
| `grados_a_radianes(g) → g * π / 180` | Conversión grados → radianes |
| `radianes_a_grados(r) → r * 180 / π` | Conversión radianes → grados |

---  

## 5️⃣ Geometría plana y espacial  

| Definición | Comentario |
|------------|------------|
| `area_circulo(r) → π * r ^ 2` | Área del círculo |
| `perimetro_circulo(r) → 2 * π * r` | Circunferencia |
| `area_rectangulo(a,b) → a * b` | Área del rectángulo |
| `perimetro_rectangulo(a,b) → 2 * (a + b)` | Perímetro del rectángulo |
| `area_triangulo(b,h) → (b * h) / 2` | Área de triángulo (base × altura / 2) |
| `perimetro_triangulo(a,b,c) → a + b + c` | Perímetro de triángulo |
| `area_trapecio(b1,b2,h) → (b1 + b2) * h / 2` | Área de trapecio |
| `area_cuadrado(l) → l ^ 2` | Área del cuadrado |
| `volumen_cubo(l) → l ^ 3` | Volumen del cubo |
| `volumen_esfera(r) → (4/3) * π * r ^ 3` | Volumen de la esfera |
| `volumen_prisma_base_area(A,h) → A * h` | Volumen de prisma (base de área `A`) |

---  

## 6️⃣ Estadística y probabilidad básica  

| Definición | Comentario |
|------------|------------|
| `media(lista) → sum(lista) / len(lista)` | Promedio |
| `varianza(lista) → sum((x - media(lista))^2 for x in lista) / len(lista)` | Varianza poblacional |
| `desviacion_estandar(lista) → sqrt(varianza(lista))` | Desviación típica |
| `probabilidad(evento,total) → evento / total` | Frecuencia relativa |
| `combinaciones(n,k) → n! / (k! * (n-k)!)` | Número de formas de elegir *k* sin orden |
| `permutaciones(n,k) → n! / (n-k)!` | Número de formas de elegir *k* con orden |
| `binomial(k,n,p) → combinaciones(n,k) * p^k * (1-p)^(n-k)` | Distribución binomial (prob. de **k** éxitos en **n** intentos) |

---  

## 7️⃣ Números complejos (lite)  

| Definición | Comentario |
|------------|------------|
| `modulo_complex(z) → sqrt(re(z)^2 + im(z)^2)` | Módulo (magnitud) |
| `conjugado(z) → re(z) - im(z)·i` | Conjugado |
| `parte_real(z) → re(z)` | Parte real |
| `parte_imaginaria(z) → im(z)` | Parte imaginaria |
| `suma_complex(a,b) → (re(a)+re(b)) + (im(a)+im(b))·i` | Suma de complejos |
| `producto_complex(a,b) → (re(a)*re(b) - im(a)*im(b)) + (re(a)*im(b)+im(a)*re(b))·i` | Producto de complejos |

---  

## 8️⃣ Lógica proposicional (extendida)  

| Definición | Comentario |
|------------|------------|
| `negacion(p) → ¬ p` | Negación |
| `conjuncion(p,q) → p ∧ q` | Conjunción |
| `disyuncion(p,q) → p ∨ q` | Disyunción |
| `implicacion(p,q) → p → q` | Implicación |
| `equivalencia(p,q) → (p → q) ∧ (q → p)` | Equivalencia lógica |
| `xor(p,q) → (p ∨ q) ∧ ¬(p ∧ q)` | Disyunción exclusiva (XOR) |

---  

## 9️⃣ Conjuntos (extendida)

| Definición | Comentario |
|------------|------------|
| `pertenece(x,A) → x ∈ A` | Pertenencia |
| `no_pertenece(x,A) → x ∉ A` | No pertenencia |
| `union(A,B) → A ∪ B` | Unión |
| `interseccion(A,B) → A ∩ B` | Intersección |
| `diferencia(A,B) → A \ B` | Diferencia (A menos B) |
| `producto_cartesiano(A,B) → {(a,b) | a ∈ A ∧ b ∈ B}` | Producto cartesiano |
| `conjunto_vacio() → ∅` | Conjunto vacío |
| `potencia(A) → ℘(A)` | Conjunto potencia (todos los subconjuntos) |

---  
