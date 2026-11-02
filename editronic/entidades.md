# Entidades de Editronic

Ficha de cada entidad del modelo. Una entidad sin ficha completa no entra al diagrama (ver D-004).

## Resumen

| Entidad | Estado | En Dev | En Producción |
|---|---|---|---|
| — | — | — | — |

## Plantilla de ficha

```
## nombre_tabla
- **Estado:** Propuesta | Aprobada | Eliminada
- **Propósito:** qué representa.
- **Justificación:** qué problema resuelve y qué pasaría si no existiera.
- **Alternativas descartadas:** p. ej. resolverlo con un campo en otra tabla, y por qué no.
- **Valoración crítica:** riesgos, dudas o costes de esta entidad.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| id | BIGINT | PK | No | Identificador |

**Relaciones:**
- `otra_tabla` 1 → N `nombre_tabla` mediante `otra_tabla_id`.

**Historial:**
- AAAA-MM-DD: creada / cambio realizado y motivo.
```

---

(Aún no hay entidades.)
