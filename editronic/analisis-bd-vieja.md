# Análisis de la base de datos vieja

**Uso de este archivo:** la BD vieja sirve **solo como guía** para entender cómo funciona el negocio. No es un modelo a copiar. Cuando la BD vieja y las respuestas del usuario no coinciden, mandan las respuestas del usuario. La migración de datos la hace el usuario.

**Fuentes:**
- 15 capturas de pantalla del sistema viejo.
- Exportación `bd.json`: no se sube al repositorio porque contiene datos personales de clientes.

## Estructura de `bd.json`
Es un único documento JSON con 7 colecciones. No es una base de datos relacional.

| Colección | Registros | Qué guarda | Tablas nuevas equivalentes |
|---|---|---|---|
| `company` | 1 objeto | Datos de la empresa e IVA | `configuracion` |
| `cash` | 1 objeto + 16 movimientos | Solo la caja **actual** y sus movimientos | `sesiones_caja`, `movimientos_caja` |
| `clients` | 37 | Clientes | `clientes`, `tipos_identificacion` |
| `devices` | 27 | Equipo + orden + estado + garantía en un mismo registro | `equipos`, `ordenes_reparacion`, `historial_estados_orden`, `tipos_equipo`, `estados_orden` |
| `products` | 87 | Productos y servicios con precios y stock | `productos`, `categorias_producto`, `marcas`, `precios_producto`, `tarifas`, `movimientos_inventario` |
| `sales` | 16 | Factura + líneas (JSON) + pagos (JSON) + datos del cliente copiados + último correo | `facturas`, `detalle_factura`, `movimientos_caja`, `envios_correo` |
| `proformas` | 2 | Proforma + líneas (JSON) + datos del cliente copiados | `proformas`, `detalle_proforma` |

**No aparecen en la exportación:** usuarios, roles, sesiones, compras, proveedores ni archivos. El usuario indica que el sistema viejo guarda fotos en base64 en una columna `foto`.

## Hallazgos
Cada hallazgo indica cómo se corrige en el modelo nuevo.

### Integridad y tipos de datos
| # | Hallazgo | Corrección |
|---|---|---|
| 1 | **Categorías en texto libre: 14 variantes en 87 productos** (`accesorios` ×50, `ACCESORIO`, `PRODUCTO`, `PRODUCTOS`, `SERVICIO`, `servicio`, `Servicio Tecnico`, `SERVICIO/REPUESTO`, `Cargador`, `Disco`, `Celular`, `Laptop`, `repuesto`, vacía) | Catálogo `categorias_producto` (D-007) |
| 2 | **Marcas en texto libre**: `HP`/`Hp`/`hp`, `meetion`/`MEETION`, `Wuasad`/`Quasad`, `xiomi`; mezcla marca con color (`GENIUS NEGRO`), línea (`WD Green`, `EPSON AAA`) o modelo (`PM-02`); 29 productos sin marca | Catálogo `marcas` compartido con equipos |
| 3 | **"OEM" guardado como marca** | OEM es la calidad del repuesto, no una marca (D-022) |
| 4 | **Tipo de equipo "Otro" + `customType` en texto** (`Tarjeta grafica`, `Mando PS5`) | Catálogo `tipos_equipo` ampliable; sin texto libre |
| 5 | **Fechas guardadas como texto local** (`"21/9/2026, 10:52:39 a. m."`) y repetidas en `dateKey` | `TIMESTAMPTZ` (D-005); se ordenan y filtran correctamente |
| 6 | **Identificadores de texto aleatorios** (`MOV-MUBGF7ZU629`, `VTA-…`, `ABO-…`) | PK `BIGINT IDENTITY`; el número visible (`FAC-000016`) es una columna aparte |
| 7 | **Prefijos de orden inconsistentes**: los equipos usan `OR-000003` y el concepto de caja `OT-000003` | Un solo número por orden, guardado una vez |
| 8 | **Precio de compra en 0 en los 87 productos** | Costo obligatorio en compras y copiado en cada venta (D-020) |
| 9 | **Fotos en base64 dentro de la BD** (según el usuario) | Tabla `archivos` con ruta; el archivo vive fuera de la BD (D-024) |

### Normalización
| # | Hallazgo | Corrección |
|---|---|---|
| 10 | **Líneas de venta y de proforma como array JSON** (`items`) | `detalle_factura`, `detalle_proforma` |
| 11 | **Pagos como array JSON dentro de la venta** (`payments`) y repetidos como movimiento de caja (`paymentId`) | El abono es el movimiento de caja (D-009) |
| 12 | **Datos del cliente copiados en cada venta y proforma** (`clientName`, `clientEmail`, `clientPhone`, `clientCedula`) | Solo `cliente_id` |
| 13 | **Equipo y orden en el mismo registro** (`devices`) | `equipos` + `ordenes_reparacion` (D-006) |
| 14 | **Facturar a otra persona con campos sueltos** (`billingClientId`, `serviceClientName`, `serviceClientCedula`, `billedToDifferentPerson`) | `ordenes_reparacion.cliente_id` (quien trae el equipo) y `facturas.cliente_id` (a quien se factura) (D-017) |
| 15 | **Tres columnas de precio** (`price`, `techPrice`, `wholesalePrice`) | `tarifas` + `precios_producto` (D-011) |
| 16 | **Referencias dentro de texto** (`"Reparación OT-000003 · FAC-000001 · Efectivo"`) | FK reales; el concepto queda para notas |

### Datos calculados que se guardan
| # | Hallazgo | Corrección |
|---|---|---|
| 17 | `balance`, `amountPaid`, `paymentStatus`, `creditSale` en ventas | Se calculan desde los abonos (D-008, D-009) |
| 18 | `validUntil` junto a `validityDays` y `status: "Vigente"` en proformas | Solo `vigencia_dias`; vencimiento y estado se calculan |
| 19 | `repairedAt`, `deliveredAt`, `warrantyStart`, `warrantyUntil` en equipos | Se obtienen de `historial_estados_orden` (D-016) |
| 20 | `stock` editable en el producto | Se calcula desde `movimientos_inventario` (D-010) |
| 21 | Saldo de caja, totales por método y `lastClosedTotal` | Se calculan; solo se guarda el efectivo contado al cerrar |

### Historial que se pierde
| # | Hallazgo | Corrección |
|---|---|---|
| 22 | **Solo existe la caja actual**: al abrir una nueva se pierden los cierres anteriores (solo queda `lastClosedTotal`) | `sesiones_caja` con un registro por apertura |
| 23 | **Solo el estado actual del equipo**, sin quién ni cuándo lo cambió | `historial_estados_orden` (D-016) |
| 24 | **Solo el último correo** (`lastEmailSentAt`, `lastEmailStatus`, `lastEmailRecipient`); un envío con `Error` ya no deja rastro | `envios_correo` |
| 25 | **Garantía por equipo, casi siempre 0** (26 de 27 equipos con 0 días; un PlayStation con 90) | Garantía por tipo de equipo, copiada en la orden (D-015) |

### Seguridad y operación
| # | Hallazgo | Corrección |
|---|---|---|
| 26 | **Sin tablas de autenticación** (sesiones, refresh tokens) | `sesiones`, `refresh_tokens` (D-025) |
| 27 | **Administrador guardado aparte** del resto de usuarios | Un solo `usuarios` con rol (D-014) |
| 28 | **Permisos inexistentes o fijos** | `permisos` + `roles_permisos`, configurables (D-023) |
| 29 | **Borrado físico** de clientes, equipos y facturas | Borrado lógico (`activo`) y anulación de facturas |
| 30 | **Botón "Restablecer datos de prueba"** en el sistema en uso | Fuera del alcance del modelo; quitarlo del sistema nuevo |
| 31 | **RUC vacío y razón social "Soporte técnico"** | Las facturas son comprobantes internos (respuesta B1) |
| 32 | **Credenciales de Gmail API** | En la configuración del servidor, nunca en la BD |

### Lo que la BD vieja sí enseña del negocio
- El cliente que trae el equipo puede no ser a quien se factura.
- Una venta puede quedar a crédito con abonos parciales (3 de 16 ventas).
- Todas las ventas usan precios con IVA incluido.
- Las proformas se convierten en venta (`saleId`, `convertedAt`).
- Hay egresos de caja (1 de 16 movimientos).
- Los servicios (mantenimiento, diagnóstico) se venden como productos del catálogo.
