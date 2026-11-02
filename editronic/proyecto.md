# Proyecto Editronic

## Descripción
Editronic es un local que combina dos negocios:
- **Servicio técnico:** reparación de equipos (computadoras, impresoras, mandos, consolas, etc.).
- **Venta de productos tecnológicos:** mouse, teclados, laptops, etc.

Además gestiona inventario y facturación.

## Contexto
- Existe un **sistema viejo** con su propia base de datos.
- El objetivo es diseñar una **base de datos nueva, profesional y normalizada**, sin las tablas innecesarias del sistema viejo.
- Se parte de las primeras tablas que conoce el usuario y se amplía de forma incremental; cada entidad se justifica (ver `CLAUDE.md`).

## Módulos
| Módulo | Descripción |
|---|---|
| Dashboard | Resumen e indicadores del negocio |
| Caja | Apertura, cierre y movimientos de caja |
| Clientes | Datos de los clientes |
| Equipos | Equipos que los clientes traen a reparar |
| Ventas | Ventas de productos (y cobro de servicios) |
| Inventario: productos | Catálogo de productos a la venta |
| Inventario: inventario | Existencias y movimientos de stock |
| Inventario: inventario de equipos | Equipos de clientes en el taller: es una vista de las órdenes de reparación, no una tabla propia |
| Proformas | Cotizaciones previas a una venta o reparación |
| Cuentas por cobrar | Saldos pendientes de los clientes y sus abonos |
| Empleados | Personal del local |
| Configuración | Parámetros del sistema (datos del negocio, impuestos, etc.) |
| Perfil | Datos y credenciales del usuario que inicia sesión |
| Otros | Envío de facturas por correo, entre otros |

## Usuarios y roles
- Roles vistos: **Administrador**, **Técnico**, **Secretario/a**.
- Cada empleado es un usuario del sistema (D-014).
- Pendiente: qué puede hacer cada rol.

## Requisitos técnicos
- **Motor de base de datos:** PostgreSQL (ver D-005).
- **Volumen esperado de datos:** pendiente.

- **País:** Ecuador; el local está en el centro de Quevedo (dirección en Configuración).
- **IVA:** 15 %, configurable en Configuración; precios con IVA incluido.
- **Correo:** facturas y órdenes se envían en PDF mediante Gmail API desde el correo de la empresa.

## Dudas abiertas
Lista única y completa de lo que falta decidir antes de diagramar. Cada duda trae una **recomendación**: si el usuario la acepta, basta responder "ok".

### A. Servicio técnico
| # | Duda | Recomendación | Afecta a |
|---|---|---|---|
| A1 | ¿La persona que deja el equipo puede ser distinta del dueño registrado? | Si siempre es el dueño, quitar `cliente_id` de la orden | `ordenes_reparacion` |
| A2 | ¿Cuál es la lista completa de estados de una orden? | Recibido, En diagnóstico, En reparación, Reparado, Entregado, Sin reparación | `estados_orden` |
| A3 | ¿Se guarda el historial de cambios de estado (quién y cuándo)? | Sí, con una tabla `historial_estados_orden` | Nueva tabla |
| A4 | ¿Cada orden tiene un técnico asignado? | Sí, `tecnico_id` hacia `usuarios` | `ordenes_reparacion` |
| A5 | ¿Se registran diagnóstico técnico, costo estimado, fecha de entrega o accesorios recibidos? | Al menos `diagnostico` y `fecha_entrega` | `ordenes_reparacion` |
| A6 | Las cláusulas dicen que el diagnóstico se cobra aunque no se repare. ¿Se factura como un servicio del catálogo? | Sí, como producto con `es_servicio` | `productos`, `detalle_factura` |
| A7 | Las cláusulas dan 3 meses de garantía. ¿Hay que enlazar una orden por garantía con la orden original? | Sí, `orden_garantia_id` opcional en la orden | `ordenes_reparacion` |
| A8 | ¿Una orden puede tener más de una factura? | No: una orden, como máximo una factura | `facturas` |
| A9 | ¿Los repuestos usados en una reparación se descuentan del inventario y van en la misma factura? | Sí | `detalle_factura`, `movimientos_inventario` |

### B. Ventas, facturas y proformas
| # | Duda | Recomendación | Afecta a |
|---|---|---|---|
| B1 | ¿Las facturas están autorizadas por el SRI o son comprobantes internos? | Internos ahora (el RUC está vacío), dejando claro qué faltaría para el SRI | `facturas`, `configuracion` |
| B2 | ¿Se usan descuentos? | No añadirlos si no se usan | `detalle_factura` |
| B3 | ¿Todos los productos llevan IVA 15 % o hay alguno con 0 %? | Si hay 0 %, `porcentaje_iva` en el producto | `productos` |
| B4 | ¿Cada cliente tiene una tarifa fija o se elige en cada venta? | Tarifa por defecto en el cliente, modificable en la venta | `clientes` |
| B5 | ¿Las tres tarifas (Público, Técnico, Mayorista) son definitivas? | Tabla `precios_producto` (D-011) si pueden cambiar | `precios_producto` |
| B6 | ¿Las proformas cotizan siempre a precio Público? ¿También cotizan reparaciones? | Público; solo productos y servicios del catálogo | `proformas` |
| B7 | Al convertir una proforma vigente, ¿se respeta el precio cotizado? | Sí | `detalle_proforma` |
| B8 | ¿Totales de factura guardados al emitir (excepción a D-008)? | Sí | `facturas` |

### C. Caja e inventario
| # | Duda | Recomendación | Afecta a |
|---|---|---|---|
| C1 | ¿Hay una sola caja o varios puntos de cobro? | Una sola caja | `sesiones_caja` |
| C2 | ¿Todo cobro, también por transferencia, se hace con la caja abierta? | Sí (requisito de D-009) | `movimientos_caja` |
| C3 | ¿Se registran compras a proveedores? | Si no se usan, entradas por ajuste con motivo | Posibles `proveedores`, `compras` |
| C4 | ¿Se necesita el precio de compra? Hoy siempre está en $0 | Sí, para calcular ganancia | `productos` |
| C5 | "OEM": ¿marca del catálogo o sin marca? | Valor del catálogo "Genérico/OEM" | `marcas` |
| C6 | ¿La categoría "servicio" basta o se mantiene `es_servicio`? | Mantener `es_servicio` | `productos` |

### D. Clientes, usuarios y configuración
| # | Duda | Recomendación | Afecta a |
|---|---|---|---|
| D1 | ¿Nombre del cliente en un solo campo (`razon_social`)? | Sí | `clientes` |
| D2 | ¿Se usa "consumidor final" para ventas sin cliente identificado? | Sí, como tipo de identificación | `clientes` |
| D3 | ¿Los permisos de cada rol se configuran en el sistema o son fijos? | Fijos en el código | `roles` |
| D4 | El login acepta usuario o correo. Si un usuario no tiene correo, solo entra con su usuario: ¿es aceptable? | Sí | `usuarios` |
| D5 | ¿Hay que conservar en cada orden las cláusulas vigentes al imprimirla? | No por ahora | `ordenes_reparacion` |

### E. Decisiones por validar
| # | Decisión | Recomendación |
|---|---|---|
| E1 | D-002 `snake_case` en español, PK `id`, FK `tabla_id` | Aceptar |
| E2 | D-003 / D-005 tipos de PostgreSQL, importes `NUMERIC(12,2)` | Aceptar |
| E3 | D-006 a D-014 (ver `decisiones.md`) | Aceptar |

### F. Migración
| # | Duda | Recomendación | Afecta a |
|---|---|---|---|
| F1 | ¿Se migrarán los datos del sistema viejo a la base nueva? | Sí, con limpieza de marcas, categorías y modelos (hallazgos 6 y 8) | Plan de migración |

### Resueltas
- Inventario de equipos: vista de las órdenes de reparación.
- Roles: Administrador, Técnico, Secretario/a.
- Cuentas por cobrar: facturas con saldo (D-009).
- Empleados = usuarios (D-014).
- Acceso: solo inicio de sesión con usuario o correo; no hay registro público (las cuentas las crea el administrador).

## Glosario
| Término | Significado |
|---|---|
| Proforma | Cotización sin valor fiscal que puede convertirse en venta u orden de reparación |
| Cuenta por cobrar | Deuda de un cliente generada por una venta o servicio a crédito |
