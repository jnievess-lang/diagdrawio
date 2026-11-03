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
| A2 | Estados: Recibido, En diagnóstico, Esperando aprobación, En reparación, Reparado, Entregado (+ "No aprobado", P2) | `tbestadosorden` |
| A3 | Sí, historial de estados | `tbhistorialestadosorden`, D-016 |
| A4 | Sí, técnico asignado | `tbordenesreparacion.tecnico_id` |
| A5 | Diagnóstico, costo, fecha y accesorios | `tbordenesreparacion` |
| A6 | El diagnóstico se cobra como servicio (aunque el cliente se lleve el equipo a otro lado) | Producto de categoría Servicio |
| A7 | Garantía enlazada con la orden original y configurable por tipo de equipo | D-015 |
| A8 | Una orden, una factura como máximo | `tbfacturas.orden_reparacion_id` único |
| A9 | Los repuestos se descuentan del inventario y van en la factura | `tbmovimientosinventario` |
| B1 | Facturas internas | Sin campos del SRI por ahora |
| B2 | Sí hay descuentos, configurables por el dueño | D-019 |
| B3 | Hay productos con IVA 0 % | D-018 |
| B4 | Tarifa fija por cliente, modificable en la venta | `tbclientes.tarifa_id` |
| B5 | Tarifas configurables | D-011 |
| B6 | Proformas a precio Público, solo productos y servicios del catálogo | `tbtarifas.es_predeterminada` |
| B7 | Al convertir una proforma se respeta el precio cotizado | `tbdetalleproforma` |
| B8 | Totales de factura guardados al emitir | Excepción a D-008 |
| C1 | Una sola caja | `tbsesionescaja` |
| C2 | Todo cobro con caja abierta | D-009 |
| C3 | Sí se registran compras a proveedores | D-020 |
| C4 | Sí se necesita el precio de compra | D-020 |
| C5 | OEM indica repuesto con la calidad del fabricante original | D-022 |
| C6 | El servicio se define por la categoría | D-021 |
| D1 | Un solo campo `razon_social` (se atiende a empresas) | `tbclientes` |
| D2 | Sí, consumidor final | `tbtiposidentificacion` |
| D3 | Permisos en la BD, configurables desde el panel | D-023 |
| D4 | Usuario sin correo entra con su usuario | `tbusuarios` |
| D5 | No se copian las cláusulas en cada orden | `tbconfiguracion` |
| E | Todas las decisiones D-002 a D-014 aceptadas | `decisiones.md` |
| F | La migración la hace el usuario. Faltan tablas de archivos (no base64) y de autenticación. No usar JSON para líneas | D-024, D-025 |

## Preguntas finales (respondidas el 2026-11-03)
| # | Respuesta | Dónde se aplica |
|---|---|---|
| P1 | Las compras se pagan con egreso de caja; sin cuentas por pagar por ahora | D-026, `tbmovimientoscaja.compra_id` |
| P2 | Se añade el estado "No aprobado" | `tbestadosorden` (no final: luego pasa a Entregado) |
| P3 | Sí, fotos del equipo al recibirlo | `tbordenesarchivos` |
| P4 | Sin "olvidé mi contraseña" por ahora | `tokens_recuperacion` descartada |
| P5 | OEM como `calidad_repuesto` (Original, OEM, Genérico) | D-022 |
| P6 | Archivos con tablas de vínculo por uso | D-024 |
| P7 | Estado actual calculado desde el historial | D-016 |

**No quedan preguntas abiertas.** Siguiente paso: validación final de `entidades.md`.

## Glosario
| Término | Significado |
|---|---|
| Proforma | Cotización sin valor fiscal que puede convertirse en venta u orden de reparación |
| Cuenta por cobrar | Deuda de un cliente generada por una venta o servicio a crédito |
