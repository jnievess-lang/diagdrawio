# Reglas del proyecto Editronic (ERD)

Estas reglas son obligatorias para cualquier cambio dentro de `editronic/`.

## Antes de empezar a trabajar
1. Leer `project_memory.md` para saber qué se hizo y qué quedó pendiente.
2. Leer `proyecto.md`, `decisiones.md`, `entidades.md` y `analisis-bd-vieja.md`.
3. No repetir preguntas que ya estén respondidas en esos archivos.

## Después de cada cambio
- Registrar el cambio en `project_memory.md`: fecha, qué cambió y por qué.
- Si el cambio implica una decisión de diseño, añadir una entrada en `decisiones.md`.
- Si cambia una entidad, actualizar su ficha en `entidades.md`.
- Los tres archivos y los `.drawio` deben decir lo mismo. Si no coinciden, avisar antes de seguir.

## Justificación y valoración crítica
- Ninguna entidad entra al diagrama sin justificación en `entidades.md`: qué problema resuelve, qué pasaría si no existiera y qué alternativas se descartaron.
- Ejemplo: si se propone `movimiento_inventarios`, explicar por qué no basta con un campo `stock` en `tbproductos` (trazabilidad, auditoría, historial de entradas y salidas).
- Si una petición me parece incorrecta o arriesgada (redundancia, mala normalización, pérdida de datos), decirlo antes de aplicarla y proponer alternativas.
- No inventar entidades ni atributos que no se hayan pedido o justificado.

## La BD vieja
- La BD vieja (`analisis-bd-vieja.md`) es **solo una guía** para entender el negocio, nunca un modelo a copiar.
- Las respuestas del usuario (`proyecto.md`) tienen **prioridad** sobre la BD vieja.
- La migración de datos la hace el usuario: no condicionar el diseño a la BD vieja ni proponer columnas solo para facilitar la migración.
- `bd.json` contiene datos personales de clientes: nunca subirlo al repositorio.

## Prohibido en el modelo
- Texto libre para valores de una lista: siempre tabla catálogo con FK.
- JSON o arrays para datos relacionales (líneas de factura, pagos, permisos).
- Archivos en base64 o binario en la BD: solo nombre, ruta y metadatos en `tbarchivos`; el archivo vive en el backend o en un servicio externo.
- Referencias genéricas sin FK (`tabla`, `registro_id`).
- Fechas como texto.
- Datos de otra tabla copiados (nombre, cédula del cliente…), salvo copias intencionales del momento de la venta (precio, IVA, costo), justificadas en su ficha.

## Flujo Dev → Producción
- Todo cambio se hace primero en `ERD-Editronic-Dev.drawio`.
- `ERD-Editronic-Produccion.drawio` solo se actualiza cuando el usuario aprueba explícitamente pasar los cambios a producción.
- Cada paso a producción se registra en `project_memory.md`.

## Estilo de los diagramas
- Figura: la Tabla de la sección "Relación de la entidad" de draw.io (una fila por atributo).
- Color de todas las entidades: relleno `#dae8fc`, borde `#6c8ebf`. No usar otros colores.
- Cuatro columnas por fila: clave (`PK`, `FK`, `UQ` o combinadas como `PK,FK`), nombre, tipo de PostgreSQL y `NULL` si admite nulos (vacío = NOT NULL). La PK va en negrita y subrayada. Sin descripción: eso queda en `entidades.md`.
- Relaciones: pata de gallo, ancladas a la fila PK y a la fila FK (nunca líneas sueltas), con la cardinalidad escrita en cada extremo (`1`, `0..1`, `1..N`, `0..N`).
- Líneas ortogonales que van por los huecos entre columnas o por carriles encima de las tablas; nunca atraviesan una tabla. Cada relación sale de su propio punto de la fila PK.
- Tablas de otro módulo (referencia): con todos sus atributos y borde discontinuo, para indicar que su hoja principal es la de su módulo.
- Sin recuadro de leyenda en las hojas.
- Todas las hojas: etiquetas de cardinalidad encima de su línea, sin tapar símbolos ni bordes; 28 px entre salidas de una misma PK y 70 px libres junto a las tablas antes del primer cruce.
- Hojas de `ERD-Editronic-Dev.drawio`: 0 Diagrama completo (todas las tablas, en columnas por dependencia) y una por módulo (1 Seguridad, 2 Clientes y servicio técnico, 3 Productos, inventario y compras, 4 Ventas y caja, 5 Archivos, correo y configuración).
- Todas las hojas se generan desde `entidades.md` con `herramientas/generar_erd.py`, para que el diagrama y el documento digan lo mismo. Cambiar primero `entidades.md` y volver a generar.

## Nombres y tipos de datos
- Tablas: prefijo `tb` y nombre en minúsculas sin guiones bajos, en español y sin tildes ni ñ (ejemplo: `tbdetalleproforma`, `tbmovimientosinventario`) (D-028).
- Columnas en `snake_case` (ejemplo: `fecha_creacion`).
- Clave primaria: `<tabla_en_singular>_id` (ejemplo: `detalle_proforma_id` en `tbdetalleproforma`). Clave foránea: el mismo nombre que la PK a la que apunta (ejemplo: `producto_id`), salvo cuando el rol lo exige (`tecnico_id`, `usuario_apertura_id`) (D-028).
- Motor: PostgreSQL (D-005). Usar sus tipos en el diagrama.
- PK: `BIGINT GENERATED ALWAYS AS IDENTITY`. No usar `SERIAL`.
- Dinero: `NUMERIC(12,2)`. Prohibido `FLOAT`, `REAL` o `MONEY` para importes.
- Fechas: `DATE` o `TIMESTAMPTZ`, nunca texto ni `TIMESTAMP` sin zona horaria.
- Estados o categorías fijas: tabla catálogo o `ENUM` según `decisiones.md`; nunca texto libre.
