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
- Pendiente de definir.

## Requisitos técnicos
- **Motor de base de datos:** PostgreSQL (ver D-005).
- **Volumen esperado de datos:** pendiente.

- **País:** Ecuador (deducido del IVA del 15 %, la cédula/RUC y las direcciones). Por confirmar.
- **IVA:** 15 %, precios con IVA incluido.

## Dudas abiertas
1. ~~**Inventario de equipos**~~: resuelta; son los equipos de clientes en reparación (vista de órdenes).
2. **Facturación electrónica:** ¿las facturas `FAC-000016` están autorizadas por el SRI o son comprobantes internos?
3. **Roles:** ¿qué perfiles de usuario hay (administrador, técnico, cajero…)?
4. **Compras y proveedores:** ¿se registra la compra de mercadería o el stock entra solo por ajuste?
5. **Repuestos en reparaciones:** ¿se descuentan del inventario y se facturan en la misma factura de reparación?
6. **Tarifa por cliente:** ¿cada cliente tiene una tarifa fija o se elige en cada venta?

## Glosario
| Término | Significado |
|---|---|
| Proforma | Cotización sin valor fiscal que puede convertirse en venta u orden de reparación |
| Cuenta por cobrar | Deuda de un cliente generada por una venta o servicio a crédito |
