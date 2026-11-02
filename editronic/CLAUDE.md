# Reglas del proyecto Editronic (ERD)

Estas reglas son obligatorias para cualquier cambio dentro de `editronic/`.

## Antes de empezar a trabajar
1. Leer `project_memory.md` para saber qué se hizo y qué quedó pendiente.
2. Leer `proyecto.md`, `decisiones.md` y `entidades.md`.
3. No repetir preguntas que ya estén respondidas en esos archivos.

## Después de cada cambio
- Registrar el cambio en `project_memory.md`: fecha, qué cambió y por qué.
- Si el cambio implica una decisión de diseño, añadir una entrada en `decisiones.md`.
- Si cambia una entidad, actualizar su ficha en `entidades.md`.
- Los tres archivos y los `.drawio` deben decir lo mismo. Si no coinciden, avisar antes de seguir.

## Justificación y valoración crítica
- Ninguna entidad entra al diagrama sin justificación en `entidades.md`: qué problema resuelve, qué pasaría si no existiera y qué alternativas se descartaron.
- Ejemplo: si se propone `movimiento_inventarios`, explicar por qué no basta con un campo `stock` en `productos` (trazabilidad, auditoría, historial de entradas y salidas).
- Si una petición me parece incorrecta o arriesgada (redundancia, mala normalización, pérdida de datos), decirlo antes de aplicarla y proponer alternativas.
- No inventar entidades ni atributos que no se hayan pedido o justificado.

## Flujo Dev → Producción
- Todo cambio se hace primero en `ERD-Editronic-Dev.drawio`.
- `ERD-Editronic-Produccion.drawio` solo se actualiza cuando el usuario aprueba explícitamente pasar los cambios a producción.
- Cada paso a producción se registra en `project_memory.md`.

## Estilo de los diagramas
- Figura: la Tabla de la sección "Relación de la entidad" de draw.io (una fila por atributo).
- Color de todas las entidades: relleno `#dae8fc`, borde `#6c8ebf`. No usar otros colores.
- Columna de claves: `PK`, `FK`, `FK1`, `FK2`…; PK en negrita y subrayada.
- Relaciones: notación pata de gallo, ancladas a la fila PK y a la fila FK (nunca líneas sueltas).

## Nombres y tipos de datos
- Tablas y columnas en `snake_case`, en español y sin tildes ni ñ (ejemplo: `movimiento_inventarios`, `fecha_creacion`).
- Clave primaria: `id`. Clave foránea: `<tabla_en_singular>_id` (ejemplo: `producto_id`).
- Motor: PostgreSQL (D-005). Usar sus tipos en el diagrama.
- PK: `BIGINT GENERATED ALWAYS AS IDENTITY`. No usar `SERIAL`.
- Dinero: `NUMERIC(12,2)`. Prohibido `FLOAT`, `REAL` o `MONEY` para importes.
- Fechas: `DATE` o `TIMESTAMPTZ`, nunca texto ni `TIMESTAMP` sin zona horaria.
- Estados o categorías fijas: tabla catálogo o `ENUM` según `decisiones.md`; nunca texto libre.
