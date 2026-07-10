# Guía paso a paso desde cero (Mac) — Panorama CEDA

Sigue las partes en orden. Lo de la Parte 0 y 1 se hace UNA sola vez; la Parte 2 es tu rutina de desarrollo y la Parte 3 tu rutina de cada madrugada.

---

## PARTE 0 — Preparar tu computadora (una sola vez, ~20 min)

**0.1 Abre la Terminal:** presiona `Cmd + barra espaciadora`, escribe `Terminal`, Enter.

**0.2 Instala las herramientas de desarrollador de Apple (incluye git):**
```bash
git --version
```
Si aparece una ventana pidiendo instalar "herramientas de línea de comandos", acepta y espera. Si muestra una versión (ej. `git version 2.x`), ya está.

**0.3 Instala Node.js:** ve a https://nodejs.org y descarga la versión **LTS** para macOS. Instálala como cualquier app. Verifica:
```bash
node -v
npm -v
```

**0.4 Identifícate en git (para que los commits lleven tu nombre):**
```bash
git config --global user.name "Jose"
git config --global user.email "hugov7060@gmail.com"
```

**0.5 Instala Claude Code:**
```bash
npm install -g @anthropic-ai/claude-code
```
Luego escribe `claude` y sigue las instrucciones para iniciar sesión con tu cuenta de Claude. Sal con `Ctrl+C` o escribiendo `/exit`.

**0.6 Instala Blackbox CLI:**
```bash
curl -fsSL https://blackbox.ai/install.sh | bash
```
Cierra y vuelve a abrir la Terminal. Luego configura tu llave (te la da el Dashboard de blackbox.ai al crear cuenta):
```bash
blackbox configure
```
Documentación oficial: https://docs.blackbox.ai/features/blackbox-cli/getting-started/

> Si algún comando dice "command not found" después de instalar: cierra la Terminal y ábrela de nuevo.

---

## PARTE 1 — Subir el proyecto a GitHub (una sola vez, ~15 min)

**1.1** Crea tu cuenta en https://github.com (si no tienes).

**1.2** En GitHub: botón **New repository** → nombre: `panorama-ceda` → **Public** (necesario para GitHub Pages gratis) → NO marques "Add README" → **Create repository**.

**1.3** En la Terminal:
```bash
cd ~/Desktop/PROYECT\ CEDA
git remote add origin https://github.com/TU-USUARIO/panorama-ceda.git
git branch -M main
git push -u origin main
```
(Cambia `TU-USUARIO` por tu usuario real. GitHub te pedirá iniciar sesión la primera vez.)

**1.4 Activa GitHub Pages:** en el repo → **Settings** → **Pages** → Source: `Deploy from a branch` → Branch: `main` / carpeta `/ (root)` → **Save**. En 2-5 minutos tu app vive en:
`https://TU-USUARIO.github.io/panorama-ceda/`

Ese link se abre en cualquier celular. Guárdalo: es el que compartes por WhatsApp.

---

## PARTE 2 — Rutina de desarrollo (cada sesión de vibe coding)

**Regla: una sesión = una funcionalidad.** El backlog vive en `CLAUDE.md` §8.5.

**2.1** Abre la Terminal y entra al proyecto:
```bash
cd ~/Desktop/PROYECT\ CEDA
```

**2.2** Arranca tu agente:
- Claude Code: `claude` (lee CLAUDE.md automáticamente)
- Blackbox: `blackbox` (NO lee CLAUDE.md solo → tu primer mensaje siempre empieza con "Lee CLAUDE.md")

**2.3** Dale UN objetivo. Los dos primeros ya están definidos:

*Sesión 1 — Lógica (escala de calidades):*
> Lee CLAUDE.md completo, en especial la sección 8.5. Implementa en index.html el soporte para productos con `escala_calidades` (ya existe en datos/datos.json para guayaba): la tarjeta debe mostrar la escalera de precios por calidad, ordenada de mayor a menor, y el encabezado debe decir el rango ($50–$270) en vez de un solo precio frecuente. No rompas los productos que no tienen escala. Prueba con datos/datos.json y no toques nada más.

*Sesión 2 — UX/UI (lectura en pasillo oscuro):*
> Lee CLAUDE.md, sección 8.5 punto 2. Rediseña la tarjeta de producto para leerse en 5 segundos en un pasillo oscuro a las 5 am: contraste alto, tipografía grande, modo oscuro. Mobile-first, sin librerías externas. Todo en index.html.

**2.4** Prueba en tu celular ANTES de dar por buena la sesión:
```bash
python3 -m http.server 8000
```
En tu celular (misma red WiFi): `http://IP-DE-TU-MAC:8000` (la IP está en Ajustes del Sistema → Wi-Fi → Detalles). Para detener el servidor: `Ctrl+C`.

**2.5** Si funciona, guarda y publica:
```bash
git add -A
git commit -m "describe qué hiciste"
git push
```
El push actualiza automáticamente tu página de GitHub Pages en ~1 minuto.

**2.6** Si algo se rompió y no sabes por qué:
```bash
git checkout -- .
```
(regresa todo al último commit que funcionaba; se pierde solo lo no guardado).

---

## PARTE 3 — Rutina de cada madrugada (operación del negocio)

1. Captura tus precios en la Central (libreta, nota de voz o foto).
2. En Claude (app o Cowork), usa la skill **analista-ceda**: pásale la captura y pídele el Reporte CEDA por cliente + el `datos.json` actualizado.
3. Reemplaza el contenido de `datos/datos.json` con el nuevo y publica:
```bash
cd ~/Desktop/PROYECT\ CEDA
git add datos/datos.json && git commit -m "datos $(date +%F)" && git push
```
4. Manda los reportes por WhatsApp antes de las 6:00 am. **Esto es el negocio; la app es el escaparate.**

---

## Pendientes de una sola vez

- [ ] Reemplazar `52XXXXXXXXXX` por tu WhatsApp real en `index.html` (botón CTA).
- [ ] Parte 0 completa (herramientas instaladas).
- [ ] Parte 1 completa (repo en GitHub + Pages activo).
- [ ] Sesión 1 y 2 del backlog hechas y probadas en celular.
