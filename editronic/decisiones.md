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
