# Memoria del proyecto Editronic

Bitácora cronológica: cada cambio, en orden, con su motivo. La entrada más reciente va arriba.

## Estado actual
- **Fase:** levantamiento de entidades del sistema viejo a partir de capturas. **No se modifican los diagramas** hasta que el usuario tenga el panorama completo y valide `entidades.md`.
- **Diagrama Dev:** vacío.
- **Diagrama Producción:** vacío.
- **Entidades propuestas (10):** `clientes`, `equipos`, `tipos_equipo`, `ordenes_reparacion`, `estados_orden`, `sesiones_caja`, `movimientos_caja`, `metodos_pago`, `usuarios` (incompleta), `facturas` (pendiente de captura).
- **Pendiente:**
  - Recibir más capturas: ventas y facturación, inventario, proformas, cuentas por cobrar, empleados y configuración (lista en `entidades.md`).
  - Validar D-002, D-003, D-006, D-007 y D-008.
  - Resolver las dudas abiertas de `proyecto.md`.

## Bitácora

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
