# Memoria del proyecto Editronic

Bitácora cronológica: cada cambio, en orden, con su motivo. La entrada más reciente va arriba.

## Estado actual
- **Fase:** levantamiento de entidades del sistema viejo a partir de capturas. **No se modifican los diagramas** hasta que el usuario tenga el panorama completo y valide `entidades.md`.
- **Diagrama Dev:** vacío.
- **Diagrama Producción:** vacío.
- **Entidades propuestas (22):** `clientes`, `equipos`, `tipos_equipo`, `ordenes_reparacion`, `estados_orden`, `sesiones_caja`, `movimientos_caja`, `metodos_pago`, `usuarios`, `roles`, `facturas`, `detalle_factura`, `proformas`, `detalle_proforma`, `productos`, `categorias_producto`, `marcas`, `tarifas`, `precios_producto`, `movimientos_inventario`, `envios_correo`, `configuracion`.
- **Pendiente:**
  - Validación final de `entidades.md` (35 tablas). No quedan preguntas abiertas.
  - Solo después de validar: empezar `ERD-Editronic-Dev.drawio`.

## Bitácora

### 2026-11-03 — Respuestas finales (P1 a P7)
- **Qué:**
  - `movimientos_caja` + `compra_id` para pagar compras desde la caja (D-026).
  - `estados_orden` + "No aprobado": no es final, porque el equipo se devuelve después (Entregado), y deja la garantía en 0.
  - `ordenes_archivos` confirmada.
  - `tokens_recuperacion` y `cuentas_por_pagar` descartadas.
  - D-016, D-022 y D-024 aceptadas.
- **Ajuste a una recomendación:** "No aprobado" se había propuesto como estado final; se corrige porque el equipo todavía debe entregarse al cliente.
- **Diagramas:** sin cambios; esperan la validación final.

### 2026-11-03 — Respuestas del usuario y análisis de la BD vieja
- **Qué:**
  - Se registraron las respuestas A1 a F en `proyecto.md`.
  - Se creó `analisis-bd-vieja.md`, con la estructura de `bd.json` y 32 hallazgos.
  - Se reescribió `entidades.md`: de 22 a 35 tablas.
  - Se aceptaron D-002 a D-014 y se añadieron D-015 a D-025.
  - `CLAUDE.md` tiene nuevas reglas sobre la BD vieja y lo prohibido en el modelo.
- **Tablas nuevas (13):** `tipos_identificacion`, `tipos_iva`, `permisos`, `roles_permisos`, `sesiones`, `refresh_tokens`, `proveedores`, `historial_estados_orden`, `ordenes_archivos`, `productos_archivos`, `compras`, `detalle_compra`, `archivos`; además `estados_orden` cambia a los 6 estados del usuario.
- **Cambios en tablas existentes:**
  - `ordenes_reparacion`: + técnico, diagnóstico, costo estimado, fecha estimada, accesorios, garantía, orden de garantía, PDF; − estado (pasa al historial).
  - `productos`: − `es_servicio` (pasa a la categoría), + `tipo_iva_id`, + `calidad_repuesto`.
  - `detalle_factura`: + `descuento`, + `costo_unitario`.
  - `detalle_proforma`: + `descuento`.
  - `clientes`: + tipo de identificación (catálogo), + tarifa por defecto.
  - `usuarios`: + intentos fallidos y bloqueo.
  - `configuracion`: + IVA predeterminado, + tope de descuento, logo como archivo.
- **Descartadas:** `tokens_recuperacion` (pendiente P4) y `archivos_vinculos` genérica (D-024).
- **Privacidad:** `bd.json` no se sube al repositorio (datos personales).
- **Diagramas:** sin cambios.

### 2026-11-02 — Cierre del levantamiento y dudas consolidadas
- **Qué:** última captura (Login). Se cerró el levantamiento: no hay más capturas. Se reunieron todas las dudas en `proyecto.md`, agrupadas (A servicio técnico, B ventas, C caja e inventario, D clientes y usuarios, E decisiones, F migración), cada una con una recomendación.
- **Por qué:** el usuario pidió la lista completa de dudas para responderlas de una vez.
- **Resuelto:** no hay registro público; las cuentas las crea el administrador. Usuario y correo deben ser únicos.
- **Diagramas:** sin cambios.

### 2026-11-02 — Proformas, cuentas por cobrar, empleados y configuración
- **Qué:** con 4 capturas más se añadieron `roles`, `proformas`, `detalle_proforma` y `configuracion`; se completó `usuarios` y se añadió `proforma_id` a `facturas`.
- **Resuelto:** cuentas por cobrar no necesita tabla (la pantalla confirma D-009); empleados y usuarios son la misma tabla; roles: Administrador, Técnico, Secretario/a; local en Quevedo, Ecuador.
- **Hallazgos:** 5 nuevos (14 a 18), entre ellos el administrador guardado aparte, el RUC vacío y el botón "Restablecer datos de prueba".
- **Decisiones:** D-012 (configuración de una fila), D-013 (proformas separadas de facturas), D-014 (usuarios = empleados).
- **Diagramas:** sin cambios.

### 2026-11-02 — Entidades de ventas, facturas e inventario
- **Qué:** con 5 capturas más (Ventas, Facturas, Productos, Inventario, Inventario de equipos) se añadieron 8 entidades: `facturas` (completa), `detalle_factura`, `productos`, `categorias_producto`, `marcas`, `tarifas`, `precios_producto`, `movimientos_inventario` y `envios_correo`. `equipos` pasa a usar el catálogo `marcas`; `estados_orden` recibe la columna `es_final`.
- **Hallazgos:** 8 nuevos (6 a 13), entre ellos servicios con stock, "Crédito" usado como forma de pago, facturas que se eliminan y stock editado a mano.
- **Resuelto:** "Inventario de equipos" es una vista de órdenes, no una tabla. Cuentas por cobrar se cubre con facturas y abonos (por confirmar).
- **Decisiones:** D-009 (abonos como movimientos de caja), D-010 (stock calculado), D-011 (precios por tarifa); excepción a D-008 para los totales de factura.
- **Diagramas:** sin cambios.

### 2026-11-02 — Primeras entidades desde capturas del sistema viejo
- **Qué:** se documentaron 10 entidades propuestas en `entidades.md` a partir de 5 capturas (Caja, Movimientos de caja, Clientes, Registrar equipo y Órdenes ingresadas), junto con 5 hallazgos críticos del sistema viejo.
- **Por qué:** el usuario pidió extraer las entidades antes de diagramar, para tener un panorama completo y validarlo primero.
- **Decisiones:** D-006 (separar equipos y órdenes), D-007 (tablas catálogo) y D-008 (no guardar totales calculados), todas propuestas.
- **Diagramas:** sin cambios, por indicación del usuario.

### 2026-11-02 — Definición del proyecto
- **Qué:** se completó `proyecto.md` con la descripción del negocio (servicio técnico y venta de tecnología), los módulos y el contexto del sistema viejo.
- **Por qué:** el usuario explicó qué es Editronic; el objetivo es una base de datos nueva y normalizada, sin las tablas innecesarias del sistema viejo.
- **Decisiones:** D-005 (PostgreSQL y sus tipos de datos).

### 2026-11-02 — Creación de la estructura
- **Qué:** se crearon `CLAUDE.md`, `project_memory.md`, `proyecto.md`, `decisiones.md`, `entidades.md`, `ERD-Editronic-Dev.drawio` y `ERD-Editronic-Produccion.drawio` en la rama `feat/UML-ERD-Editronic`.
- **Por qué:** llevar un flujo ordenado en el que cada cambio quede registrado y justificado.
- **Decisiones:** D-001 a D-004 (ver `decisiones.md`).
