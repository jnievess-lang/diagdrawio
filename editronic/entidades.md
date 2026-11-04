# Entidades de Editronic

Ficha de cada entidad del modelo. Una entidad sin ficha completa no entra al diagrama (D-004).

**Fase actual:** modelo aprobado por el usuario y publicado en `ERD-Editronic-Produccion.drawio` (versión 1, 2026-11-04).

**Fuentes:** respuestas del usuario (prioridad máxima), 15 capturas y `bd.json`. Los hallazgos de la BD vieja están en `analisis-bd-vieja.md`.

**Convenciones de las tablas de columnas:**
- `IDENTITY` = `BIGINT GENERATED ALWAYS AS IDENTITY`.
- **Clave:** PK, FK, UQ (único).
- **Nulo:** Sí o No.

## Resumen (35 tablas)

| Grupo | Tablas |
|---|---|
| Catálogos | `tbtiposidentificacion`, `tbtiposiva`, `tbmetodospago`, `tbmarcas`, `tbcategoriasproducto`, `tbtarifas`, `tbtiposequipo`, `tbestadosorden` |
| Seguridad | `tbusuarios`, `tbroles`, `tbpermisos`, `tbrolespermisos`, `tbsesiones`, `tbrefreshtokens` |
| Clientes y proveedores | `tbclientes`, `tbproveedores` |
| Servicio técnico | `tbequipos`, `tbordenesreparacion`, `tbhistorialestadosorden`, `tbordenesarchivos` |
| Productos e inventario | `tbproductos`, `tbpreciosproducto`, `tbproductosarchivos`, `tbmovimientosinventario`, `tbcompras`, `tbdetallecompra` |
| Ventas | `tbproformas`, `tbdetalleproforma`, `tbfacturas`, `tbdetallefactura` |
| Caja | `tbsesionescaja`, `tbmovimientoscaja` |
| Archivos y correo | `tbarchivos`, `tbenvioscorreo` |
| Configuración | `tbconfiguracion` |

## Entidades descartadas
No se crean, aunque exista una pantalla o una idea para ellas. Se dejan aquí para no volver a discutirlas.

| Entidad | Motivo |
|---|---|
| `empleados` | Son los registros de `tbusuarios` (D-014) |
| `cuentas_por_cobrar` | Son las facturas con saldo (D-009) |
| `abonos` | Son los `tbmovimientoscaja` con `factura_id` (D-009) |
| `inventario_equipos` | Es una consulta sobre órdenes y equipos |
| `cajas` | Hay una sola caja (respuesta C1) |
| `documentos` (proforma + factura juntas) | Ciclos de vida distintos (D-013) |
| `archivos_vinculos` (tabla + id genérico) | Sin FK reales; se usan tablas de vínculo por uso (D-024) |
| `tokens_recuperacion` | No hay "olvidé mi contraseña" por ahora; el administrador restablece las contraseñas (respuesta P4) |
| `cuentas_por_pagar` | Las compras se pagan desde la caja; no hay compras a crédito por ahora (respuesta P1) |

---

# Catálogos

## tbtiposidentificacion
- **Propósito:** tipos de documento de clientes y proveedores: Cédula, RUC, Pasaporte, Consumidor final.
- **Justificación:** el sistema viejo mezcla cédula y RUC en un campo, y la venta a consumidor final exige identificarlo (respuesta D2).
- **Alternativas descartadas:** `VARCHAR` con texto libre (repite el problema de las categorías).
- **Valoración crítica:** `codigo_sri` queda nulo mientras las facturas sean internas; si se pasa al SRI, ya está la columna (respuesta B1).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| tipo_identificacion_id | IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(30) | UQ | No | Cédula, RUC, Pasaporte, Consumidor final |
| codigo_sri | VARCHAR(2) | | Sí | Código oficial, para el futuro |
| activo | BOOLEAN | | No | Si aparece en la lista |

## tbtiposiva
- **Propósito:** tarifas de IVA aplicables a los productos (0 %, 15 %…).
- **Justificación:** hay productos con IVA 0 % (respuesta B3), y la tarifa general ya cambió en Ecuador; con un catálogo, un cambio de IVA es un registro nuevo.
- **Alternativas descartadas:** `porcentaje_iva` numérico en cada producto (un cambio de tarifa obliga a editar todos los productos).
- **Valoración crítica:** el detalle de factura y de proforma sigue copiando el porcentaje al vender, para que las facturas antiguas no cambien.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| tipo_iva_id | IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(30) | UQ | No | IVA 0 %, IVA 15 % |
| porcentaje | NUMERIC(5,2) | | No | 0.00, 15.00 |
| codigo_sri | VARCHAR(4) | | Sí | Código oficial, para el futuro |
| activo | BOOLEAN | | No | Si se puede asignar |

## tbmetodospago
- **Propósito:** Efectivo, Transferencia, Tarjeta.
- **Justificación:** caja y abonos se agrupan por método. "Crédito" no es un método: es una factura con saldo (D-009).
- **Alternativas descartadas:** texto libre o `ENUM` (D-007).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| metodo_pago_id | IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(40) | UQ | No | Efectivo, Transferencia, Tarjeta |
| activo | BOOLEAN | | No | Si aparece en la lista |

## tbmarcas
- **Propósito:** marcas de productos y de equipos de clientes.
- **Justificación:** el sistema viejo tiene `HP`/`Hp`/`hp`, `xiomi`, `GENIUS NEGRO`, `PM-02`… (hallazgo 2). Una sola lista sirve a productos y equipos.
- **Alternativas descartadas:** un catálogo por uso (la misma lista repetida).
- **Valoración crítica:** "OEM" no es una marca (D-022). El color y el modelo no van aquí: van en el nombre del producto o en el modelo del equipo.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| marca_id | IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(60) | UQ | No | HP, Lenovo, Sony, Genius… |
| activo | BOOLEAN | | No | Si aparece en la lista |

## tbcategoriasproducto
- **Propósito:** Accesorio, Repuesto, Laptop, Cargador, Servicio…
- **Justificación:** 14 variantes de texto en 87 productos (hallazgo 1). Además, la categoría decide si el producto lleva stock (respuesta C6).
- **Alternativas descartadas:**
  - Texto libre (el problema actual).
  - `es_servicio` en cada producto: la respuesta C6 lo pone en la categoría, así un servicio nunca queda mal marcado.
- **Valoración crítica:** si una categoría de servicio pasa a tener stock, todos sus productos cambian a la vez; es el comportamiento deseado.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| categoria_producto_id | IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(60) | UQ | No | Accesorio, Repuesto, Servicio… |
| es_servicio | BOOLEAN | | No | Sus productos no llevan stock |
| activo | BOOLEAN | | No | Si aparece en la lista |

## tbtarifas
- **Propósito:** tipos de precio: Público, Técnico, Mayorista.
- **Justificación:** las tarifas son configurables (respuesta B5) y cada cliente tiene una por defecto (respuesta B4).
- **Alternativas descartadas:** tres columnas de precio en `tbproductos` (D-011).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| tarifa_id | IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(40) | UQ | No | Público, Técnico, Mayorista |
| es_predeterminada | BOOLEAN | | No | La que usan proformas y clientes nuevos (Público) |
| activo | BOOLEAN | | No | Si aparece en la lista |

## tbtiposequipo
- **Propósito:** Laptop, Computadora, PlayStation, Xbox, Impresora, Mando, Tarjeta gráfica…
- **Justificación:** sustituye "Otro" + texto libre (hallazgo 4). La garantía es configurable por tipo (respuesta A7).
- **Alternativas descartadas:**
  - Garantía fija en las cláusulas: la respuesta A7 pide que dependa del tipo.
  - Garantía escrita a mano en cada orden: así queda en 0 días en 26 de 27 equipos (hallazgo 25).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| tipo_equipo_id | IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(60) | UQ | No | Laptop, PlayStation… |
| dias_garantia | SMALLINT | | No | Garantía por defecto (p. ej. 90) |
| activo | BOOLEAN | | No | Si aparece en la lista |

## tbestadosorden
- **Propósito:** Recibido, En diagnóstico, Esperando aprobación, No aprobado, En reparación, Reparado, Entregado (respuesta A2 más "No aprobado", respuesta P2).
- **Justificación:** filtros e indicadores de órdenes, e historial de estados.
- **Alternativas descartadas:** texto libre o `ENUM` (D-007).
- **Valoración crítica:**
  - **"No aprobado"** (respuesta P2): el cliente rechaza el presupuesto y se cobra solo el diagnóstico. **No es estado final**, porque el equipo aún debe devolverse: después pasa a "Entregado". Esto ajusta la recomendación inicial, que lo proponía como final.
  - **Garantía:** una orden que pasó por "No aprobado" no tiene garantía (no se reparó nada); al registrar ese estado, `tbordenesreparacion.dias_garantia` pasa a 0.
  - Flujos posibles: Recibido → En diagnóstico → Esperando aprobación → En reparación → Reparado → Entregado; o bien Esperando aprobación → No aprobado → Entregado.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| estado_orden_id | IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(40) | UQ | No | Recibido … Entregado |
| orden | SMALLINT | UQ | No | Posición en listas (1 a 7) |
| es_final | BOOLEAN | | No | Cierra la orden (Entregado) |
| inicia_garantia | BOOLEAN | | No | La garantía empieza en este estado (Entregado) |

---

# Seguridad

## tbusuarios
- **Propósito:** empleados que inician sesión.
- **Justificación:** toda operación registra quién la hizo. El login usa usuario o correo (captura 15).
- **Alternativas descartadas:** `empleados` aparte, o administrador aparte (D-014).
- **Valoración crítica:**
  - Usuario y correo únicos (el correo puede faltar; respuesta D4).
  - Contraseña siempre como hash.
  - `intentos_fallidos` y `bloqueado_hasta` frenan ataques de fuerza bruta en el login. Son estado del usuario, no historial.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| usuario_id | IDENTITY | PK | No | Identificador |
| nombre_completo | VARCHAR(150) | | No | Nombre del empleado |
| nombre_usuario | VARCHAR(50) | UQ | No | Usuario de acceso |
| correo | VARCHAR(150) | UQ | Sí | Correo, también para iniciar sesión |
| hash_contrasena | VARCHAR(255) | | No | Contraseña cifrada |
| rol_id | BIGINT | FK | No | Rol |
| intentos_fallidos | SMALLINT | | No | Intentos fallidos seguidos |
| bloqueado_hasta | TIMESTAMPTZ | | Sí | Bloqueo temporal tras varios intentos |
| activo | BOOLEAN | | No | Si puede iniciar sesión |
| fecha_creacion | TIMESTAMPTZ | | No | Alta |

## tbroles
- **Propósito:** Administrador, Técnico, Secretario/a.
- **Justificación:** agrupa permisos (respuesta D3).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| rol_id | IDENTITY | PK | No | Identificador |
| nombre | VARCHAR(40) | UQ | No | Administrador, Técnico, Secretario/a |
| descripcion | VARCHAR(200) | | Sí | Para qué sirve el rol |

## tbpermisos
- **Propósito:** acciones que se pueden permitir o negar: `tbfacturas.anular`, `ventas.aplicar_descuento`, `caja.cerrar`…
- **Justificación:** los permisos se gestionan en la BD desde el panel administrativo (respuesta D3).
- **Alternativas descartadas:** permisos fijos en el código (lo que pide evitar la respuesta D3).
- **Valoración crítica:** la lista de permisos la define el sistema (cada permiso corresponde a una acción programada). El administrador decide qué rol tiene cuál, pero no inventa permisos nuevos.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| permiso_id | IDENTITY | PK | No | Identificador |
| codigo | VARCHAR(80) | UQ | No | `modulo.accion`, p. ej. `tbfacturas.anular` |
| modulo | VARCHAR(40) | | No | Caja, Ventas, Inventario… |
| descripcion | VARCHAR(200) | | No | Texto que ve el administrador |

## tbrolespermisos
- **Propósito:** qué permisos tiene cada rol.
- **Justificación:** relación N a N entre `tbroles` y `tbpermisos`.
- **Alternativas descartadas:** lista de permisos en texto o JSON dentro del rol (sin integridad; hallazgo 10).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| rol_id | BIGINT | PK, FK | No | Rol |
| permiso_id | BIGINT | PK, FK | No | Permiso |

## tbsesiones
- **Propósito:** cada inicio de sesión en un dispositivo.
- **Justificación:** no existe nada de autenticación en el sistema viejo (hallazgo 26). Permite ver dónde está conectado un usuario, cerrar una sesión concreta o todas, y cortar el acceso de un usuario desactivado.
- **Alternativas descartadas:** sesión solo en el token, sin tabla: no se puede revocar antes de que expire.
- **Valoración crítica:** los access tokens (JWT de corta duración) **no** se guardan; solo la sesión y sus refresh tokens.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| sesion_id | IDENTITY | PK | No | Identificador |
| usuario_id | BIGINT | FK | No | Usuario |
| fecha_inicio | TIMESTAMPTZ | | No | Inicio de sesión |
| ultima_actividad | TIMESTAMPTZ | | No | Último uso |
| ip | INET | | Sí | Dirección IP |
| user_agent | VARCHAR(300) | | Sí | Navegador o dispositivo |
| expira_en | TIMESTAMPTZ | | No | Caducidad absoluta |
| revocada_en | TIMESTAMPTZ | | Sí | Cierre de sesión o revocación |

## tbrefreshtokens
- **Propósito:** tokens para renovar el acceso, con rotación: cada uso emite uno nuevo y marca el anterior como usado.
- **Justificación:** si alguien reutiliza un token ya usado (señal de robo), se detecta y se revoca toda la sesión. Para eso hay que conservar los tokens anteriores.
- **Alternativas descartadas:** guardar el refresh token en `tbsesiones` (solo el último; no permite detectar la reutilización).
- **Valoración crítica:** se guarda el **hash** del token, nunca el token. Se pueden purgar los tokens expirados periódicamente.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| refresh_token_id | IDENTITY | PK | No | Identificador |
| sesion_id | BIGINT | FK | No | Sesión a la que pertenece |
| hash_token | CHAR(64) | UQ | No | SHA-256 del token |
| emitido_en | TIMESTAMPTZ | | No | Emisión |
| expira_en | TIMESTAMPTZ | | No | Caducidad |
| usado_en | TIMESTAMPTZ | | Sí | Cuándo se rotó |
| reemplazado_por_id | BIGINT | FK | Sí | Token que lo sustituyó |
| revocado_en | TIMESTAMPTZ | | Sí | Revocación |

---

# Clientes y proveedores

## tbclientes
- **Propósito:** personas y empresas a las que se vende o se repara (respuesta F).
- **Justificación:** facturas, órdenes, proformas y cuentas por cobrar.
- **Alternativas descartadas:** datos del cliente copiados en cada documento (hallazgo 12).
- **Valoración crítica:**
  - `razon_social` sirve para personas y empresas (respuesta D1).
  - "Consumidor final" es un cliente más, con su tipo de identificación (respuesta D2).
  - `tarifa_id` es la tarifa por defecto; se puede cambiar en cada venta (respuesta B4).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| cliente_id | IDENTITY | PK | No | Identificador |
| tipo_identificacion_id | BIGINT | FK | No | Cédula, RUC, Pasaporte, Consumidor final |
| identificacion | VARCHAR(20) | UQ | No | Número |
| razon_social | VARCHAR(200) | | No | Nombre o razón social |
| telefono | VARCHAR(20) | | Sí | Teléfono |
| correo | VARCHAR(150) | | Sí | Para enviar facturas y órdenes |
| direccion | VARCHAR(250) | | Sí | Dirección |
| tarifa_id | BIGINT | FK | No | Tarifa por defecto |
| activo | BOOLEAN | | No | Borrado lógico |
| fecha_creacion | TIMESTAMPTZ | | No | Alta |

## tbproveedores
- **Propósito:** a quién se compra mercadería y repuestos.
- **Justificación:** se registran las compras a proveedores (respuesta C3).
- **Alternativas descartadas:** reutilizar `tbclientes` con un indicador de "es proveedor". Comparten campos, pero mezclar ambos enreda las búsquedas de ventas y los permisos.
- **Valoración crítica:** si un proveedor también compra en el local, quedará en ambas tablas; es poco frecuente y aceptable.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| proveedor_id | IDENTITY | PK | No | Identificador |
| tipo_identificacion_id | BIGINT | FK | No | RUC, Cédula… |
| identificacion | VARCHAR(20) | UQ | No | Número |
| razon_social | VARCHAR(200) | | No | Nombre |
| telefono | VARCHAR(20) | | Sí | Teléfono |
| correo | VARCHAR(150) | | Sí | Correo |
| direccion | VARCHAR(250) | | Sí | Dirección |
| activo | BOOLEAN | | No | Borrado lógico |

---

# Servicio técnico

## tbequipos
- **Propósito:** cada aparato físico.
- **Justificación:** un equipo vuelve a reparación o por garantía; se registra una vez (D-006).
- **Valoración crítica:**
  - `cliente_id` es el **propietario**. Quien lo trae a una orden concreta va en la orden (D-017).
  - La serie puede faltar (mandos), así que no es única obligatoria.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| equipo_id | IDENTITY | PK | No | Identificador |
| cliente_id | BIGINT | FK | No | Propietario |
| tipo_equipo_id | BIGINT | FK | No | Tipo |
| marca_id | BIGINT | FK | Sí | Marca |
| modelo | VARCHAR(120) | | Sí | Modelo |
| serie | VARCHAR(80) | | Sí | Número de serie |
| fecha_creacion | TIMESTAMPTZ | | No | Alta |

## tbordenesreparacion
- **Propósito:** cada ingreso de un equipo al taller.
- **Justificación:** documento central del servicio técnico.
- **Valoración crítica:**
  - **Clientes:** `cliente_id` es quien trae el equipo y responde por la orden (respuesta A1). La factura puede ir a otro cliente (D-017).
  - **Técnico** asignado (respuesta A4); puede estar vacío hasta asignarlo. Que el usuario tenga rol Técnico se valida en la aplicación.
  - **Diagnóstico, costo estimado, fecha estimada de entrega y accesorios** (respuesta A5). Los accesorios son texto ("cargador, funda"); no se consultan por separado, así que no merecen tabla.
  - **El estado actual no es columna:** es el último registro de `tbhistorialestadosorden` (D-016). Lo mismo para las fechas de reparación y de entrega.
  - **Garantía:** `dias_garantia` se copia del tipo de equipo al crear la orden, para que cambiar la configuración no altere las garantías ya dadas. Fin de garantía = fecha del estado Entregado + `dias_garantia` (D-015).
  - **Orden de garantía:** `orden_garantia_id` enlaza con la orden original (respuesta A7).
  - **Diagnóstico cobrado:** el diagnóstico se factura como un producto de categoría Servicio (respuesta A6). Una orden tiene una factura como máximo (respuesta A8).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| orden_reparacion_id | IDENTITY | PK | No | Identificador |
| numero | VARCHAR(20) | UQ | No | `OR-000029` |
| equipo_id | BIGINT | FK | No | Equipo |
| cliente_id | BIGINT | FK | No | Quien trae el equipo |
| tecnico_id | BIGINT | FK | Sí | Técnico asignado (`tbusuarios`) |
| dano_reportado | TEXT | | No | Falla que indica el cliente |
| accesorios | VARCHAR(250) | | Sí | Accesorios recibidos |
| observaciones | TEXT | | Sí | Estado físico y notas |
| diagnostico | TEXT | | Sí | Diagnóstico técnico |
| costo_estimado | NUMERIC(12,2) | | Sí | Presupuesto para el cliente |
| fecha_ingreso | TIMESTAMPTZ | | No | Recepción |
| fecha_entrega_estimada | DATE | | Sí | Fecha prometida |
| dias_garantia | SMALLINT | | No | Copiado del tipo de equipo |
| orden_garantia_id | BIGINT | FK | Sí | Orden original, si es por garantía |
| pdf_ingreso_archivo_id | BIGINT | FK | Sí | PDF de la orden de ingreso |
| usuario_id | BIGINT | FK | No | Quién la registró |

## tbhistorialestadosorden
- **Propósito:** cada cambio de estado de una orden: cuál, cuándo y quién.
- **Justificación:** respuesta A3. El sistema viejo solo guarda el estado actual (hallazgo 23). Además da las fechas de reparación y de entrega, y el inicio de la garantía.
- **Alternativas descartadas:** columnas `fecha_reparado`, `fecha_entregado`… (una por estado; si se añade un estado, hay que añadir una columna).
- **Valoración crítica:** al crear la orden se inserta el primer registro ("Recibido").

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| historial_estado_orden_id | IDENTITY | PK | No | Identificador |
| orden_reparacion_id | BIGINT | FK | No | Orden |
| estado_orden_id | BIGINT | FK | No | Nuevo estado |
| fecha_hora | TIMESTAMPTZ | | No | Cuándo |
| usuario_id | BIGINT | FK | No | Quién |
| observacion | VARCHAR(250) | | Sí | Motivo o nota |

## tbordenesarchivos
- **Estado:** Propuesta (confirmada por el usuario, respuesta P3)
- **Propósito:** fotos del equipo al recibirlo.
- **Justificación:** las cláusulas excluyen de la garantía los golpes, caídas y humedad. Una foto al recibir el equipo prueba su estado en caso de reclamo.
- **Alternativas descartadas:** fotos en base64 en la orden (hallazgo 9).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| orden_reparacion_id | BIGINT | PK, FK | No | Orden |
| archivo_id | BIGINT | PK, FK | No | Foto |
| descripcion | VARCHAR(150) | | Sí | "Golpe en esquina", "pantalla rota"… |

---

# Productos e inventario

## tbproductos
- **Propósito:** lo que se vende: productos físicos y servicios.
- **Justificación:** ventas, proformas, compras e inventario.
- **Valoración crítica:**
  - Si lleva stock o no lo decide la categoría (`tbcategoriasproducto.es_servicio`; respuesta C6).
  - El IVA viene de `tbtiposiva` (respuesta B3).
  - `precio_compra` es el **costo actual**: se actualiza al registrar una compra y es editable (respuesta C4). Para calcular la ganancia se copia en cada línea vendida (D-020).
  - `calidad_repuesto` (Original, OEM, Genérico) aplica solo a repuestos (D-022, respuesta P5).
  - El stock se calcula desde `tbmovimientosinventario` (D-010); `stock_minimo` es un parámetro.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| producto_id | IDENTITY | PK | No | Identificador |
| codigo | VARCHAR(30) | UQ | No | `A0071` |
| nombre | VARCHAR(200) | | No | Nombre |
| categoria_producto_id | BIGINT | FK | No | Categoría |
| marca_id | BIGINT | FK | Sí | Marca |
| tipo_iva_id | BIGINT | FK | No | IVA aplicable |
| calidad_repuesto | VARCHAR(10) | | Sí | `original`, `oem`, `generico` (CHECK) |
| precio_compra | NUMERIC(12,2) | | No | Costo actual |
| stock_minimo | INTEGER | | No | Umbral de stock bajo |
| activo | BOOLEAN | | No | Borrado lógico |

## tbpreciosproducto
- **Propósito:** precio de cada producto en cada tarifa.
- **Justificación:** tarifas configurables (respuesta B5, D-011).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| producto_id | BIGINT | PK, FK | No | Producto |
| tarifa_id | BIGINT | PK, FK | No | Tarifa |
| precio | NUMERIC(12,2) | | No | Precio con IVA incluido |

## tbproductosarchivos
- **Propósito:** imágenes de cada producto.
- **Justificación:** el usuario prevé imágenes de productos; el sistema viejo las guarda en base64 (hallazgo 9).
- **Alternativas descartadas:** `archivos_vinculos` genérico (D-024).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| producto_id | BIGINT | PK, FK | No | Producto |
| archivo_id | BIGINT | PK, FK | No | Imagen |
| posicion | SMALLINT | | No | Orden de las imágenes |
| es_principal | BOOLEAN | | No | Imagen que se muestra en listas |

## tbmovimientosinventario
- **Propósito:** cada entrada o salida de unidades.
- **Justificación:** el stock se calcula de aquí (D-010) con trazabilidad completa. Se alimenta de compras, ventas, repuestos usados en reparaciones (respuesta A9) y ajustes.
- **Valoración crítica:**
  - Enlaza con la factura o la compra que lo originó; un `CHECK` impide que tenga las dos.
  - Al anular una factura se registra una entrada de "anulación" que devuelve las unidades.
  - El stock inicial al migrar es un movimiento de tipo "inicial".

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| movimiento_inventario_id | IDENTITY | PK | No | Identificador |
| producto_id | BIGINT | FK | No | Producto |
| tipo | VARCHAR(10) | | No | `entrada` o `salida` (CHECK) |
| motivo | VARCHAR(20) | | No | `compra`, `venta`, `ajuste`, `devolucion`, `dano`, `inicial`, `anulacion` (CHECK) |
| cantidad | INTEGER | | No | Mayor que 0 |
| costo_unitario | NUMERIC(12,2) | | Sí | Costo en entradas |
| factura_id | BIGINT | FK | Sí | Factura que originó la salida |
| compra_id | BIGINT | FK | Sí | Compra que originó la entrada |
| observacion | VARCHAR(250) | | Sí | Detalle del ajuste |
| fecha_hora | TIMESTAMPTZ | | No | Cuándo |
| usuario_id | BIGINT | FK | No | Quién |

## tbcompras
- **Propósito:** cada compra de mercadería a un proveedor.
- **Justificación:** respuesta C3. Es el origen de las entradas de inventario y del costo (respuesta C4); el sistema viejo tiene costo 0 en todo (hallazgo 8).
- **Valoración crítica:**
  - Los totales se calculan desde `tbdetallecompra`.
  - **El pago sale de la caja** (respuesta P1): uno o varios egresos en `tbmovimientoscaja` con `compra_id`.
  - No hay compras a crédito ni cuentas por pagar por ahora. Si aparecen, el saldo de una compra se calcularía igual que el de una factura (total − egresos enlazados), sin tabla nueva.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| compra_id | IDENTITY | PK | No | Identificador |
| proveedor_id | BIGINT | FK | No | Proveedor |
| numero_documento | VARCHAR(30) | | Sí | Número de la factura del proveedor |
| fecha_compra | DATE | | No | Fecha del documento |
| observaciones | VARCHAR(250) | | Sí | Notas |
| anulada | BOOLEAN | | No | Si se anuló |
| usuario_id | BIGINT | FK | No | Quién la registró |
| fecha_registro | TIMESTAMPTZ | | No | Cuándo se registró |

## tbdetallecompra
- **Propósito:** cada producto comprado.
- **Justificación:** una compra incluye varios productos.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| detalle_compra_id | IDENTITY | PK | No | Identificador |
| compra_id | BIGINT | FK | No | Compra |
| producto_id | BIGINT | FK | No | Producto |
| cantidad | INTEGER | | No | Unidades |
| costo_unitario | NUMERIC(12,2) | | No | Costo por unidad |
| porcentaje_iva | NUMERIC(5,2) | | No | IVA de la compra |

---

# Ventas

## tbproformas
- **Propósito:** cotización sin valor fiscal que puede convertirse en venta.
- **Justificación:** D-013. Cotiza a la tarifa predeterminada, Público (respuesta B6). Al convertirla se respeta el precio cotizado (respuesta B7).
- **Valoración crítica:** sin estado ni fecha de vencimiento guardados (hallazgo 18): vencida si `fecha_emision + vigencia_dias` ya pasó; convertida si hay una factura con su `proforma_id`.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| proforma_id | IDENTITY | PK | No | Identificador |
| numero | VARCHAR(20) | UQ | No | `PRO-000002` |
| cliente_id | BIGINT | FK | No | Cliente |
| fecha_emision | TIMESTAMPTZ | | No | Fecha |
| vigencia_dias | SMALLINT | | No | Por defecto 7 |
| observaciones | TEXT | | Sí | Condiciones, alcance |
| pdf_archivo_id | BIGINT | FK | Sí | PDF generado |
| usuario_id | BIGINT | FK | No | Quién la creó |

## tbdetalleproforma

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| detalle_proforma_id | IDENTITY | PK | No | Identificador |
| proforma_id | BIGINT | FK | No | Proforma |
| producto_id | BIGINT | FK | No | Producto |
| cantidad | NUMERIC(10,2) | | No | Cantidad |
| precio_unitario | NUMERIC(12,2) | | No | Precio con IVA al cotizar |
| descuento | NUMERIC(12,2) | | No | Descuento de la línea (0 si no hay) |
| porcentaje_iva | NUMERIC(5,2) | | No | IVA aplicado |

- **Justificación:** líneas de la proforma (antes en JSON; hallazgo 10). El descuento se incluye porque al convertir se respeta lo cotizado (respuesta B7), con descuento incluido.

## tbfacturas
- **Propósito:** comprobante **interno** de venta o reparación (respuesta B1).
- **Justificación:** documento de cobro, origen de abonos y de cuentas por cobrar.
- **Valoración crítica:**
  - `cliente_id` es **a quien se factura**, que puede no ser quien trajo el equipo (D-017).
  - `orden_reparacion_id` es único: una orden, como máximo una factura (respuesta A8).
  - Los totales se guardan al emitir (respuesta B8).
  - Abonado, saldo y estado se calculan (D-009).
  - Se anula, no se borra.
  - Si en el futuro se emiten facturas del SRI, faltarían: establecimiento, punto de emisión, secuencial, clave de acceso, autorización y estado SRI.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| factura_id | IDENTITY | PK | No | Identificador |
| numero | VARCHAR(20) | UQ | No | `FAC-000016` |
| cliente_id | BIGINT | FK | No | A quien se factura |
| orden_reparacion_id | BIGINT | FK, UQ | Sí | Orden cobrada |
| proforma_id | BIGINT | FK, UQ | Sí | Proforma convertida |
| fecha_emision | TIMESTAMPTZ | | No | Fecha |
| subtotal_sin_iva | NUMERIC(12,2) | | No | Al emitir |
| total_descuento | NUMERIC(12,2) | | No | Al emitir |
| total_iva | NUMERIC(12,2) | | No | Al emitir |
| total | NUMERIC(12,2) | | No | Al emitir |
| anulada | BOOLEAN | | No | Si se anuló |
| fecha_anulacion | TIMESTAMPTZ | | Sí | Cuándo |
| motivo_anulacion | VARCHAR(250) | | Sí | Por qué |
| pdf_archivo_id | BIGINT | FK | Sí | PDF emitido |
| usuario_id | BIGINT | FK | No | Quién la emitió |

## tbdetallefactura
- **Justificación:** líneas de la factura (antes en JSON; hallazgo 10).
- **Valoración crítica:**
  - `precio_unitario`, `porcentaje_iva` y `costo_unitario` son copias del momento de la venta. Con el costo se calcula la ganancia aunque después cambie (D-020).
  - El descuento lo regulan la configuración y el permiso `ventas.aplicar_descuento` (D-019).
  - La tarifa se elige en cada línea; por defecto, la del cliente.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| detalle_factura_id | IDENTITY | PK | No | Identificador |
| factura_id | BIGINT | FK | No | Factura |
| producto_id | BIGINT | FK | No | Producto o servicio |
| tarifa_id | BIGINT | FK | No | Tarifa aplicada |
| cantidad | NUMERIC(10,2) | | No | Cantidad |
| precio_unitario | NUMERIC(12,2) | | No | Precio con IVA al vender |
| descuento | NUMERIC(12,2) | | No | Descuento de la línea |
| porcentaje_iva | NUMERIC(5,2) | | No | IVA aplicado |
| costo_unitario | NUMERIC(12,2) | | No | Costo al vender |

---

# Caja

## tbsesionescaja
- **Propósito:** cada apertura y cierre de la caja única (respuesta C1).
- **Justificación:** el sistema viejo solo guarda la caja actual y pierde los cierres (hallazgo 22).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| sesion_caja_id | IDENTITY | PK | No | Identificador |
| usuario_apertura_id | BIGINT | FK | No | Quién abrió |
| fecha_apertura | TIMESTAMPTZ | | No | Apertura |
| base_inicial | NUMERIC(12,2) | | No | Efectivo inicial |
| usuario_cierre_id | BIGINT | FK | Sí | Quién cerró |
| fecha_cierre | TIMESTAMPTZ | | Sí | Nula si está abierta |
| monto_contado_cierre | NUMERIC(12,2) | | Sí | Efectivo contado al cerrar |

## tbmovimientoscaja
- **Propósito:** entradas y salidas de dinero. Los ingresos con `factura_id` son los abonos (D-009); los egresos con `compra_id` son los pagos a proveedores (D-026).
- **Justificación:** todo cobro se hace con la caja abierta (respuesta C2).
- **Valoración crítica:**
  - El saldo acumulado se calcula.
  - Al anular una factura con abonos, la devolución es un egreso enlazado a esa factura.
  - Un `CHECK` impide que un movimiento tenga a la vez `factura_id` y `compra_id`.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| movimiento_caja_id | IDENTITY | PK | No | Identificador |
| sesion_caja_id | BIGINT | FK | No | Apertura de caja |
| tipo | VARCHAR(10) | | No | `ingreso` o `egreso` (CHECK) |
| metodo_pago_id | BIGINT | FK | No | Método |
| monto | NUMERIC(12,2) | | No | Mayor que 0 |
| concepto | VARCHAR(250) | | Sí | Nota libre |
| factura_id | BIGINT | FK | Sí | Factura abonada (o devuelta) |
| compra_id | BIGINT | FK | Sí | Compra pagada |
| fecha_hora | TIMESTAMPTZ | | No | Cuándo |
| usuario_id | BIGINT | FK | No | Quién |

---

# Archivos y correo

## tbarchivos
- **Propósito:** registro de cada archivo guardado fuera de la BD (imágenes y PDF): nombre, ruta, tipo y tamaño.
- **Justificación:** el sistema viejo guarda base64 (hallazgo 9). El archivo vive en el backend o en un servicio externo; la BD solo guarda dónde está (D-024).
- **Valoración crítica:** `hash_sha256` detecta archivos duplicados o alterados.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| archivo_id | IDENTITY | PK | No | Identificador |
| nombre_original | VARCHAR(255) | | No | Nombre con el que se subió |
| ruta | VARCHAR(500) | UQ | No | Ubicación en el almacenamiento |
| tipo_mime | VARCHAR(100) | | No | `image/jpeg`, `application/pdf` |
| tamano_bytes | BIGINT | | No | Tamaño |
| hash_sha256 | CHAR(64) | | No | Huella del contenido |
| fecha_subida | TIMESTAMPTZ | | No | Cuándo |
| usuario_id | BIGINT | FK | Sí | Quién lo subió; nulo si lo generó el sistema |

**Dónde se usa cada archivo** (todas con FK real):
- `tbproductosarchivos`: imágenes de productos.
- `tbordenesarchivos`: fotos del equipo.
- `tbordenesreparacion.pdf_ingreso_archivo_id`: PDF de la orden de ingreso.
- `tbfacturas.pdf_archivo_id`: PDF de la factura.
- `tbproformas.pdf_archivo_id`: PDF de la proforma.
- `tbenvioscorreo.archivo_id`: adjunto enviado.
- `tbconfiguracion.logo_archivo_id`: logo.

## tbenvioscorreo
- **Propósito:** cada envío de factura u orden por correo, con su resultado.
- **Justificación:** el sistema viejo solo recuerda el último envío y pierde los errores (hallazgo 24).
- **Valoración crítica:** un `CHECK` garantiza que solo una de `factura_id` u `orden_reparacion_id` esté llena.

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| envio_correo_id | IDENTITY | PK | No | Identificador |
| factura_id | BIGINT | FK | Sí | Factura enviada |
| orden_reparacion_id | BIGINT | FK | Sí | Orden enviada |
| archivo_id | BIGINT | FK | No | PDF adjunto |
| destinatario | VARCHAR(150) | | No | Correo de destino |
| fecha_envio | TIMESTAMPTZ | | No | Cuándo |
| exitoso | BOOLEAN | | No | Resultado |
| error | TEXT | | Sí | Mensaje si falló |
| usuario_id | BIGINT | FK | No | Quién lo envió |

---

# Configuración

## tbconfiguracion
- **Propósito:** datos del negocio y parámetros generales (D-012).
- **Valoración crítica:**
  - **Una sola fila** (`CHECK (configuracion_id = 1)`).
  - **IVA:** `tipo_iva_predeterminado_id` es el IVA que se propone a cada producto nuevo (respuesta B3).
  - **Descuentos:** `descuento_maximo_porcentaje` lo fija el dueño (respuesta B2); 0 = sin descuentos.
  - **Cláusulas:** no se copian en cada orden (respuesta D5).
  - **Credenciales de Gmail:** fuera de la BD (hallazgo 32).

| Columna | Tipo | Clave | Nulo | Descripción |
|---|---|---|---|---|
| configuracion_id | SMALLINT | PK | No | Siempre 1 |
| ruc | VARCHAR(13) | | Sí | RUC |
| nombre_comercial | VARCHAR(150) | | No | EDITRONIC |
| razon_social | VARCHAR(200) | | Sí | Razón social legal |
| telefono | VARCHAR(20) | | Sí | Teléfono |
| direccion | VARCHAR(250) | | Sí | Dirección |
| correo | VARCHAR(150) | | Sí | Remitente de facturas |
| tipo_iva_predeterminado_id | BIGINT | FK | No | IVA por defecto |
| descuento_maximo_porcentaje | NUMERIC(5,2) | | No | Tope de descuento |
| logo_archivo_id | BIGINT | FK | Sí | Logo |
| clausulas_servicio | TEXT | | Sí | Condiciones impresas en órdenes |
| color_principal | CHAR(7) | | Sí | `#4524eb` |
| color_secundario | CHAR(7) | | Sí | `#0f172a` |

---

# Relaciones principales

| Origen (1) | Destino (N) | Mediante |
|---|---|---|
| `tbtiposidentificacion` | `tbclientes`, `tbproveedores` | `tipo_identificacion_id` |
| `tbtarifas` | `tbclientes`, `tbpreciosproducto`, `tbdetallefactura` | `tarifa_id` |
| `tbroles` | `tbusuarios` | `rol_id` |
| `tbroles` ↔ `tbpermisos` | `tbrolespermisos` | N a N |
| `tbusuarios` | `tbsesiones` | `usuario_id` |
| `tbsesiones` | `tbrefreshtokens` | `sesion_id` |
| `tbclientes` | `tbequipos` (propietario), `tbordenesreparacion` (quien trae), `tbfacturas` (a quien se factura), `tbproformas` | `cliente_id` |
| `tbtiposequipo`, `tbmarcas` | `tbequipos` | `tipo_equipo_id`, `marca_id` |
| `tbequipos` | `tbordenesreparacion` | `equipo_id` |
| `tbordenesreparacion` | `tbordenesreparacion` (garantía) | `orden_garantia_id` |
| `tbordenesreparacion` | `tbhistorialestadosorden` | `orden_reparacion_id` |
| `tbestadosorden` | `tbhistorialestadosorden` | `estado_orden_id` |
| `tbordenesreparacion` | `tbfacturas` (0..1) | `orden_reparacion_id` |
| `tbproformas` | `tbfacturas` (0..1) | `proforma_id` |
| `tbcategoriasproducto`, `tbmarcas`, `tbtiposiva` | `tbproductos` | FK homónimas |
| `tbproductos` | `tbpreciosproducto`, `tbdetallefactura`, `tbdetalleproforma`, `tbdetallecompra`, `tbmovimientosinventario` | `producto_id` |
| `tbproveedores` | `tbcompras` | `proveedor_id` |
| `tbcompras` | `tbdetallecompra`, `tbmovimientosinventario`, `tbmovimientoscaja` | `compra_id` |
| `tbfacturas` | `tbdetallefactura`, `tbmovimientoscaja`, `tbmovimientosinventario`, `tbenvioscorreo` | `factura_id` |
| `tbproformas` | `tbdetalleproforma` | `proforma_id` |
| `tbsesionescaja` | `tbmovimientoscaja` | `sesion_caja_id` |
| `tbmetodospago` | `tbmovimientoscaja` | `metodo_pago_id` |
| `tbarchivos` | `tbproductosarchivos`, `tbordenesarchivos`, PDF de órdenes, facturas y proformas, `tbenvioscorreo`, `tbconfiguracion` | `archivo_id` |
| `tbusuarios` | casi todas (quién registró la operación) | `usuario_id` |
