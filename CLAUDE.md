# PROYECTO CEDA — Inteligencia de mercado de la Central de Abasto

> **Cómo usar este archivo:** está en la raíz del repositorio como `CLAUDE.md` (Claude Code lo lee automáticamente) o pégalo al inicio de tu sesión con Blackbox CLI. Es el contexto completo del proyecto: cualquier agente de IA que lo lea debe poder continuar el trabajo sin explicaciones adicionales.

## 1. Qué es este negocio

Servicio B2B de inteligencia de precios para locatarios y compradores mayoristas de la Central de Abasto (CDMX). El fundador (José) trabaja dentro de la Central (4:30–13:30) y captura precios reales cada madrugada: precio mín/frec/máx, calidad, volumen y contexto de pasillo. Ese dato fresco + recomendaciones accionables se vende por suscripción ($199–299 MXN/mes por cliente).

**Ventaja competitiva:** acceso físico diario al dato antes de las 6:00 am (hora en que los clientes deciden sus compras) + histórico propio acumulado. El SNIIM (gobierno) publica promedios con retraso y sin contexto; las apps existentes (CEDACDMX, Click Abasto, Mayoreo Online) venden producto, no inteligencia.

**Regla de oro comercial:** vender antes de construir. El reporte por WhatsApp es el producto v0 y NO se detiene por desarrollar la app. Desarrollo solo por las tardes, con tope de 2–3 semanas por fase.

## 2. Activos que ya existen

- `Plan_de_vida_y_negocio_Jose.docx` — plan completo a corto/mediano/largo plazo.
- Skill `analista-ceda` — normaliza capturas, mantiene `historico_precios.csv`, genera el Reporte CEDA (formato WhatsApp) y alertas (±12% en un día o rachas de 3+ días).
- Skill `vendedor-ceda` — pitch, objeciones, seguimiento, referidos.
- Esquema de captura (CSV): `fecha, producto, presentacion, calidad, precio_min, precio_frec, precio_max, volumen, nota_contexto`

## 3. Producto por fases (la app se construye en este orden)

### Fase 0 — Reporte WhatsApp (semanas 1–6) · SIN CÓDIGO
Captura manual → skill analista → reporte texto → WhatsApp. Meta: 8–10 clientes de pago. **Esta fase valida el negocio; todo lo demás depende de ella.**

### Fase 1 — Panorama CEDA (web estática) · semanas 3–6
- Página web mobile-first, un solo archivo HTML o sitio estático.
- Contenido: precios del día, tendencia semanal (mini-gráficas), y sección **"¿Por qué se va a mover el precio?"** (factores externos, ver §5).
- Datos: un `datos/datos.json` que José regenera cada madrugada (la skill analista puede producirlo) y sube al repo.
- Hosting: GitHub Pages o Vercel (gratis). Sin login, sin base de datos. Se comparte por link de WhatsApp.
- Stack: HTML + CSS + JS vanilla en `index.html`. Mientras menos piezas, menos se rompe.

### Fase 2 — App con cuentas · meses 3–6 (SOLO si hay 20+ clientes pagando)
- Stack sugerido: Next.js + Supabase (plan gratis) + Vercel.
- Cada cliente inicia sesión y ve SOLO sus productos contratados → Supabase **RLS** (Row Level Security) obligatorio desde el primer día de esta fase.
- Pagos: primero manual (transferencia + activación), Stripe/MercadoPago después.

### Fase 3 — Cooperativa de datos · meses 6+
- Bodegueros de confianza aportan sus precios (formulario dentro de la app) y a cambio reciben gratis el panorama agregado y anonimizado.
- Anti-trampa: cruzar lo reportado contra la captura presencial de José; marcar outliers; dos reportes falsos = fuera del panorama.
- **Nunca** mostrar el dato individual de un aportante; solo agregados.

## 4. Modelo de datos (núcleo)

```
precios:   fecha, producto, presentacion, calidad, precio_min, precio_frec,
           precio_max, volumen, nota_contexto, fuente (jose|aportante_id)
eventos:   fecha, tipo (clima|cosecha|flete|bloqueo|cambiario|arancel|politica|economia), descripcion,
           productos_afectados[], direccion_esperada (alza|baja|incierto), fuente_url
clientes:  id, nombre, contacto, productos_contratados[], plan, etapa
           (prospecto|prueba|pago|renovo), fecha_alta
```

## 5. Factores externos (sección "¿Por qué se va a mover el precio?")

Fuentes gratuitas a consultar/mostrar:
- **Clima:** SMN / Conagua (heladas, ciclones, sequía en zonas productoras).
- **Cosechas:** SIAP / SADER (avance de siembra y cosecha por estado).
- **Flete:** precio de gasolina/diésel (CRE) y bloqueos carreteros (noticias).
- **Cambiario:** tipo de cambio USD/MXN (Banxico) para productos importados.
- **Referencia oficial:** SNIIM cuando esté disponible (suele estar en mantenimiento).
- **Política comercial:** aranceles y cupos de importación/exportación (DOF, Secretaría de Economía) — afectan directo a productos importados o exportables (aguacate, jitomate, limón).
- **Economía:** inflación de alimentos (INEGI/INPC quincenal), precio del diésel, salario mínimo/programas de apoyo al campo (cambian oferta y demanda).
- **Regulación CEDA/CDMX:** cambios en cuotas, operativos, obras o reglas dentro de la Central (FICEDA, Gobierno CDMX).

**Regla editorial adicional:** en temas políticos y económicos, SOLO hechos con efecto en precios y su dirección esperada. Cero opiniones ni colores partidistas: los clientes son de todas las ideas y la neutralidad es parte del producto.

**Regla editorial:** se reporta el hecho y la dirección esperada ("helada en Sinaloa → presión al alza en jitomate"), NUNCA magnitudes inventadas. Si no hay certeza: "incierto". La credibilidad es el producto.

## 6. Los 10 puntos de "app vendible" — cuándo aplica cada uno

| Punto | ¿Cuándo? |
|---|---|
| Control de versiones (git + GitHub) | **Día 1, siempre.** Commit por cada cambio que funcione. |
| Hosting/deployment (no localhost) | **Día 1** (GitHub Pages/Vercel desde el primer commit). |
| Secretos protegidos (llaves fuera del código, frontend sin source maps) | **Día 1.** Nunca pegar API keys en prompts, commits ni frontend. Variables de entorno siempre. |
| Base de datos con RLS | Fase 2 (cuando existan usuarios y datos ajenos que proteger). |
| APIs bien diseñadas | Fase 2 (antes no hay API; el JSON estático es suficiente). |
| Seguridad (auth, validación de inputs) | Fase 2, junto con las cuentas. |
| Rate limiting | Fase 2–3, al exponer API pública o formulario de aportantes. |
| Caching | Fase 2–3, cuando algo se sienta lento (no antes: es complejidad gratis). |
| Escalabilidad | Fase 3+. Con menos de 1,000 usuarios, Vercel+Supabase escalan solos. |
| Monitoreo (logs, alertas de error) | Básico desde Fase 2 (los logs de Vercel/Supabase bastan al inicio). |

**Lectura correcta:** los 10 puntos son ciertos, pero aplicarlos TODOS en la v1 es la forma más segura de no lanzar nunca. Se aplican por fase; la disciplina de día 1 son solo tres: git, deploy y secretos.

## 7. Reglas para las sesiones de vibe coding

1. Una sesión = una funcionalidad. Definir "qué debe poder hacer el usuario al final" antes de escribir el primer prompt.
2. Probar en el celular después de cada cambio (los clientes solo usan celular).
3. Commit cuando funcione; si algo se rompe, `git revert` en vez de parchar a ciegas.
4. No agregar funciones que ningún cliente pidió. El backlog sale de lo que los clientes digan, no de lo que sea divertido construir.
5. Nunca subir al repo: llaves, `historico_precios.csv` con datos reales de clientes, ni contactos. Usar `.gitignore` desde el día 1.
6. Presupuesto: todo el stack de Fase 1–2 debe costar $0/mes (planes gratis). Si algo pide tarjeta, buscar alternativa.

## 8. Métricas que mandan

Clientes de pago · ingreso recurrente mensual · retención (85%+) · días con captura (90%+). Si una semana de desarrollo no movió ninguna de estas, la siguiente semana es de ventas, no de código.

## 8.5 Aprendizaje de dominio (validado con experto en guayaba)

Algunos productos NO se cotizan con un solo precio min/frec/máx: se cotizan por **escala de calidades**. Guayaba real (caja de 9 kg): madura $50-70, chiquita $100, luego $120, $150, $170, $200, $250 y "la mejor" $270. El campo opcional `escala_calidades: [{calidad, precio}]` en `datos/datos.json` ya guarda esto.

**Backlog inmediato (primeras sesiones de vibe coding):**
1. LÓGICA: que el modelo de datos y el render soporten productos con `escala_calidades` (tarjeta expandible que muestre la escalera de precios por calidad); la variación diaria debe calcularse POR calidad, no por promedio.
2. UX/UI: rediseñar la tarjeta de producto para leerse en 5 segundos en un pasillo oscuro: contraste alto, tipografía grande, la escala de calidades como lista vertical precio-descendente.

## 9. Estado actual del código

- `index.html` — Fase 1: precios del día, mini-gráficas SVG de 7 días (`historial_7d` en el JSON), factores externos, recomendaciones y botón CTA de WhatsApp. Mobile-first, sin dependencias externas.
- `datos/datos.json` — datos de EJEMPLO (reemplazar con datos reales cada madrugada). Cada producto puede llevar `historial_7d: [7 precios]` para la mini-gráfica.
- Pendiente (lo hace José): reemplazar `52XXXXXXXXXX` por su número de WhatsApp en el CTA de `index.html`, crear repo en GitHub y hacer push, activar GitHub Pages o Vercel.
