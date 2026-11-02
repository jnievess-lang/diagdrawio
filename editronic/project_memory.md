# Memoria del proyecto Editronic

Bitácora cronológica: cada cambio, en orden, con su motivo. La entrada más reciente va arriba.

## Estado actual
- **Fase:** alcance definido; esperando las primeras tablas del usuario.
- **Diagrama Dev:** vacío.
- **Diagrama Producción:** vacío.
- **Pendiente:**
  - Recibir las primeras tablas (basadas en lo que el usuario conoce del sistema viejo) y analizarlas una a una.
  - Resolver las dudas abiertas de `proyecto.md` (inventario de equipos, facturación electrónica, roles).
  - Confirmar D-002 (nombres) y D-003 (importes).

## Bitácora

### 2026-11-02 — Definición del proyecto
- **Qué:** se completó `proyecto.md` con la descripción del negocio (servicio técnico y venta de tecnología), los módulos y el contexto del sistema viejo.
- **Por qué:** el usuario explicó qué es Editronic; el objetivo es una base de datos nueva y normalizada, sin las tablas innecesarias del sistema viejo.
- **Decisiones:** D-005 (PostgreSQL y sus tipos de datos).

### 2026-11-02 — Creación de la estructura
- **Qué:** se crearon `CLAUDE.md`, `project_memory.md`, `proyecto.md`, `decisiones.md`, `entidades.md`, `ERD-Editronic-Dev.drawio` y `ERD-Editronic-Produccion.drawio` en la rama `feat/UML-ERD-Editronic`.
- **Por qué:** llevar un flujo ordenado en el que cada cambio quede registrado y justificado.
- **Decisiones:** D-001 a D-004 (ver `decisiones.md`).
