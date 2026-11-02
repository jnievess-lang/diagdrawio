# Memoria del proyecto Editronic

Bitácora cronológica: cada cambio, en orden, con su motivo. La entrada más reciente va arriba.

## Estado actual
- **Fase:** levantamiento de entidades del sistema viejo a partir de capturas. **No se modifican los diagramas** hasta que el usuario tenga el panorama completo y valide `entidades.md`.
- **Diagrama Dev:** vacío.
- **Diagrama Producción:** vacío.
- **Entidades propuestas (18):** `clientes`, `equipos`, `tipos_equipo`, `ordenes_reparacion`, `estados_orden`, `sesiones_caja`, `movimientos_caja`, `metodos_pago`, `usuarios` (incompleta), `facturas`, `detalle_factura`, `productos`, `categorias_producto`, `marcas`, `tarifas`, `precios_producto`, `movimientos_inventario`, `envios_correo`.
- **Pendiente:**
  - Recibir más capturas: proformas, cuentas por cobrar, empleados, perfil, configuración, detalle de orden y dashboard (lista en `entidades.md`).
  - Validar D-002, D-003 y D-006 a D-011.
  - Resolver las dudas abiertas de `proyecto.md`.

## Bitácora

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
