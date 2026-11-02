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
| 6 | Nueva venta de productos | Ventas | `facturas`, `detalle_factura`, `tarifas` |
| 7 | Historial de facturas | Ventas | `facturas`, `movimientos_caja` (abonos), `envios_correo` |
| 8 | Ingresar producto y productos registrados | Inventario: productos | `productos`, `categorias_producto`, `marcas`, `precios_producto` |
| 9 | Inventario actual | Inventario: inventario | `productos`, `movimientos_inventario` |
| 10 | Inventario de equipos / máquinas | Inventario de equipos | `ordenes_reparacion`, `equipos`, `estados_orden` (no aporta tabla nueva) |

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
| `facturas` | Observada | Propuesta | No | No |
| `detalle_factura` | Observada (detalle de venta) | Propuesta | No | No |
| `productos` | Observada | Propuesta | No | No |
| `categorias_producto` | Observada (texto libre en el sistema viejo) | Propuesta | No | No |
| `marcas` | Observada (texto libre con variantes) | Propuesta | No | No |
| `tarifas` | Observada (Público, Técnico, Mayorista) | Propuesta | No | No |
| `precios_producto` | Derivada de normalizar las tres columnas de precio | Propuesta, por validar | No | No |
| `movimientos_inventario` | Nueva: no existe en el sistema viejo | Propuesta, por validar | No | No |
| `envios_correo` | Observada ("PDF enviado · correo · fecha") | Propuesta | No | No |

**Tablas que no hacen falta** (aunque haya módulo o pantalla):
- **Inventario de equipos:** es una consulta sobre `ordenes_reparacion` + `equipos` + `clientes`; sus totales (pendientes, reparados, entregados) se cuentan por estado.
- **Cuentas por cobrar:** son las facturas con saldo mayor que 0; los abonos son movimientos de caja enlazados a la factura (D-009). Pendiente de confirmar con la captura del módulo.

**Origen:** *Observada* = aparece en pantalla con sus campos. *Referenciada* = se menciona, pero faltan sus campos.

## Hallazgos del sistema viejo (valoración crítica)
1. **Equipo y orden mezclados.** El formulario "Registrar equipo" crea a la vez el equipo y la orden (`OR-000029`), y la tabla de órdenes tiene un botón "Eliminar equipo". Si el mismo equipo vuelve a reparación, se duplican marca, modelo y serie. Propuesta: separarlos (D-006).
2. **Referencias guardadas como texto.** El concepto de un movimiento es `Reparación OR-000026 · FAC-000016 · Transferencia`: la orden, la factura y el método van dentro de un texto. No se puede consultar ni garantizar que existan. Propuesta: claves foráneas reales; el concepto queda solo para notas libres.
3. **Totales calculados.** "Saldo total", "Efectivo cobrado", "Transferencias", "Tarjetas", "Egresos totales" y la columna "Saldo" se calculan a partir de los movimientos. Guardarlos como columnas los desincroniza. Propuesta: calcularlos con consultas o vistas, no almacenarlos.
4. **Borrado físico.** Clientes y equipos tienen botón "Eliminar". Si un cliente tiene facturas, borrarlo rompe el historial fiscal. Propuesta: borrado lógico (`activo = false`).
5. **Listas fijas.** Tipo de equipo, estado de la orden, tipo y método de movimiento son listas desplegables. Propuesta: tablas catálogo (D-007) para poder añadir valores sin cambiar la estructura.
6. **Marcas y categorías como texto libre.** En inventario aparecen `hp` y `Hp`, `xiomi` (mal escrito), `Laptop` y `repuesto`. Propuesta: catálogos `marcas` (compartido por productos y equipos) y `categorias_producto`.
7. **Servicios con stock.** "Mantenimiento preventivo de laptops" es un producto de categoría *servicio* con stock 4. Un servicio no tiene existencias. Propuesta: `productos.es_servicio`; los servicios no llevan control de stock.
8. **Datos de modelo y serie mezclados.** En equipos aparece el modelo `HP S/N` (la serie dentro del modelo) y la marca escrita junto al modelo. Al migrar habrá que limpiar estos datos.
9. **"Crédito" como forma de pago.** En facturas, la columna "Pago" mezcla el método (Efectivo, Transferencia) con la condición (Crédito). Son cosas distintas: una factura a crédito se paga luego con abonos en efectivo o transferencia (D-009).
10. **Abonado, saldo y estado guardados.** "Abonado", "Saldo" y "Pagado/Pendiente" se calculan a partir de los abonos (D-008).
11. **Facturas que se eliminan.** El historial tiene botón "Eliminar". Una factura emitida no se borra: se anula y queda registrada, sobre todo si tiene validez ante el SRI.
12. **Precio de compra en $0,00.** Todos los productos vistos tienen precio de compra 0, así que "Valor de compra" del inventario es $0. El campo existe pero no se llena; sin él no se puede calcular la ganancia.
13. **Stock editado a mano.** El stock se escribe en el formulario del producto, sin registro de por qué cambió. Propuesta: `movimientos_inventario` (D-010).

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
  - La marca es texto libre en el sistema viejo (`HP`, `hp`, `lenovo`, `sony`…). Usa el catálogo `marcas`, compartido con productos (hallazgo 6).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| cliente_id | BIGINT | FK | No | Dueño del equipo |
| tipo_equipo_id | BIGINT | FK | No | Computadora, laptop, PlayStation… |
| marca_id | BIGINT | FK | Sí | Marca (catálogo `marcas`) |
| modelo | VARCHAR(120) | | Sí | Modelo |
| serie | VARCHAR(80) | | Sí | Número de serie |
| fecha_creacion | TIMESTAMPTZ | | No | Fecha de registro |

**Relaciones:**
- `clientes` 1 → N `equipos` mediante `cliente_id`.
- `tipos_equipo` 1 → N `equipos` mediante `tipo_equipo_id`.
- `marcas` 1 → N `equipos` mediante `marca_id`.
- `equipos` 1 → N `ordenes_reparacion`.

**Historial:**
- 2026-11-02: propuesta, separada de la orden de reparación.

---

## tipos_equipo
- **Estado:** Propuesta
- **Origen:** capturas 4 y 10 (valores vistos: Computadora, Laptop, PlayStation).
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
- **Origen:** capturas 4, 5 y 10 (valores vistos: Recibido, Entregado; los indicadores mencionan "Pendientes: sin finalizar" y "Reparados: listos / reparados").
- **Propósito:** catálogo de estados de una orden de reparación.
- **Justificación:** el filtro "Estado" y los indicadores de Inventario de equipos agrupan las órdenes por estado.
- **Alternativas descartadas:** texto libre (variantes como "recibido" / "Recibido") o `ENUM` (ver D-007).
- **Valoración crítica:**
  - Estados deducidos: Recibido → (¿En reparación?) → Reparado/Listo → Entregado. Falta confirmar la lista completa y si existe "Sin reparación" o "Devuelto sin arreglar".
  - Los indicadores agrupan varios estados ("Pendientes" = sin finalizar). Propuesta: columna `es_final` para saber qué estados cierran la orden.
  - Falta decidir si se guarda el historial de cambios de estado (otra tabla) o solo el estado actual.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(40) | UQ | No | Recibido, Reparado, Entregado… |
| orden | SMALLINT | | No | Posición en el flujo |
| es_final | BOOLEAN | | No | Si cierra la orden (p. ej. Entregado) |

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
  - Un movimiento con `factura_id` es un **abono** a esa factura: el pago total de una venta al contado es un único abono; una venta a crédito recibe varios. Así el mismo dinero no se registra en dos tablas (D-009).
  - Consecuencia de D-009: solo se puede cobrar con una caja abierta. Hay que confirmar que en el local siempre es así, también para transferencias.
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
- `facturas` 1 → N `movimientos_caja` mediante `factura_id` (opcional; son los abonos).
- `usuarios` 1 → N `movimientos_caja` mediante `usuario_id`.

**Historial:**
- 2026-11-02: propuesta.

---

## metodos_pago
- **Estado:** Propuesta
- **Origen:** capturas 1, 2, 6 y 7 (Efectivo, Transferencia, Tarjetas). "Crédito" no es un método de pago (hallazgo 9).
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
- **Estado:** Propuesta
- **Origen:** capturas 6 y 7 (nueva venta e historial de facturas).
- **Propósito:** documento de cobro de una venta de productos o de una reparación.
- **Justificación:** es el documento fiscal del negocio, el origen de los abonos en caja y de las cuentas por cobrar.
- **Alternativas descartadas:**
  - Tablas separadas para facturas de venta y de reparación: comparten numeración (`FAC-000013` a `FAC-000016` mezcla ambos tipos), cliente, totales y abonos.
  - Columna `tipo` (Venta/Reparación): se deduce de si `orden_reparacion_id` está vacío o no, así que guardarla sería redundante.
- **Valoración crítica:**
  - **Totales:** subtotal sin IVA, IVA y total se calculan desde `detalle_factura`. Por tratarse de un documento fiscal, propongo una excepción a D-008: guardarlos al emitir la factura, porque una vez emitida no puede cambiar aunque cambien los precios o el IVA. Por validar.
  - **Abonado, saldo y estado Pagado/Pendiente** se calculan desde los abonos (hallazgo 10).
  - **Anulación en lugar de borrado** (hallazgo 11): columnas `anulada`, `fecha_anulacion` y `motivo_anulacion`.
  - **SRI:** el IVA del 15 % y la cédula/RUC indican Ecuador. La numeración `FAC-000016` no sigue el formato del SRI (`001-001-000000016`), así que hay que confirmar si son facturas electrónicas autorizadas o comprobantes internos. Si son del SRI, faltan clave de acceso, número de autorización, establecimiento y punto de emisión.
  - Una factura de reparación ¿puede llevar repuestos además del servicio? Si sí, todo va en `detalle_factura` y no cambia el modelo.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| numero | VARCHAR(20) | UQ | No | Número visible, p. ej. `FAC-000016` |
| cliente_id | BIGINT | FK | No | Cliente facturado |
| orden_reparacion_id | BIGINT | FK | Sí | Orden cobrada; nula en ventas |
| fecha_emision | TIMESTAMPTZ | | No | Fecha y hora |
| subtotal_sin_iva | NUMERIC(12,2) | | No | Guardado al emitir (por validar) |
| total_iva | NUMERIC(12,2) | | No | Guardado al emitir (por validar) |
| total | NUMERIC(12,2) | | No | Guardado al emitir (por validar) |
| anulada | BOOLEAN | | No | Si fue anulada |
| fecha_anulacion | TIMESTAMPTZ | | Sí | Cuándo se anuló |
| motivo_anulacion | VARCHAR(250) | | Sí | Por qué se anuló |
| usuario_id | BIGINT | FK | No | Quién la emitió |

**Relaciones:**
- `clientes` 1 → N `facturas` mediante `cliente_id`.
- `ordenes_reparacion` 1 → 0..1 `facturas` mediante `orden_reparacion_id` (por confirmar si una orden puede tener más de una factura).
- `facturas` 1 → N `detalle_factura`.
- `facturas` 1 → N `movimientos_caja` (abonos).
- `facturas` 1 → N `envios_correo`.

**Historial:**
- 2026-11-02: propuesta a partir de las capturas de Ventas y Facturas.

---

## detalle_factura
- **Estado:** Propuesta
- **Origen:** captura 6 (producto, cantidad, tarifa y "Detalle de venta").
- **Propósito:** cada línea de una factura.
- **Justificación:** una factura tiene varios productos o servicios; sin esta tabla habría que repetir columnas en la factura.
- **Alternativas descartadas:** guardar las líneas como texto o JSON en la factura (no se puede consultar qué se vendió).
- **Valoración crítica:**
  - **`precio_unitario` y `porcentaje_iva` no son redundantes** aunque el producto ya tenga precio: son una copia del momento de la venta. Si mañana cambia el precio o el IVA, las facturas anteriores no deben cambiar.
  - `tarifa_id` registra con qué tarifa se vendió (Público, Técnico, Mayorista).
  - La pantalla de venta **no tiene descuento**. No lo añado; si se usa, hay que confirmarlo.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| factura_id | BIGINT | FK | No | Factura a la que pertenece |
| producto_id | BIGINT | FK | No | Producto o servicio vendido |
| tarifa_id | BIGINT | FK | No | Tarifa aplicada |
| cantidad | NUMERIC(10,2) | | No | Cantidad, mayor que 0 |
| precio_unitario | NUMERIC(12,2) | | No | Precio con IVA en el momento de la venta |
| porcentaje_iva | NUMERIC(5,2) | | No | IVA aplicado (p. ej. 15.00) |

**Relaciones:**
- `facturas` 1 → N `detalle_factura` mediante `factura_id`.
- `productos` 1 → N `detalle_factura` mediante `producto_id`.
- `tarifas` 1 → N `detalle_factura` mediante `tarifa_id`.

**Historial:**
- 2026-11-02: propuesta.

---

## productos
- **Estado:** Propuesta
- **Origen:** capturas 8 y 9 (formulario de producto, productos registrados e inventario actual; 87 productos).
- **Propósito:** catálogo de lo que se vende: productos físicos (repuestos, laptops) y servicios (mantenimiento).
- **Justificación:** ventas, inventario y facturas dependen de él.
- **Alternativas descartadas:** tablas separadas para productos y servicios. Comparten código, nombre, categoría, precios y se facturan igual; basta `es_servicio`.
- **Valoración crítica:**
  - **Servicios sin stock** (hallazgo 7): si `es_servicio = true`, no tiene movimientos de inventario.
  - **Stock:** el sistema viejo lo guarda en el producto y se edita a mano. Propongo calcularlo desde `movimientos_inventario` (D-010). `stock_minimo` sí se guarda, porque es un parámetro.
  - **Estado "Disponible / Sin stock"** se calcula desde el stock; no es columna.
  - **Precios:** las tres columnas Público, Técnico y Mayorista se pasan a `precios_producto` (D-011). Solo `precio_compra` queda en el producto.
  - **`precio_compra` vacío** en el sistema viejo (hallazgo 12): si siempre será 0, conviene preguntarse si se necesita.
  - **IVA:** los precios incluyen IVA del 15 %. En Ecuador algunos productos llevan IVA 0 %. Si hay productos con distinto IVA, hace falta `porcentaje_iva` en el producto; si no, basta el valor de Configuración.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| codigo | VARCHAR(30) | UQ | No | Código, p. ej. `A0071`, `E001` |
| nombre | VARCHAR(200) | | No | Nombre del producto o servicio |
| categoria_producto_id | BIGINT | FK | No | Servicio, repuesto, laptop… |
| marca_id | BIGINT | FK | Sí | Marca; nula en servicios |
| es_servicio | BOOLEAN | | No | Si no lleva control de stock |
| precio_compra | NUMERIC(12,2) | | Sí | Costo de compra |
| stock_minimo | INTEGER | | No | Umbral para "stock bajo" |
| activo | BOOLEAN | | No | Borrado lógico |

**Relaciones:**
- `categorias_producto` 1 → N `productos`.
- `marcas` 1 → N `productos`.
- `productos` 1 → N `precios_producto`.
- `productos` 1 → N `detalle_factura`.
- `productos` 1 → N `movimientos_inventario`.

**Historial:**
- 2026-11-02: propuesta.

---

## categorias_producto
- **Estado:** Propuesta
- **Origen:** capturas 8 y 9 (servicio, repuesto, Laptop; el campo sugiere "Repuestos, accesorios…").
- **Propósito:** catálogo de categorías de productos.
- **Justificación:** el buscador filtra por categoría y hoy hay variantes de mayúsculas (hallazgo 6).
- **Alternativas descartadas:** texto libre (variantes) o `ENUM` (D-007).
- **Valoración crítica:** "servicio" como categoría se solapa con `es_servicio`. Si todas las categorías de servicio son una sola, se podría quitar `es_servicio` y deducirlo de la categoría; prefiero el indicador porque es explícito. Por validar.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(60) | UQ | No | Servicio, repuesto, laptop, accesorio… |
| activo | BOOLEAN | | No | Si aparece en la lista |

**Historial:**
- 2026-11-02: propuesta.

---

## marcas
- **Estado:** Propuesta
- **Origen:** capturas 8, 9 y 10 (hp, Hp, xiomi, OEM, lenovo, sony…).
- **Propósito:** catálogo de marcas, compartido por productos y equipos.
- **Justificación:** el texto libre ya produjo variantes y errores (`hp`/`Hp`, `xiomi`). Una sola tabla sirve a productos y a equipos de clientes.
- **Alternativas descartadas:** dos catálogos (marcas de productos y marcas de equipos): sería la misma lista repetida.
- **Valoración crítica:** "OEM" no es una marca sino "sin marca/genérico"; se puede mantener como valor del catálogo o dejar `marca_id` nulo. Por decidir.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(60) | UQ | No | HP, Lenovo, Sony, Xiaomi… |
| activo | BOOLEAN | | No | Si aparece en la lista |

**Historial:**
- 2026-11-02: propuesta.

---

## tarifas
- **Estado:** Propuesta
- **Origen:** capturas 6 y 8 (lista "Tarifa" en ventas; columnas Público, Técnico, Mayorista).
- **Propósito:** tipos de precio que se aplican al vender.
- **Justificación:** la venta elige la tarifa por línea, y la factura debe registrar cuál se aplicó.
- **Alternativas descartadas:** guardar el nombre de la tarifa como texto en el detalle.
- **Valoración crítica:** ¿la tarifa depende del cliente (un técnico siempre compra a precio técnico)? Si es así, conviene `clientes.tarifa_id` como tarifa por defecto.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(40) | UQ | No | Público, Técnico, Mayorista |
| activo | BOOLEAN | | No | Si aparece en la lista |

**Historial:**
- 2026-11-02: propuesta.

---

## precios_producto
- **Estado:** Propuesta, por validar (D-011)
- **Origen:** normalización de las columnas Público, Técnico y Mayorista del producto.
- **Propósito:** precio de cada producto en cada tarifa.
- **Justificación:** tres columnas de precio son un grupo repetido. Con esta tabla, una tarifa nueva (p. ej. "Distribuidor") es un registro más, no una columna nueva en `productos` y en todas las pantallas.
- **Alternativas descartadas:** mantener tres columnas en `productos`. Es más simple y válido **si las tarifas nunca cambian**. Es la alternativa a decidir.
- **Valoración crítica:** añade una tabla y una unión al consultar precios. Si las tres tarifas son definitivas, la opción de columnas es aceptable.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| producto_id | BIGINT | PK, FK | No | Producto |
| tarifa_id | BIGINT | PK, FK | No | Tarifa |
| precio | NUMERIC(12,2) | | No | Precio con IVA incluido |

**Relaciones:**
- `productos` 1 → N `precios_producto`.
- `tarifas` 1 → N `precios_producto`.

**Historial:**
- 2026-11-02: propuesta.

---

## movimientos_inventario
- **Estado:** Propuesta, por validar (D-010)
- **Origen:** no existe en el sistema viejo; se propone por el hallazgo 13.
- **Propósito:** cada entrada o salida de unidades de un producto.
- **Justificación:**
  - Hoy el stock se sobrescribe a mano: si un producto pasa de 5 a 1, no se sabe si se vendió, se usó en una reparación, se dañó o fue un error.
  - Con esta tabla cada cambio tiene motivo, fecha, usuario y documento de origen (factura, orden, ajuste).
  - Permite responder "¿cuándo entró este disco y a qué precio?" y detectar pérdidas.
- **Alternativas descartadas:** solo la columna `stock` en `productos`, como el sistema viejo (sin trazabilidad).
- **Valoración crítica:**
  - Es la tabla que más crece; con 87 productos y el volumen de un local no es problema.
  - Las entradas de mercadería (compras) no aparecen en ninguna captura. ¿Hay proveedores y compras registradas? Si sí, harían falta `proveedores` y `compras`; si no, las entradas son ajustes manuales con motivo.
  - Los repuestos usados en una reparación ¿se descuentan del inventario? Si sí, la salida se enlaza a la factura de reparación.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| producto_id | BIGINT | FK | No | Producto |
| tipo | VARCHAR(10) | | No | `entrada` o `salida` (CHECK) |
| motivo | VARCHAR(30) | | No | Venta, compra, ajuste, devolución, daño… |
| cantidad | INTEGER | | No | Unidades, mayor que 0 |
| costo_unitario | NUMERIC(12,2) | | Sí | Costo en entradas |
| factura_id | BIGINT | FK | Sí | Factura que originó la salida |
| observacion | VARCHAR(250) | | Sí | Detalle del ajuste |
| fecha_hora | TIMESTAMPTZ | | No | Fecha y hora |
| usuario_id | BIGINT | FK | No | Quién lo registró |

**Relaciones:**
- `productos` 1 → N `movimientos_inventario`.
- `facturas` 1 → N `movimientos_inventario` (opcional).
- `usuarios` 1 → N `movimientos_inventario`.

**Historial:**
- 2026-11-02: propuesta.

---

## envios_correo
- **Estado:** Propuesta
- **Origen:** capturas 5 y 7 ("Enviar ingreso PDF", "Enviar factura PDF" y la nota "PDF enviado · correo · fecha").
- **Propósito:** registro de cada correo enviado con una factura o una orden de ingreso.
- **Justificación:** el sistema viejo ya muestra a quién y cuándo se envió el PDF. Si el correo falla o el cliente dice que no lo recibió, hay constancia.
- **Alternativas descartadas:** guardar "fecha_envio" y "correo_envio" en la factura (solo recuerda el último envío y no sirve para órdenes).
- **Valoración crítica:** referencia a dos documentos distintos. Se usan dos FK opcionales con un `CHECK` para que solo una esté llena; es más seguro que una referencia genérica sin FK.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT IDENTITY | PK | No | Identificador |
| factura_id | BIGINT | FK | Sí | Factura enviada |
| orden_reparacion_id | BIGINT | FK | Sí | Orden de ingreso enviada |
| destinatario | VARCHAR(150) | | No | Correo de destino |
| fecha_envio | TIMESTAMPTZ | | No | Fecha y hora |
| exitoso | BOOLEAN | | No | Si se envió correctamente |
| error | TEXT | | Sí | Mensaje de error si falló |
| usuario_id | BIGINT | FK | No | Quién lo envió |

**Relaciones:**
- `facturas` 1 → N `envios_correo`.
- `ordenes_reparacion` 1 → N `envios_correo`.

**Historial:**
- 2026-11-02: propuesta.

---

## Pendiente de capturas
| Módulo | Para qué |
|---|---|
| Proformas | Cabecera y detalle de cotización |
| Cuentas por cobrar | Confirmar que basta con facturas y abonos (D-009) |
| Empleados, Perfil y Configuración | Usuarios, roles, datos del negocio, IVA |
| Órdenes (detalle, edición o factura de reparación) | Estados, técnico, diagnóstico, costos, entrega, repuestos |
| Dashboard | Comprobar que todo lo que muestra se calcula con las tablas propuestas |
