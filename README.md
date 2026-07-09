# Panorama CEDA

Inteligencia de precios de la Central de Abasto para locatarios y compradores mayoristas. Ver `CLAUDE.md` para el contexto completo del proyecto (Claude Code lo lee automáticamente).

## Ver la app en tu computadora

```bash
cd "PROYECT CEDA"
python3 -m http.server 8000
# abre http://localhost:8000 en el navegador (o en el celular, misma red: http://TU-IP:8000)
```

## Actualizar los datos de cada madrugada

Edita `datos/datos.json` (o pídele a la skill `analista-ceda` que lo genere desde tu captura del día) y sube el cambio:

```bash
git add datos/datos.json && git commit -m "datos $(date +%F)" && git push
```

## Subir a GitHub por primera vez (una sola vez)

1. Crea una cuenta en github.com si no tienes.
2. Crea un repositorio nuevo llamado `panorama-ceda` (privado por ahora).
3. En la terminal, dentro de esta carpeta:

```bash
git init
git add .
git commit -m "Versión inicial: Fase 1 Panorama CEDA"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/panorama-ceda.git
git push -u origin main
```

## Publicar gratis (GitHub Pages)

En el repositorio: Settings → Pages → Source: `main` → Save. En unos minutos tu app queda en `https://TU-USUARIO.github.io/panorama-ceda/`. **Nota:** Pages requiere repo público; si prefieres privado, usa Vercel (gratis, importa el repo y listo).

## Trabajar con Claude Code

```bash
cd "PROYECT CEDA"
claude
```

Claude Code leerá `CLAUDE.md` solo. Primer prompt sugerido:
> "Lee CLAUDE.md. Revisa index.html (Fase 1) y mejóralo: agrega mini-gráficas de tendencia de 7 días por producto usando los datos históricos que te pasaré."

## Reglas de oro

- Nunca subas al repo: llaves/API keys, `historico_precios.csv` real, ni contactos de clientes (ya están en `.gitignore`).
- Commit cada vez que algo funcione.
- La app no sustituye la venta: el reporte por WhatsApp sigue siendo el producto principal.
