# Registro de decisiones

Cada decisión de diseño con su contexto, alternativas y consecuencias. Las decisiones no se borran: si cambian, se marca la anterior como "Reemplazada por D-XXX".

## Plantilla

```
### D-XXX — Título
- **Fecha:**
- **Estado:** Propuesta | Aceptada | Reemplazada por D-XXX
- **Contexto:** qué problema o duda la origina.
- **Decisión:** qué se decidió.
- **Alternativas descartadas:** cuáles y por qué.
- **Consecuencias:** qué implica (ventajas, costes, riesgos).
```

---

### D-001 — Flujo Dev → Producción con dos archivos
- **Fecha:** 2026-11-02
- **Estado:** Aceptada
- **Contexto:** se necesita experimentar sin romper el modelo aprobado.
- **Decisión:** `ERD-Editronic-Dev.drawio` para trabajo en curso y `ERD-Editronic-Produccion.drawio` solo con cambios aprobados.
- **Alternativas descartadas:** un solo archivo con hojas Dev/Prod (más fácil de desincronizar por error).
- **Consecuencias:** cada paso a producción requiere aprobación explícita y se registra en `project_memory.md`.

### D-002 — Convención de nombres `snake_case` en español
- **Fecha:** 2026-11-02
- **Estado:** Aceptada (2026-11-03, respuesta E)
- **Contexto:** el usuario usó `movimiento_inventarios` como ejemplo.
- **Decisión:** tablas y columnas en `snake_case`, sin tildes ni ñ; PK `id`; FK `<tabla_en_singular>_id`.
- **Alternativas descartadas:** `PascalCase` (`DetalleOrden`), que da problemas de mayúsculas en PostgreSQL.
- **Consecuencias:** el modelo de órdenes de prueba (PascalCase) no sigue esta convención; no se reutiliza tal cual.

### D-003 — Importes con `DECIMAL(12,2)`
- **Fecha:** 2026-11-02
- **Estado:** Aceptada (2026-11-03, respuesta E)
- **Contexto:** los tipos de coma flotante producen errores de redondeo en dinero.
- **Decisión:** todo importe usa `DECIMAL(12,2)`; prohibido `FLOAT`/`REAL`.
- **Alternativas descartadas:** guardar céntimos como `INTEGER` (válido, pero menos legible en el diagrama).
- **Consecuencias:** precisión exacta en cálculos de precios, descuentos e impuestos.

### D-004 — Toda entidad requiere justificación
- **Fecha:** 2026-11-02
- **Estado:** Aceptada
- **Contexto:** evitar diagramas sin sustento.
- **Decisión:** ninguna entidad se añade sin su ficha completa en `entidades.md` (propósito, justificación, alternativas y valoración crítica).
- **Consecuencias:** cada entidad tarda algo más en añadirse, pero el modelo queda defendible.

### D-005 — PostgreSQL como motor de base de datos
- **Fecha:** 2026-11-02
- **Estado:** Aceptada
- **Contexto:** el usuario confirmó que se usará PostgreSQL.
- **Decisión:** los tipos del diagrama son tipos de PostgreSQL: `BIGINT GENERATED ALWAYS AS IDENTITY` para PK, `NUMERIC(12,2)` para importes, `TIMESTAMPTZ` para fechas con hora, `DATE` para fechas, `VARCHAR(n)` o `TEXT` para texto y `BOOLEAN` para indicadores.
- **Alternativas descartadas:** `SERIAL` (obsoleto frente a `IDENTITY`); `TIMESTAMP` sin zona horaria (ambiguo si cambia el servidor); `MONEY` (depende de la configuración regional).
- **Consecuencias:** D-003 se aplica como `NUMERIC(12,2)`, el equivalente de `DECIMAL(12,2)` en PostgreSQL. Los nombres en `snake_case` (D-002) encajan con PostgreSQL, que pasa a minúsculas los nombres sin comillas.

### D-006 — Separar `equipos` de `ordenes_reparacion`
- **Fecha:** 2026-11-02
- **Estado:** Aceptada (2026-11-03, respuesta E)
- **Contexto:** en el sistema viejo, "Registrar equipo" crea el equipo y la orden a la vez, y desde la orden se "elimina el equipo".
- **Decisión:** `equipos` guarda el aparato (tipo, marca, modelo, serie) y `ordenes_reparacion` cada ingreso al taller (daño, observaciones, estado, fecha).
- **Alternativas descartadas:** una sola tabla, como el sistema viejo (marca, modelo y serie se repiten en cada visita y no hay historial por equipo).
- **Consecuencias:** al registrar una orden se busca primero si el equipo ya existe. Un equipo con órdenes no se borra.

### D-007 — Listas de valores como tablas catálogo
- **Fecha:** 2026-11-02
- **Estado:** Aceptada (2026-11-03, respuesta E)
- **Contexto:** tipos de equipo, estados de orden y métodos de pago son listas desplegables que pueden crecer.
- **Decisión:** usar tablas catálogo (`tipos_equipo`, `estados_orden`, `metodos_pago`). Para valores que nunca cambiarán (como `ingreso`/`egreso`) basta una restricción `CHECK`.
- **Alternativas descartadas:** `ENUM` de PostgreSQL (añadir o renombrar valores exige cambiar el esquema); texto libre (variantes y errores de escritura).
- **Consecuencias:** más tablas pequeñas, pero los valores se gestionan desde Configuración sin tocar la base de datos.

### D-008 — No almacenar totales calculados
- **Fecha:** 2026-11-02
- **Estado:** Aceptada (2026-11-03, respuesta E)
- **Contexto:** la pantalla de caja muestra saldo total, totales por método, egresos y saldo acumulado por fila.
- **Decisión:** estos valores se calculan con consultas o vistas a partir de `movimientos_caja` y `sesiones_caja`; no son columnas.
- **Alternativas descartadas:** guardar los totales (se desincronizan si se corrige o anula un movimiento).
- **Consecuencias:** la única cifra de cierre que se guarda es el efectivo contado físicamente, para compararla con la calculada.
- **Excepción propuesta:** los totales de `facturas` se guardan al emitir, porque un documento emitido no puede cambiar (aceptada, respuesta B8).

### D-009 — Los abonos son movimientos de caja
- **Fecha:** 2026-11-02
- **Estado:** Aceptada (2026-11-03, respuesta E)
- **Contexto:** el historial de facturas muestra "Abonado", "Saldo" y un botón "Abonar"; la caja registra ingresos como `Venta FAC-000015 · Transferencia`. Es el mismo dinero visto desde dos pantallas.
- **Decisión:** un abono es un `movimientos_caja` de tipo ingreso con `factura_id`. Abonado = suma de esos movimientos; saldo = total − abonado; estado Pagado/Pendiente = saldo igual a 0 o no. "Crédito" deja de ser método de pago: una venta a crédito es una factura con saldo.
- **Alternativas descartadas:** tabla `abonos` aparte (el mismo pago quedaría en dos tablas y podrían no coincidir).
- **Consecuencias:** no hace falta tabla de cuentas por cobrar. Solo se puede cobrar con caja abierta, también por transferencia (confirmar que el local trabaja así).

### D-010 — Stock calculado desde `movimientos_inventario`
- **Fecha:** 2026-11-02
- **Estado:** Aceptada (2026-11-03, respuesta E)
- **Contexto:** el stock se edita a mano en el producto y no se sabe por qué cambia.
- **Decisión:** el stock de un producto es la suma de entradas menos salidas en `movimientos_inventario`. Cada venta genera su salida automáticamente.
- **Alternativas descartadas:** columna `stock` editable (sin trazabilidad); columna `stock` más movimientos (dos fuentes que pueden no coincidir).
- **Consecuencias:** el stock inicial al migrar se carga como un movimiento de "ajuste inicial". Si en el futuro la consulta fuera lenta, se puede añadir una columna mantenida por la base de datos sin cambiar el modelo.

### D-011 — Precios por tarifa en tabla aparte
- **Fecha:** 2026-11-02
- **Estado:** Aceptada (2026-11-03, respuesta E)
- **Contexto:** cada producto tiene tres columnas de precio: Público, Técnico y Mayorista.
- **Decisión:** catálogo `tarifas` y tabla `precios_producto` (producto, tarifa, precio).
- **Alternativas descartadas:** tres columnas en `productos`, válidas solo si las tarifas no cambiarán nunca.
- **Consecuencias:** una tarifa nueva no cambia la estructura. Consultar el precio requiere unir dos tablas.

### D-012 — Configuración en una tabla de una sola fila
- **Fecha:** 2026-11-02
- **Estado:** Aceptada (2026-11-03, respuesta E)
- **Contexto:** Configuración guarda los datos de la empresa (RUC, nombre, dirección, IVA, logo, cláusulas, colores).
- **Decisión:** tabla `configuracion` con columnas tipadas y una sola fila (`CHECK (id = 1)`).
- **Alternativas descartadas:** tabla clave-valor (todo texto, sin validación); valores en el código (hay que reprogramar para cambiar un dato).
- **Consecuencias:** añadir un parámetro nuevo es añadir una columna. Las credenciales (Gmail API) no se guardan aquí sino en el servidor.

### D-013 — Proformas separadas de facturas
- **Fecha:** 2026-11-02
- **Estado:** Aceptada (2026-11-03, respuesta E)
- **Contexto:** proformas y facturas tienen cabecera y detalle casi iguales.
- **Decisión:** tablas propias `proformas` y `detalle_proforma`; al convertir en venta, la factura guarda `proforma_id`.
- **Alternativas descartadas:** una tabla `documentos` con tipo. Ahorra tablas, pero mezcla un documento fiscal (con abonos, anulación y numeración controlada) con uno que solo vence; muchas columnas quedarían vacías según el tipo.
- **Consecuencias:** dos tablas más con estructura parecida; a cambio, cada una tiene solo las reglas que le corresponden.

### D-014 — Usuarios y empleados son la misma tabla
- **Fecha:** 2026-11-02
- **Estado:** Aceptada (2026-11-03, respuesta E)
- **Contexto:** en la pantalla Empleados cada empleado se crea con usuario, rol y contraseña; el administrador aparece en un bloque aparte.
- **Decisión:** una sola tabla `usuarios` (con `nombre_completo`) y un catálogo `roles`. El administrador es un usuario con rol Administrador.
- **Alternativas descartadas:** `empleados` y `usuarios` por separado (hoy no hay empleados sin acceso); administrador guardado aparte (dos formas de iniciar sesión y dos lugares para la contraseña).
- **Consecuencias:** si en el futuro hay empleados sin acceso al sistema (p. ej. técnicos que no usan la aplicación), se separa en dos tablas.

### D-015 — Garantía configurable por tipo de equipo
- **Fecha:** 2026-11-03
- **Estado:** Aceptada (respuesta A7)
- **Contexto:** el sistema viejo guarda la garantía en cada equipo y casi siempre está en 0 días.
- **Decisión:** `tipos_equipo.dias_garantia` es la garantía por defecto; al crear la orden se copia en `ordenes_reparacion.dias_garantia`. El fin de la garantía se calcula desde la fecha del estado Entregado. Una orden por garantía enlaza con la original mediante `orden_garantia_id`.
- **Alternativas descartadas:** fecha de fin guardada (dato calculado); garantía solo en la configuración del tipo (cambiarla alteraría garantías ya entregadas).
- **Consecuencias:** cambiar la garantía de un tipo solo afecta a las órdenes nuevas.

### D-016 — Historial de estados y estado actual calculado
- **Fecha:** 2026-11-03
- **Estado:** Aceptada (2026-11-03, respuesta P7)
- **Contexto:** el usuario pidió guardar quién y cuándo cambió cada estado (respuesta A3).
- **Decisión:** `historial_estados_orden` registra cada cambio. El estado actual de una orden es el último registro; no hay columna de estado en la orden. Las fechas de reparación y de entrega salen del historial.
- **Alternativas descartadas:** guardar también el estado actual en la orden (dos fuentes que pueden no coincidir, igual que el stock en D-010).
- **Consecuencias:** las consultas por estado usan una vista sobre el historial. Si el rendimiento lo exigiera, se añade una columna mantenida por la base de datos sin cambiar el modelo.

### D-017 — Tres clientes distintos en el servicio técnico
- **Fecha:** 2026-11-03
- **Estado:** Aceptada (respuesta A1 y hallazgo 14)
- **Contexto:** quien trae el equipo no siempre es quien paga; el sistema viejo lo resuelve con campos sueltos (`billedToDifferentPerson`, `serviceClientName`).
- **Decisión:** `equipos.cliente_id` = propietario; `ordenes_reparacion.cliente_id` = quien trae el equipo; `facturas.cliente_id` = a quien se factura. Los tres apuntan a `clientes`.
- **Alternativas descartadas:** copiar nombre y cédula del segundo cliente en la factura (datos sin integridad).
- **Consecuencias:** en la mayoría de los casos los tres son el mismo cliente, y la aplicación lo propone por defecto.

### D-018 — IVA por producto mediante el catálogo `tipos_iva`
- **Fecha:** 2026-11-03
- **Estado:** Aceptada (respuesta B3)
- **Contexto:** hay productos con IVA 0 % y otros con 15 %.
- **Decisión:** `productos.tipo_iva_id`; la configuración guarda el IVA predeterminado para productos nuevos; las líneas de venta copian el porcentaje.
- **Alternativas descartadas:** porcentaje numérico en cada producto (un cambio de tarifa obliga a editarlos todos).
- **Consecuencias:** un cambio de IVA del país es un registro nuevo en `tipos_iva` y una reasignación.

### D-019 — Descuentos por línea, regulados por configuración y permiso
- **Fecha:** 2026-11-03
- **Estado:** Aceptada (respuesta B2)
- **Contexto:** se usan descuentos y el dueño debe poder configurarlos.
- **Decisión:** columna `descuento` (importe) en `detalle_factura` y `detalle_proforma`; tope en `configuracion.descuento_maximo_porcentaje`; solo los roles con el permiso `ventas.aplicar_descuento` pueden aplicarlo.
- **Alternativas descartadas:** descuento solo en la cabecera de la factura (no se sabe qué producto se rebajó).
- **Consecuencias:** `facturas.total_descuento` se guarda al emitir.

### D-020 — Compras como origen del inventario y costo copiado en la venta
- **Fecha:** 2026-11-03
- **Estado:** Aceptada (respuestas C3 y C4)
- **Contexto:** se compran productos a proveedores y hace falta el costo para calcular la ganancia; el sistema viejo tiene costo 0 en todo.
- **Decisión:** `proveedores`, `compras` y `detalle_compra`. Cada compra genera entradas en `movimientos_inventario` y actualiza `productos.precio_compra`. Cada línea vendida copia el costo en `detalle_factura.costo_unitario`.
- **Alternativas descartadas:** calcular la ganancia con el costo actual (si el costo cambia, cambia la ganancia de ventas pasadas).
- **Consecuencias:** la ganancia de cada venta es exacta y no cambia con el tiempo.

### D-021 — El servicio se define en la categoría
- **Fecha:** 2026-11-03
- **Estado:** Aceptada (respuesta C6)
- **Contexto:** los servicios (mantenimiento, diagnóstico) son productos sin stock.
- **Decisión:** `categorias_producto.es_servicio`; los productos de esas categorías no generan movimientos de inventario.
- **Alternativas descartadas:** `es_servicio` en cada producto (un producto podría quedar mal marcado respecto a su categoría).
- **Consecuencias:** reemplaza la propuesta anterior de `productos.es_servicio`.

### D-022 — OEM es la calidad del repuesto, no una marca
- **Fecha:** 2026-11-03
- **Estado:** Aceptada (2026-11-03, respuesta P5)
- **Contexto:** el sistema viejo tiene "OEM" como marca. El usuario explica que OEM indica que el repuesto cumple las especificaciones y la calidad del fabricante original (respuesta C5).
- **Decisión:** la categoría es Repuesto y `productos.calidad_repuesto` indica `original`, `oem` o `generico` (CHECK). La marca es la del fabricante, si se conoce.
- **Alternativas descartadas:** "OEM" como marca (no es un fabricante); categorías "Repuesto OEM" y "Repuesto original" (multiplica categorías).
- **Consecuencias:** se puede filtrar repuestos por calidad sin tocar marcas ni categorías.

### D-023 — Permisos configurables en la base de datos
- **Fecha:** 2026-11-03
- **Estado:** Aceptada (respuesta D3)
- **Contexto:** los permisos deben gestionarse desde el panel administrativo.
- **Decisión:** `permisos` (lista definida por el sistema) y `roles_permisos` (qué rol tiene qué permiso).
- **Alternativas descartadas:** permisos fijos en el código; permisos por usuario (más difícil de mantener; si hiciera falta, se añadiría `usuarios_permisos`).
- **Consecuencias:** el administrador ajusta los roles sin tocar el código.

### D-024 — Archivos con tablas de vínculo por uso
- **Fecha:** 2026-11-03
- **Estado:** Aceptada (2026-11-03, respuesta P6)
- **Contexto:** el sistema viejo guarda imágenes en base64. El usuario propone dos tablas: una con ruta y nombre del archivo, y otra que indique dónde se usa y qué tabla lo usa.
- **Decisión:** se acepta la tabla `archivos` tal como la propone el usuario. Para el uso, en lugar de una tabla genérica (`tabla`, `registro_id`), una FK por uso: `productos_archivos`, `ordenes_archivos` y columnas `*_archivo_id` para PDF y logo.
- **Alternativas descartadas:** tabla genérica `archivos_vinculos(tabla, registro_id)`. Es flexible, pero `registro_id` no puede tener FK: se puede apuntar a un registro que no existe o escribir mal el nombre de la tabla (`"producto"` en vez de `"productos"`). Es el mismo problema que la categoría en texto libre.
- **Consecuencias:** un uso nuevo de archivos (p. ej. fotos de clientes) requiere una tabla de vínculo nueva, pero todas las referencias quedan protegidas por FK.

### D-025 — Autenticación con sesiones y refresh tokens rotativos
- **Fecha:** 2026-11-03
- **Estado:** Aceptada (pedido del usuario en F)
- **Contexto:** el sistema viejo no tiene tablas de autenticación.
- **Decisión:** `sesiones` (una por dispositivo) y `refresh_tokens` (rotación con detección de reutilización); los access tokens no se guardan; bloqueo por intentos fallidos en `usuarios`.
- **Alternativas descartadas:** solo JWT sin tablas (no se puede revocar); un único refresh token por sesión (no detecta robo).
- **Consecuencias:** se puede cerrar sesión en todos los dispositivos y cortar el acceso de un usuario desactivado de inmediato.

### D-026 — Pagos a proveedores como egresos de caja
- **Fecha:** 2026-11-03
- **Estado:** Aceptada (respuesta P1)
- **Contexto:** las compras a distribuidores se pagan desde la caja; no hay cuentas por pagar por ahora.
- **Decisión:** el pago de una compra es un egreso en `movimientos_caja` con `compra_id`, igual que un abono es un ingreso con `factura_id` (D-009). Un `CHECK` impide que un movimiento tenga ambas FK.
- **Alternativas descartadas:** tabla `pagos_proveedores` (el mismo dinero quedaría en dos tablas); tabla `cuentas_por_pagar` (no hay compras a crédito).
- **Consecuencias:** el cuadre de caja incluye los pagos a proveedores. Si en el futuro hay compras a crédito, el saldo de cada compra se calcula como total − egresos enlazados, sin tabla nueva.
