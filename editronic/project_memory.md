# Memoria del proyecto Editronic

Bitácora cronológica: cada cambio, en orden, con su motivo. La entrada más reciente va arriba.

## Estado actual
- **Fase:** levantamiento de entidades del sistema viejo a partir de capturas. **No se modifican los diagramas** hasta que el usuario tenga el panorama completo y valide `entidades.md`.
- **Diagrama Dev:** vacío.
- **Diagrama Producción:** vacío.
- **Entidades propuestas (22):** `clientes`, `equipos`, `tipos_equipo`, `ordenes_reparacion`, `estados_orden`, `sesiones_caja`, `movimientos_caja`, `metodos_pago`, `usuarios`, `roles`, `facturas`, `detalle_factura`, `proformas`, `detalle_proforma`, `productos`, `categorias_producto`, `marcas`, `tarifas`, `precios_producto`, `movimientos_inventario`, `envios_correo`, `configuracion`.
- **Pendiente:**
  - Recibir las últimas capturas: detalle o edición de una orden, Dashboard y Perfil.
  - Validar D-002, D-003 y D-006 a D-014.
  - Resolver las dudas abiertas de `proyecto.md`.

## Bitácora

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
