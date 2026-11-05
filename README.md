# DRACULATOR 3000

Sistema de registro de donantes de sangre — Ing. SW, grupo 7.

Hoy los donantes se registran en papel. Este sistema permite que el profesional de recolección los
registre y los busque desde el computador. En el Sprint 1 los datos se guardan en un archivo de texto
(`datos/donantes.txt`); todavía no se usa base de datos.

---

## Cómo usarlo

Requiere Python 3.10 o superior (no necesita instalar librerías extra).

```bash
python main.py
```

```
=== DRACULATOR 3000 ===
1. Registrar donante
2. Buscar donante por RUT
0. Salir
```

- **Registrar:** pide los datos uno por uno. Si un dato no es válido, explica por qué y lo vuelve a
  pedir. Si el RUT ya está registrado, avisa y vuelve al menú sin pedir el resto.
- **Buscar:** pide un RUT (con o sin puntos y guion) y muestra los datos del donante.

### Pruebas

```bash
python -m unittest discover -s tests -v
```

---

## Historia de usuario

**H1 · Registrar donante** — Sprint 1 (2 al 13 de noviembre) · Prioridad alta · 3 puntos

> Como profesional de recolección quiero registrar a un donante con sus datos (RUT, nombre, fecha de
> nacimiento, sexo, peso, tipo de sangre y teléfono), para tenerlo identificado sin depender de
> registros en papel.

| Criterio de aceptación | Dónde se cumple | Task |
|---|---|---|
| Registro exitoso con mensaje de confirmación | `servicio.py` → `registrar`, `main.py` | T5, T6 |
| RUT duplicado se rechaza | `servicio.py` → `registrar`, `main.py` | T5, T6 |
| RUT inválido (formato o dígito verificador) | `rut.py` → `validar_rut` | T2 |
| Campos faltantes se señalan | `validaciones.py` → `validar_campo` | T3 |
| Tipo de sangre: solo los 8 grupos | `validaciones.py` → `validar_tipo_sangre` | T3 |
| Peso positivo y fecha no futura | `validaciones.py` → `validar_peso`, `validar_fecha_nacimiento` | T3 |
| Búsqueda por RUT | `servicio.py` → `buscar_por_rut`, `main.py` | T5, T6 |

---

## Tasks

La historia está dividida en 6 tasks. Cada una tiene sus propios archivos, así cada integrante puede
subir la suya por separado. **Se suben en orden**, porque cada una usa lo de las anteriores:

```
T1 Estructura ──┬── T2 RUT ── T3 Validaciones ──┐
                └── T4 Guardado .txt ───────────┴── T5 Registro y búsqueda ── T6 Menú
```

T2 y T4 no dependen entre sí: se pueden hacer al mismo tiempo.

### T1 · Estructura base del proyecto

**Archivos:** `README.md`, `.gitignore`, `donantes/__init__.py`, `tests/__init__.py`
**Depende de:** nada (va primero)

- `donantes/` es la carpeta con el código, y `tests/` la de las pruebas. Los `__init__.py` vacíos le
  dicen a Python que esas carpetas son paquetes, para poder hacer `from donantes import ...`.
- `.gitignore` evita subir `datos/`: son datos personales de donantes y el repositorio es público.
  También ignora `__pycache__/`, que Python genera solo.

### T2 · Validación de RUT

**Archivos:** `donantes/rut.py`, `tests/test_rut.py`
**Depende de:** T1
**Criterio:** RUT inválido

| Función | Qué hace |
|---|---|
| `limpiar_rut` | Quita puntos, guiones y espacios: `12.345.678-5` → `123456785` |
| `calcular_dv` | Calcula el dígito verificador con el algoritmo módulo 11 |
| `validar_rut` | Revisa el formato (7–8 dígitos + dígito o K) y que el dígito verificador sea correcto |
| `normalizar_rut` | Deja el RUT como `12345678-5` |

**Por qué normalizar:** el RUT se puede escribir de muchas formas (`12.345.678-5`, `12345678-5`,
`123456785`). Si se guardan todos de la misma forma, la búsqueda y la detección de duplicados funcionan
sin importar cómo se escribió.

RUT válidos para probar: `12.345.678-5`, `11.111.111-1`, `10.000.013-K`.

### T3 · Validación de los datos del donante

**Archivos:** `donantes/validaciones.py`, `tests/test_validaciones.py`
**Depende de:** T2 (usa `validar_rut`)
**Criterios:** campos faltantes, tipo de sangre, datos numéricos y fechas

| Campo | Regla |
|---|---|
| Nombre | Al menos 2 caracteres, sin números |
| Fecha de nacimiento | Formato `DD-MM-AAAA`, fecha que exista y no futura |
| Sexo | `F` o `M` |
| Peso | Número mayor que 0 (acepta coma o punto: `70,5`) |
| Tipo de sangre | Uno de A+, A−, B+, B−, AB+, AB−, O+, O− |
| Teléfono | Celular chileno: `9` + 8 dígitos, con o sin `+56` |

- `validar_campo(campo, valor)` valida un solo dato. La usa el menú para volver a pedir el dato al tiro.
- `validar_donante(datos)` valida todos y devuelve `{campo: mensaje}` con los que fallaron.

**Por qué devolver mensajes en vez de solo verdadero/falso:** el criterio pide indicar *qué* campo
falla y por qué; con el mensaje la interfaz puede mostrarlo directamente.

**Decisiones a confirmar con el equipo/cliente:** el formato de la fecha, que el sexo sea solo F/M y
que el teléfono sea solo celular chileno.

### T4 · Guardado en archivo .txt

**Archivos:** `donantes/repositorio.py`
**Depende de:** T1
**Se prueba en:** `tests/test_servicio.py` (T5)

- Guarda cada donante en una línea de `datos/donantes.txt`, con los campos separados por `;`:
  ```
  12345678-5;Ana Pérez;15-03-1990;F;62.0;O+;+56912345678
  ```
- `guardar` agrega una línea al final, `listar` lee todas, y `buscar_por_rut` recorre la lista.
- Crea la carpeta `datos/` sola si no existe.

**Por qué el módulo `csv`:** si un nombre trae un `;`, separar a mano con `split(";")` rompería la
línea; `csv` lo maneja solo. **Por qué una clase aparte:** cuando se cambie el `.txt` por una base de
datos, solo hay que cambiar este archivo.

### T5 · Registro y búsqueda de donantes

**Archivos:** `donantes/servicio.py`, `tests/test_servicio.py`
**Depende de:** T2, T3 y T4
**Criterios:** registro exitoso, RUT duplicado, búsqueda

`registrar(datos)` hace, en orden:
1. Valida todos los datos (T3). Si algo falla, lanza `DatosInvalidosError` con los errores por campo.
2. Normaliza los datos: RUT `12345678-5`, sin espacios dobles en el nombre, sexo en mayúscula, etc.
3. Revisa si el RUT ya existe. Si existe, lanza `DonanteDuplicadoError`.
4. Guarda (T4).

`buscar_por_rut(rut)` acepta el RUT en cualquier formato y devuelve el donante, o `None` si no existe.

**Por qué validar aquí aunque el menú ya valide:** es la última barrera antes de guardar. Si en el
futuro otra pantalla llama a `registrar`, igual nunca se guardan datos malos.

Las pruebas usan un archivo temporal (`tempfile`), así nunca tocan los datos reales.

### T6 · Menú de consola

**Archivos:** `main.py`
**Depende de:** T5
**Criterios:** mensaje de confirmación, indicar errores en el campo, mostrar los datos al buscar

- `pedir_campo` pide un dato y lo vuelve a pedir hasta que sea válido.
- `registrar` pide primero el RUT y revisa si ya existe, antes de pedir el resto.
- `buscar` pide un RUT y muestra todos los datos del donante.

---

## Cómo subir cada task

Una rama por task y un Pull Request para que otro integrante la revise (lo pide el Definition of Done).

```bash
git checkout main
git pull
git checkout -b task/T2-validar-rut
git add donantes/rut.py tests/test_rut.py
git commit -m "T2: valida formato y dígito verificador del RUT"
git push -u origin task/T2-validar-rut
```

Después se abre el Pull Request en GitHub hacia `main`. Otro integrante lo revisa, y cuando se aprueba
se hace merge y se sigue con la task siguiente.

Antes de abrir el PR, corran las pruebas para confirmar que pasan:

```bash
python -m unittest discover -s tests -v
```

| Task | Rama sugerida | Archivos |
|---|---|---|
| T1 | `task/T1-estructura` | `README.md` `.gitignore` `donantes/__init__.py` `tests/__init__.py` |
| T2 | `task/T2-validar-rut` | `donantes/rut.py` `tests/test_rut.py` |
| T3 | `task/T3-validaciones` | `donantes/validaciones.py` `tests/test_validaciones.py` |
| T4 | `task/T4-guardado-txt` | `donantes/repositorio.py` |
| T5 | `task/T5-registro-busqueda` | `donantes/servicio.py` `tests/test_servicio.py` |
| T6 | `task/T6-menu` | `main.py` |
