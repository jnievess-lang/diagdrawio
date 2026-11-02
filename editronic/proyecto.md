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
1. ~~**Inventario de equipos**~~: resuelta; son los equipos de clientes en reparación (vista de órdenes).
2. **Facturación electrónica:** ¿las facturas `FAC-000016` están autorizadas por el SRI o son comprobantes internos? El RUC vacío en Configuración sugiere que son internas.
3. ~~**Roles**~~: resuelta; Administrador, Técnico y Secretario/a. Falta saber los permisos de cada uno.
4. **Compras y proveedores:** ¿se registra la compra de mercadería o el stock entra solo por ajuste?
5. **Repuestos en reparaciones:** ¿se descuentan del inventario y se facturan en la misma factura de reparación?
6. **Tarifa por cliente:** ¿cada cliente tiene una tarifa fija o se elige en cada venta?
7. **Técnico asignado:** con el rol Técnico, ¿cada orden de reparación tiene un técnico responsable?
8. **Proformas:** ¿siempre se cotiza a precio Público? ¿También se cotizan reparaciones?
9. **Cláusulas:** ¿hay que conservar en cada orden las cláusulas vigentes cuando se imprimió?

## Glosario
| Término | Significado |
|---|---|
| Proforma | Cotización sin valor fiscal que puede convertirse en venta u orden de reparación |
| Cuenta por cobrar | Deuda de un cliente generada por una venta o servicio a crédito |
