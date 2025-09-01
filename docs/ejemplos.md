# 🧮 Ejemplos de JCAU Lite (versión completa)

A continuación tienes **un solo archivo markdown** con ejemplos para **todas** las funciones descritas en la biblioteca *Lite*.  
Cada bloque está organizado por temática y sigue la sintaxis `nombre(parámetros) → resultado`.

---  

## 1️⃣ Aritmética básica  

suma(2,3) → 5 resta(10,4) → 6 multiplicacion(7,8) → 56 division(20,5) → 4 potencia(2,5) → 32 modulo(17,5) → 2


---  

## 2️⃣ Álgebra elemental  

### Ecuaciones lineales y cuadráticas  

eq_lineal(2x + 3 = 7) → x = 2 evaluar_lineal(3,-5,2) → 1 # 3·2 + (-5) discriminante(1,-3,-4) → 25 raiz_cuadratica_mas(1,-3,-4) → 4 raiz_cuadratica_menos(1,-3,-4) → -1 evaluar_cuadratica(1,-3,-4,1) → 0 # 1·1² -3·1 -4 = 0


### Identidades notables y factorizaciones  

cuadrado_suma(2,3) → verdadero cuadrado_resta(5,2) → verdadero producto_suma_resta(5,2) → verdadero factor_diferencia_cuadrados(5,2) → (5 - 2)(5 + 2) expandir_diferencia_cuadrados(7,3) → 7^2 - 3^2


### Sistemas lineales 2×2 (Cramer)  

det2(1,2,3,4) → -2 cramer_x(1,2,3,4,5,6) → -1 cramer_y(1,2,3,4,5,6) → 2


---  

## 3️⃣ Cálculo elemental  

derivada_polinomio(3,2) → 6·x # d/dx(3·x^2) = 6·x integral_polinomio(4,2) → 4·x^3/3 # ∫4·x^2 dx = 4·x^3/3 limite_constante(7) → 7 limite_x_a(x,5) → 5 serie_geometrica(0.5,4) → 1.9375 # 1 + 0.5 + 0.25 + 0.125 + 0.0625 factorial(5) → 120


---  

## 4️⃣ Trigonometría  

seno(π/6) → 0.5 coseno(π/3) → 0.5 tangente(π/4) → 1 cotangente(π/4) → 1 arcseno(0.5) → π/6 arccoseno(0.5) → π/3 arctangente(1) → π/4 grados_a_radianes(180) → π radianes_a_grados(π/2) → 90


---  

## 5️⃣ Geometría  

area_circulo(3) → 28.274… # π·3² perimetro_circulo(3) → 18.849… # 2·π·3 area_rectangulo(4,5) → 20 perimetro_rectangulo(4,5) → 18 area_triangulo(6,4) → 12 perimetro_triangulo(3,4,5) → 12 area_trapecio(8,5,3) → 19.5 area_cuadrado(4) → 16 volumen_cubo(3) → 27 volumen_esfera(2) → 33.510… # (4/3)·π·2³ volumen_prisma_base_area(10,7) → 70


---  

## 6️⃣ Estadística y Probabilidad  

media([1,2,3,4]) → 2.5 varianza([1,2,3,4]) → 1.25 desviacion_estandar([1,2,3,4]) → 1.118… probabilidad(3,10) → 0.3 combinaciones(5,2) → 10 permutaciones(5,2) → 20 binomial(2,5,0.4) → 0.3456


---  

## 7️⃣ Números complejos  

modulo_complex(3+4i) → 5 conjugado(2-5i) → 2+5i parte_real(7+2i) → 7 parte_imaginaria(7+2i) → 2 suma_complex(1+2i,3-4i) → 4-2i producto_complex(1+2i,3-4i) → 11+2i


---  

## 8️⃣ Lógica proposicional (extendida)  

negacion(verdadero) → falso conjuncion(verdadero, falso) → falso disyuncion(verdadero, falso) → verdadero implicacion(verdadero, falso) → falso equivalencia(verdadero, verdadero) → verdadero xor(verdadero, falso) → verdadero


---  

## 9️⃣ Conjuntos (extendida)  

A = {1,2,3} B = {3,4,5} union(A,B) → {1,2,3,4,5} interseccion(A,B) → {3} diferencia(A,B) → {1,2} producto_cartesiano(A,B) → {(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,3),(3,4),(3,5)} conjunto_vacio() → ∅ potencia(A) → {∅,{1},{2},{3},{1,2},{1,3},{2,3},{1,2,3}}


---  

### 📌  Cómo usar este archivo

1. Copia todo el contenido en un archivo llamado **`ejemplos.md`** (o cualquier otro nombre que prefieras).  
2. Si tu intérprete de JCAU Lite permite leer directamente archivos, basta con ejecutarlo:  

   ```bash
   ./jcau_universal_adapter.sh "ejemplos.md"
Cada línea se evaluará de forma independiente y mostrará el resultado indicado después de la flecha (→).
