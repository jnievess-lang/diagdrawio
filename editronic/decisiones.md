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
- **Estado:** Propuesta (confirmar con el usuario)
- **Contexto:** el usuario usó `movimiento_inventarios` como ejemplo.
- **Decisión:** tablas y columnas en `snake_case`, sin tildes ni ñ; PK `id`; FK `<tabla_en_singular>_id`.
- **Alternativas descartadas:** `PascalCase` (`DetalleOrden`), que da problemas de mayúsculas en PostgreSQL.
- **Consecuencias:** el modelo de órdenes de prueba (PascalCase) no sigue esta convención; no se reutiliza tal cual.

### D-003 — Importes con `DECIMAL(12,2)`
- **Fecha:** 2026-11-02
- **Estado:** Propuesta (confirmar con el usuario)
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
- **Estado:** Propuesta (validar con el usuario)
- **Contexto:** en el sistema viejo, "Registrar equipo" crea el equipo y la orden a la vez, y desde la orden se "elimina el equipo".
- **Decisión:** `equipos` guarda el aparato (tipo, marca, modelo, serie) y `ordenes_reparacion` cada ingreso al taller (daño, observaciones, estado, fecha).
- **Alternativas descartadas:** una sola tabla, como el sistema viejo (marca, modelo y serie se repiten en cada visita y no hay historial por equipo).
- **Consecuencias:** al registrar una orden se busca primero si el equipo ya existe. Un equipo con órdenes no se borra.

### D-007 — Listas de valores como tablas catálogo
- **Fecha:** 2026-11-02
- **Estado:** Propuesta (validar con el usuario)
- **Contexto:** tipos de equipo, estados de orden y métodos de pago son listas desplegables que pueden crecer.
- **Decisión:** usar tablas catálogo (`tipos_equipo`, `estados_orden`, `metodos_pago`). Para valores que nunca cambiarán (como `ingreso`/`egreso`) basta una restricción `CHECK`.
- **Alternativas descartadas:** `ENUM` de PostgreSQL (añadir o renombrar valores exige cambiar el esquema); texto libre (variantes y errores de escritura).
- **Consecuencias:** más tablas pequeñas, pero los valores se gestionan desde Configuración sin tocar la base de datos.

### D-008 — No almacenar totales calculados
- **Fecha:** 2026-11-02
- **Estado:** Propuesta (validar con el usuario)
- **Contexto:** la pantalla de caja muestra saldo total, totales por método, egresos y saldo acumulado por fila.
- **Decisión:** estos valores se calculan con consultas o vistas a partir de `movimientos_caja` y `sesiones_caja`; no son columnas.
- **Alternativas descartadas:** guardar los totales (se desincronizan si se corrige o anula un movimiento).
- **Consecuencias:** la única cifra de cierre que se guarda es el efectivo contado físicamente, para compararla con la calculada.
- **Excepción propuesta:** los totales de `facturas` se guardan al emitir, porque un documento fiscal emitido no puede cambiar (por validar).

### D-009 — Los abonos son movimientos de caja
- **Fecha:** 2026-11-02
- **Estado:** Propuesta (validar con el usuario)
- **Contexto:** el historial de facturas muestra "Abonado", "Saldo" y un botón "Abonar"; la caja registra ingresos como `Venta FAC-000015 · Transferencia`. Es el mismo dinero visto desde dos pantallas.
- **Decisión:** un abono es un `movimientos_caja` de tipo ingreso con `factura_id`. Abonado = suma de esos movimientos; saldo = total − abonado; estado Pagado/Pendiente = saldo igual a 0 o no. "Crédito" deja de ser método de pago: una venta a crédito es una factura con saldo.
- **Alternativas descartadas:** tabla `abonos` aparte (el mismo pago quedaría en dos tablas y podrían no coincidir).
- **Consecuencias:** no hace falta tabla de cuentas por cobrar. Solo se puede cobrar con caja abierta, también por transferencia (confirmar que el local trabaja así).

### D-010 — Stock calculado desde `movimientos_inventario`
- **Fecha:** 2026-11-02
- **Estado:** Propuesta (validar con el usuario)
- **Contexto:** el stock se edita a mano en el producto y no se sabe por qué cambia.
- **Decisión:** el stock de un producto es la suma de entradas menos salidas en `movimientos_inventario`. Cada venta genera su salida automáticamente.
- **Alternativas descartadas:** columna `stock` editable (sin trazabilidad); columna `stock` más movimientos (dos fuentes que pueden no coincidir).
- **Consecuencias:** el stock inicial al migrar se carga como un movimiento de "ajuste inicial". Si en el futuro la consulta fuera lenta, se puede añadir una columna mantenida por la base de datos sin cambiar el modelo.

### D-011 — Precios por tarifa en tabla aparte
- **Fecha:** 2026-11-02
- **Estado:** Propuesta (validar con el usuario)
- **Contexto:** cada producto tiene tres columnas de precio: Público, Técnico y Mayorista.
- **Decisión:** catálogo `tarifas` y tabla `precios_producto` (producto, tarifa, precio).
- **Alternativas descartadas:** tres columnas en `productos`, válidas solo si las tarifas no cambiarán nunca.
- **Consecuencias:** una tarifa nueva no cambia la estructura. Consultar el precio requiere unir dos tablas.
