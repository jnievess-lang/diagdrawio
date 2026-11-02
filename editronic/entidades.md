# Entidades de Editronic

Ficha de cada entidad del modelo. Una entidad sin ficha completa no entra al diagrama (ver D-004).

**Fase actual:** levantamiento del sistema viejo a partir de capturas de pantalla. Todas las entidades están en estado **Propuesta** hasta que el usuario valide este archivo. Los diagramas no se tocan hasta entonces.

## Fuentes revisadas
| # | Captura | Módulo | Entidades que aporta |
|---|---|---|---|
| 1 | Caja (saldo, tarjetas resumen, registrar movimiento) | Caja | `sesiones_caja`, `movimientos_caja`, `metodos_pago`, `usuarios` |
| 2 | Movimientos de caja (tabla) | Caja | `movimientos_caja` |
| 3 | Listado de clientes | Clientes | `clientes` |
| 4 | Registrar equipo (formulario) | Equipos | `equipos`, `ordenes_reparacion`, `tipos_equipo`, `estados_orden` |
| 5 | Órdenes ingresadas (tabla) | Equipos | `ordenes_reparacion` |

## Resumen

| Entidad | Origen | Estado | En Dev | En Producción |
|---|---|---|---|---|
| `clientes` | Observada | Propuesta | No | No |
| `equipos` | Observada (separada de la orden, ver D-006) | Propuesta | No | No |
| `tipos_equipo` | Observada (lista desplegable) | Propuesta | No | No |
| `ordenes_reparacion` | Observada | Propuesta | No | No |
| `estados_orden` | Observada (lista desplegable) | Propuesta | No | No |
| `sesiones_caja` | Observada | Propuesta | No | No |
| `movimientos_caja` | Observada | Propuesta | No | No |
| `metodos_pago` | Observada (lista desplegable) | Propuesta | No | No |
| `usuarios` | Observada (usuario y rol en la cabecera) | Propuesta, incompleta | No | No |
| `facturas` | Referenciada (`FAC-000016`), sin captura propia | Pendiente de captura | No | No |

**Origen:** *Observada* = aparece en pantalla con sus campos. *Referenciada* = se menciona, pero faltan sus campos.

## Hallazgos del sistema viejo (valoración crítica)
1. **Equipo y orden mezclados.** El formulario "Registrar equipo" crea a la vez el equipo y la orden (`OR-000029`), y la tabla de órdenes tiene un botón "Eliminar equipo". Si el mismo equipo vuelve a reparación, se duplican marca, modelo y serie. Propuesta: separarlos (D-006).
2. **Referencias guardadas como texto.** El concepto de un movimiento es `Reparación OR-000026 · FAC-000016 · Transferencia`: la orden, la factura y el método van dentro de un texto. No se puede consultar ni garantizar que existan. Propuesta: claves foráneas reales; el concepto queda solo para notas libres.
3. **Totales calculados.** "Saldo total", "Efectivo cobrado", "Transferencias", "Tarjetas", "Egresos totales" y la columna "Saldo" se calculan a partir de los movimientos. Guardarlos como columnas los desincroniza. Propuesta: calcularlos con consultas o vistas, no almacenarlos.
4. **Borrado físico.** Clientes y equipos tienen botón "Eliminar". Si un cliente tiene facturas, borrarlo rompe el historial fiscal. Propuesta: borrado lógico (`activo = false`).
5. **Listas fijas.** Tipo de equipo, estado de la orden, tipo y método de movimiento son listas desplegables. Propuesta: tablas catálogo (D-007) para poder añadir valores sin cambiar la estructura.

---

## clientes
- **Estado:** Propuesta
- **Origen:** captura 3 (listado de clientes, 37 registros).
- **Propósito:** personas o empresas que compran productos o dejan equipos a reparar.
- **Justificación:** las facturas, órdenes y cuentas por cobrar necesitan identificar al cliente. Sin esta tabla, sus datos se repetirían en cada documento.
- **Alternativas descartadas:** guardar nombre y cédula directamente en la factura o la orden (datos duplicados y sin historial por cliente).
- **Valoración crítica:**
  - El sistema viejo usa un solo campo "Nombre" con apellidos y nombres en mayúsculas. Para facturar basta un campo `razon_social`, que sirve para personas y empresas. Separar nombres y apellidos solo merece la pena si se van a buscar u ordenar por apellido.
  - "Cédula/RUC" comparte columna. Hace falta saber qué tipo de identificación es (cédula, RUC, pasaporte, consumidor final), porque la factura lo exige. Propuesta: `tipo_identificacion`.
  - `identificacion` debe ser única.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| tipo_identificacion | VARCHAR(20) | | No | Cédula, RUC, pasaporte, consumidor final |
| identificacion | VARCHAR(20) | UQ | No | Número de cédula o RUC |
| razon_social | VARCHAR(200) | | No | Nombre completo o razón social |
| telefono | VARCHAR(20) | | Sí | Teléfono de contacto |
| correo | VARCHAR(150) | | Sí | Correo para enviar facturas y órdenes |
| direccion | VARCHAR(250) | | Sí | Dirección |
| activo | BOOLEAN | | No | Borrado lógico |
| fecha_creacion | TIMESTAMPTZ | | No | Fecha de registro |

**Relaciones:**
- `clientes` 1 → N `equipos`.
- `clientes` 1 → N `ordenes_reparacion`.
- `clientes` 1 → N `facturas`.

**Historial:**
- 2026-11-02: propuesta a partir de la captura del listado de clientes.

---

## equipos
- **Estado:** Propuesta
- **Origen:** captura 4 (formulario "Registrar equipo").
- **Propósito:** cada aparato físico de un cliente (computadora, impresora, consola…).
- **Justificación:** un mismo equipo puede volver varias veces a reparación. Guardarlo una vez permite ver su historial de órdenes y no repetir marca, modelo y serie.
- **Alternativas descartadas:** guardar marca, modelo y serie en la orden, como hace el sistema viejo (ver D-006).
- **Valoración crítica:**
  - La serie no siempre existe (mandos, equipos sin etiqueta), así que puede ser nula y no puede ser clave única obligatoria.
  - La marca es texto libre en el sistema viejo (`HP`, `hp`…). Una tabla `marcas` evitaría variantes, pero añade mantenimiento; queda como duda abierta.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| cliente_id | BIGINT | FK | No | Dueño del equipo |
| tipo_equipo_id | BIGINT | FK | No | Computadora, impresora, consola… |
| marca | VARCHAR(80) | | Sí | Marca |
| modelo | VARCHAR(120) | | Sí | Modelo |
| serie | VARCHAR(80) | | Sí | Número de serie |
| fecha_creacion | TIMESTAMPTZ | | No | Fecha de registro |

**Relaciones:**
- `clientes` 1 → N `equipos` mediante `cliente_id`.
- `tipos_equipo` 1 → N `equipos` mediante `tipo_equipo_id`.
- `equipos` 1 → N `ordenes_reparacion`.

**Historial:**
- 2026-11-02: propuesta, separada de la orden de reparación.

---

## tipos_equipo
- **Estado:** Propuesta
- **Origen:** captura 4 (lista "Tipo", valor visto: Computadora).
- **Propósito:** catálogo de tipos de equipo que se reparan.
- **Justificación:** permite añadir tipos nuevos sin cambiar la estructura y filtrar reportes por tipo.
- **Alternativas descartadas:** `ENUM` de PostgreSQL (añadir un valor exige cambiar el esquema; ver D-007).
- **Valoración crítica:** tabla pequeña y estable; bajo coste.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(60) | UQ | No | Computadora, impresora, mando, consola… |
| activo | BOOLEAN | | No | Si aparece en la lista |

**Historial:**
- 2026-11-02: propuesta.

---

## ordenes_reparacion
- **Estado:** Propuesta
- **Origen:** capturas 4 y 5 (formulario y tabla "Órdenes ingresadas").
- **Propósito:** cada ingreso de un equipo al servicio técnico.
- **Justificación:** es el documento central del servicio técnico: qué se recibió, qué falla tiene, en qué estado está y qué factura lo cobró.
- **Alternativas descartadas:** guardarlo todo en `equipos` (se pierde el historial de reparaciones del mismo equipo).
- **Valoración crítica:**
  - `cliente_id` se repite respecto a `equipos.cliente_id`. Se mantiene porque el cliente que trae el equipo puede no ser el dueño registrado, y la orden debe conservar a quién se entregó. **Confirmar con el usuario**; si no aplica, se elimina.
  - La relación con la factura se confirma cuando lleguen las capturas de facturación.
  - Falta saber si se registra el técnico asignado, el diagnóstico, el costo estimado y la fecha de entrega.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| numero | VARCHAR(20) | UQ | No | Número visible, p. ej. `OR-000029` |
| equipo_id | BIGINT | FK | No | Equipo recibido |
| cliente_id | BIGINT | FK | No | Cliente que deja el equipo (por confirmar) |
| estado_orden_id | BIGINT | FK | No | Estado actual |
| dano_reportado | TEXT | | No | Falla que indica el cliente |
| observaciones | TEXT | | Sí | Estado físico, accesorios, notas |
| fecha_ingreso | TIMESTAMPTZ | | No | Fecha y hora de recepción |
| usuario_id | BIGINT | FK | No | Usuario que registró la orden |

**Relaciones:**
- `equipos` 1 → N `ordenes_reparacion` mediante `equipo_id`.
- `clientes` 1 → N `ordenes_reparacion` mediante `cliente_id`.
- `estados_orden` 1 → N `ordenes_reparacion` mediante `estado_orden_id`.
- `usuarios` 1 → N `ordenes_reparacion` mediante `usuario_id`.

**Historial:**
- 2026-11-02: propuesta.

---

## estados_orden
- **Estado:** Propuesta
- **Origen:** capturas 4 y 5 (valor visto: Recibido).
- **Propósito:** catálogo de estados de una orden de reparación.
- **Justificación:** el filtro "Estado" de la tabla de órdenes necesita valores fijos y coherentes.
- **Alternativas descartadas:** texto libre (variantes como "recibido" / "Recibido") o `ENUM` (ver D-007).
- **Valoración crítica:** solo se vio "Recibido". Faltan los demás estados (¿en diagnóstico, en reparación, listo, entregado, sin reparación?). Falta decidir si se guarda el historial de cambios de estado (otra tabla) o solo el estado actual.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(40) | UQ | No | Recibido, … |
| orden | SMALLINT | | No | Posición en el flujo |

**Historial:**
- 2026-11-02: propuesta.

---

## sesiones_caja
- **Estado:** Propuesta
- **Origen:** captura 1 ("Caja abierta", fecha de apertura, "Base inicial").
- **Propósito:** cada apertura y cierre de caja de un turno o día.
- **Justificación:** el sistema muestra "Caja abierta" con una base inicial y una fecha. Para cuadrar la caja hay que saber qué movimientos pertenecen a qué apertura y con qué base empezó.
- **Alternativas descartadas:** movimientos sin sesión (no se puede cuadrar por turno ni saber quién abrió y cerró).
- **Valoración crítica:**
  - Los totales de la pantalla no se guardan: se calculan sumando `movimientos_caja` (hallazgo 3).
  - Al cerrar sí conviene guardar el monto contado físicamente, para compararlo con el calculado y ver si falta o sobra dinero.
  - Falta saber si hay una caja o varias (varios puntos de cobro). Si hay varias, se necesita una tabla `cajas`.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| usuario_apertura_id | BIGINT | FK | No | Quién abrió la caja |
| fecha_apertura | TIMESTAMPTZ | | No | Fecha y hora de apertura |
| base_inicial | NUMERIC(12,2) | | No | Efectivo con el que se abre |
| usuario_cierre_id | BIGINT | FK | Sí | Quién la cerró |
| fecha_cierre | TIMESTAMPTZ | | Sí | Nula mientras esté abierta |
| monto_contado_cierre | NUMERIC(12,2) | | Sí | Efectivo contado al cerrar |

**Relaciones:**
- `usuarios` 1 → N `sesiones_caja` (apertura y cierre).
- `sesiones_caja` 1 → N `movimientos_caja`.

**Historial:**
- 2026-11-02: propuesta.

---

## movimientos_caja
- **Estado:** Propuesta
- **Origen:** capturas 1 y 2 (formulario "Registrar movimiento" y tabla "Movimientos de caja").
- **Propósito:** cada entrada o salida de dinero de la caja.
- **Justificación:** es el registro de dinero real. Sin él no hay cuadre de caja ni reporte por método de pago.
- **Alternativas descartadas:** calcular la caja solo desde las facturas (no cubre egresos ni aportes manuales, como "aporte adicional o devolución").
- **Valoración crítica:**
  - La columna "Saldo" no se guarda: es la suma acumulada y se calcula al consultar (hallazgo 3).
  - Cuando el movimiento viene de una factura, se enlaza con `factura_id`, no con texto (hallazgo 2). Los movimientos manuales lo dejan nulo.
  - `tipo` (ingreso o egreso) tiene solo dos valores fijos. Una restricción `CHECK` basta; no hace falta una tabla catálogo.
  - `monto` siempre es positivo; el signo lo da `tipo`.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| sesion_caja_id | BIGINT | FK | No | Apertura de caja a la que pertenece |
| tipo | VARCHAR(10) | | No | `ingreso` o `egreso` (CHECK) |
| metodo_pago_id | BIGINT | FK | No | Efectivo, transferencia, tarjeta |
| monto | NUMERIC(12,2) | | No | Importe, mayor que 0 |
| concepto | VARCHAR(250) | | Sí | Nota libre |
| factura_id | BIGINT | FK | Sí | Factura que originó el movimiento |
| fecha_hora | TIMESTAMPTZ | | No | Fecha y hora |
| usuario_id | BIGINT | FK | No | Quién lo registró |

**Relaciones:**
- `sesiones_caja` 1 → N `movimientos_caja` mediante `sesion_caja_id`.
- `metodos_pago` 1 → N `movimientos_caja` mediante `metodo_pago_id`.
- `facturas` 1 → N `movimientos_caja` mediante `factura_id` (opcional; pendiente de validar con las capturas de facturación).
- `usuarios` 1 → N `movimientos_caja` mediante `usuario_id`.

**Historial:**
- 2026-11-02: propuesta.

---

## metodos_pago
- **Estado:** Propuesta
- **Origen:** capturas 1 y 2 (Efectivo, Transferencia, Tarjetas).
- **Propósito:** catálogo de formas de pago.
- **Justificación:** se usará en caja, facturas y cuentas por cobrar; los reportes agrupan por método.
- **Alternativas descartadas:** texto libre o `ENUM` (ver D-007).
- **Valoración crítica:** si la facturación electrónica exige códigos oficiales de forma de pago, se añadirá una columna `codigo`.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(40) | UQ | No | Efectivo, transferencia, tarjeta |
| activo | BOOLEAN | | No | Si aparece en la lista |

**Historial:**
- 2026-11-02: propuesta.

---

## usuarios
- **Estado:** Propuesta, incompleta
- **Origen:** captura 1 (cabecera: "edison", "Administrador").
- **Propósito:** personas que inician sesión en el sistema.
- **Justificación:** caja, órdenes y facturas registran quién hizo cada operación.
- **Alternativas descartadas:** ninguna todavía.
- **Valoración crítica:**
  - Falta la captura de Empleados. Hay que decidir si `usuarios` y `empleados` son la misma tabla o si un empleado puede no tener acceso al sistema (por ejemplo, un técnico que no usa la aplicación).
  - El rol ("Administrador") probablemente necesita una tabla `roles`; se decide con la captura de Empleados o Configuración.
  - La contraseña nunca se guarda en claro: solo su hash.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| nombre_usuario | VARCHAR(50) | UQ | No | Usuario de acceso (p. ej. `edison`) |
| hash_contrasena | VARCHAR(255) | | No | Contraseña cifrada |
| rol | (pendiente) | | No | Administrador, … |
| activo | BOOLEAN | | No | Si puede iniciar sesión |

**Historial:**
- 2026-11-02: propuesta incompleta.

---

## facturas
- **Estado:** Pendiente de captura
- **Origen:** referenciada en movimientos (`FAC-000015`, `FAC-000016`) y en el botón "Factura de reparación".
- **Lo que se sabe:** hay facturas de venta y de reparación con numeración `FAC-XXXXXX`, y se cobran por transferencia u otros métodos.
- **Lo que falta:** cabecera, detalle, impuestos, relación con productos y órdenes, y si es factura electrónica.
- No se diseña hasta tener las capturas de Ventas y Facturación.

---

## Pendiente de capturas
| Módulo | Para qué |
|---|---|
| Ventas y facturación | Cabecera y detalle de factura, impuestos, cobros |
| Inventario (productos, inventario, inventario de equipos) | Productos, stock, movimientos de inventario |
| Proformas | Cabecera y detalle de cotización |
| Cuentas por cobrar | Saldos y abonos |
| Empleados, Perfil y Configuración | Usuarios, roles, datos del negocio, impuestos |
| Órdenes (detalle o edición) | Estados, técnico, diagnóstico, costos, entrega |
