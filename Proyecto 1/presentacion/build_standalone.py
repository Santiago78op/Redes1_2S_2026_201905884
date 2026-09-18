# -*- coding: utf-8 -*-
"""
Empaqueta un deck reveal.js en UN solo archivo autocontenido (skill deck-apple).

Uso:  python build_standalone.py <deck.html>
Produce <deck>-standalone.html junto al original, con:
  - <link rel="stylesheet" href="reveal/...">  -> <style> inline
  - <script src="reveal/..."></script>         -> <script> inline
  - toda <img src="..."> relativa              -> data URI base64

El resultado abre con doble clic en cualquier máquina, sin repo ni internet
(las Google Fonts degradan a la pila de respaldo si no hay red).
Regenerar tras CADA edición del deck o del tema — el standalone no se edita a mano.
"""
import base64
import re
import sys
import urllib.parse
from pathlib import Path

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".svg": "image/svg+xml", ".webp": "image/webp", ".gif": "image/gif"}


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python build_standalone.py <deck.html>")
    fuente = Path(sys.argv[1]).resolve()
    base = fuente.parent
    salida = fuente.with_name(fuente.stem + "-standalone.html")
    html = fuente.read_text(encoding="utf-8")

    def inline_css(m):
        css = (base / m.group(1)).read_text(encoding="utf-8")
        return f"<style>\n/* === inline: {m.group(1)} === */\n{css}\n</style>"

    def inline_js(m):
        js = (base / m.group(1)).read_text(encoding="utf-8")
        return f"<script>\n/* === inline: {m.group(1)} === */\n{js}\n</script>"

    faltantes = []

    def inline_img(m):
        rel = urllib.parse.unquote(m.group(1))
        ruta = (base / rel).resolve()
        if not ruta.exists():
            faltantes.append(rel)
            return m.group(0)
        datos = base64.b64encode(ruta.read_bytes()).decode("ascii")
        mime = MIME.get(ruta.suffix.lower(), "application/octet-stream")
        return f'src="data:{mime};base64,{datos}"'

    html = re.sub(r'<link rel="stylesheet" href="((?!https?:)[^"]+)">', inline_css, html)
    html = re.sub(r'<script src="((?!https?:)[^"]+)"></script>', inline_js, html)
    html = re.sub(r'src="((?!data:|https?:)[^"]+\.(?:png|jpe?g|svg|webp|gif))"',
                  inline_img, html, flags=re.I)
    if faltantes:
        raise SystemExit(f"Imágenes no encontradas: {faltantes}")

    html = html.replace(
        "<title>",
        "<!-- GENERADO por build_standalone.py — editar el deck fuente y regenerar -->\n  <title>",
        1,
    )
    salida.write_text(html, encoding="utf-8")
    print(f"OK -> {salida.name}: {salida.stat().st_size / 1024:,.0f} KB")


if __name__ == "__main__":
    main()
