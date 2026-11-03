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
- Roles: **Administrador**, **Técnico**, **Secretario/a**.
- Cada empleado es un usuario del sistema (D-014).
- Los permisos de cada rol se configuran desde el panel administrativo (D-023).
- No hay registro público: el administrador crea las cuentas. Login con usuario o correo.

## Requisitos técnicos
- **Motor de base de datos:** PostgreSQL (ver D-005).
- **Volumen esperado de datos:** bajo (37 clientes, 87 productos, 27 órdenes y 16 facturas en el sistema viejo).
- **Facturación:** comprobantes internos, no electrónicos del SRI (respuesta B1).
- **Archivos:** imágenes y PDF se guardan fuera de la BD (backend o servicio externo); la BD guarda nombre y ruta.

- **País:** Ecuador; el local está en el centro de Quevedo (dirección en Configuración).
- **IVA:** 15 %, configurable en Configuración; precios con IVA incluido.
- **Correo:** facturas y órdenes se envían en PDF mediante Gmail API desde el correo de la empresa.

## Respuestas del usuario (2026-11-03)
Tienen **prioridad sobre la BD vieja**.

| # | Respuesta | Dónde se aplica |
|---|---|---|
| A1 | Quien trae el equipo puede no ser a quien se factura | D-017 |
| A2 | Estados: Recibido, En diagnóstico, Esperando aprobación, En reparación, Reparado, Entregado | `estados_orden` |
| A3 | Sí, historial de estados | `historial_estados_orden`, D-016 |
| A4 | Sí, técnico asignado | `ordenes_reparacion.tecnico_id` |
| A5 | Diagnóstico, costo, fecha y accesorios | `ordenes_reparacion` |
| A6 | El diagnóstico se cobra como servicio (aunque el cliente se lleve el equipo a otro lado) | Producto de categoría Servicio |
| A7 | Garantía enlazada con la orden original y configurable por tipo de equipo | D-015 |
| A8 | Una orden, una factura como máximo | `facturas.orden_reparacion_id` único |
| A9 | Los repuestos se descuentan del inventario y van en la factura | `movimientos_inventario` |
| B1 | Facturas internas | Sin campos del SRI por ahora |
| B2 | Sí hay descuentos, configurables por el dueño | D-019 |
| B3 | Hay productos con IVA 0 % | D-018 |
| B4 | Tarifa fija por cliente, modificable en la venta | `clientes.tarifa_id` |
| B5 | Tarifas configurables | D-011 |
| B6 | Proformas a precio Público, solo productos y servicios del catálogo | `tarifas.es_predeterminada` |
| B7 | Al convertir una proforma se respeta el precio cotizado | `detalle_proforma` |
| B8 | Totales de factura guardados al emitir | Excepción a D-008 |
| C1 | Una sola caja | `sesiones_caja` |
| C2 | Todo cobro con caja abierta | D-009 |
| C3 | Sí se registran compras a proveedores | D-020 |
| C4 | Sí se necesita el precio de compra | D-020 |
| C5 | OEM indica repuesto con la calidad del fabricante original | D-022 |
| C6 | El servicio se define por la categoría | D-021 |
| D1 | Un solo campo `razon_social` (se atiende a empresas) | `clientes` |
| D2 | Sí, consumidor final | `tipos_identificacion` |
| D3 | Permisos en la BD, configurables desde el panel | D-023 |
| D4 | Usuario sin correo entra con su usuario | `usuarios` |
| D5 | No se copian las cláusulas en cada orden | `configuracion` |
| E | Todas las decisiones D-002 a D-014 aceptadas | `decisiones.md` |
| F | La migración la hace el usuario. Faltan tablas de archivos (no base64) y de autenticación. No usar JSON para líneas | D-024, D-025 |

## Preguntas pendientes
Solo surgieron de las respuestas anteriores. Cada una trae una recomendación.

| # | Pregunta | Recomendación |
|---|---|---|
| P1 | ¿Las compras a proveedores se pagan desde la caja? ¿Hay compras a crédito (cuentas por pagar)? | Si se pagan en caja: `movimientos_caja.compra_id` en los egresos. Sin cuentas por pagar por ahora |
| P2 | Si el cliente no aprueba el presupuesto en "Esperando aprobación", ¿a qué estado pasa? | Añadir "No aprobado" como estado final, que cobra solo el diagnóstico |
| P3 | ¿Se guardan fotos del equipo al recibirlo (`ordenes_archivos`)? | Sí: protegen la garantía ante reclamos por golpes |
| P4 | ¿Se necesita "olvidé mi contraseña" por correo? | No por ahora: el administrador restablece las contraseñas |
| P5 | OEM: ¿confirmas `calidad_repuesto` con los valores Original, OEM y Genérico? | Sí (D-022) |
| P6 | Archivos: ¿aceptas tablas de vínculo por uso en lugar de una tabla genérica con el nombre de la tabla (D-024)? | Sí |
| P7 | Estado actual de la orden calculado desde el historial, sin columna (D-016) | Sí |

## Glosario
| Término | Significado |
|---|---|
| Proforma | Cotización sin valor fiscal que puede convertirse en venta u orden de reparación |
| Cuenta por cobrar | Deuda de un cliente generada por una venta o servicio a crédito |
