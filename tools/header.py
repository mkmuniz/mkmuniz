"""Gera o header animado do README (SVG com SMIL, sem CSS e sem JS).

O GitHub remove <script>, <style> e o atributo style de qualquer coisa que
chega no README, mas mantem SMIL (<animate>, <animateTransform>) dentro de um
SVG servido como imagem. Entao toda a animacao aqui e SMIL puro.

Estetica: CRT/scanline (Serial Experiments Lain), teal da Miku e azul gelido
da Ellen Joe. Arte original -- nenhuma personagem e reproduzida.
"""
W, H = 880, 210

BG    = "#080B11"
TEAL  = "#39C5BB"   # Hatsune Miku
ICE   = "#A8D8E8"   # Ellen Joe
RED   = "#E0533D"   # glitch da Lain
AMBER = "#D98E2B"
DIM   = "#5A6B80"
WHITE = "#DCEEF5"

MONO = "ui-monospace,'SF Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"


def flicker(dur="7s", lo="0.55", hi="1"):
    return (f'<animate attributeName="opacity" calcMode="discrete" dur="{dur}" '
            f'repeatCount="indefinite" keyTimes="0;.48;.5;.52;.54;.9;.92;1" '
            f'values="{hi};{hi};{lo};{hi};{lo};{hi};{lo};{hi}"/>')


def build():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Mikael Muniz - software engineer">']

    # ---- fundo + vinheta ------------------------------------------------
    o.append('<defs>')
    o.append(f'<linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{TEAL}" stop-opacity="0"/>'
             f'<stop offset=".5" stop-color="{TEAL}" stop-opacity=".16"/>'
             f'<stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></linearGradient>')
    o.append(f'<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{TEAL}" stop-opacity="0"/>'
             f'<stop offset=".5" stop-color="{TEAL}" stop-opacity=".9"/>'
             f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>')
    o.append('</defs>')
    o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    # ---- grade "wired" --------------------------------------------------
    g = [f'<g stroke="{TEAL}" stroke-width="1" opacity=".07">']
    for x in range(0, W + 1, 44):
        g.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>')
    for y in range(0, H + 1, 44):
        g.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
    g.append('</g>')
    o.append("".join(g))

    # ---- scanlines de CRT, com deriva lenta ------------------------------
    s = ['<g opacity=".5">',
         f'<g fill="{ICE}" opacity=".055">']
    for y in range(0, H + 8, 4):
        s.append(f'<rect x="0" y="{y}" width="{W}" height="1.6"/>')
    s.append('<animateTransform attributeName="transform" type="translate" '
             'values="0 0;0 4" dur="1.1s" repeatCount="indefinite"/>')
    s.append('</g></g>')
    o.append("".join(s))

    # varredura do tubo descendo
    o.append(f'<rect x="0" y="-70" width="{W}" height="70" fill="url(#sweep)">'
             f'<animate attributeName="y" from="-70" to="{H}" dur="4.5s" '
             f'repeatCount="indefinite"/></rect>')

    # ---- cantos de HUD ---------------------------------------------------
    c = 22
    for (px, py, sx, sy) in ((16, 16, 1, 1), (W - 16, 16, -1, 1),
                             (16, H - 16, 1, -1), (W - 16, H - 16, -1, -1)):
        o.append(f'<path d="M{px} {py + sy * c} L{px} {py} L{px + sx * c} {py}" '
                 f'fill="none" stroke="{TEAL}" stroke-width="2" opacity=".65"/>')

    # ---- nome, com aberracao cromatica -----------------------------------
    NAME, cx, by = "MIKAEL MUNIZ", W / 2, 118
    base = (f'font-family="{MONO}" font-size="52" font-weight="700" '
            f'letter-spacing="7" text-anchor="middle"')
    glitch = ('<animateTransform attributeName="transform" type="translate" '
              'calcMode="discrete" dur="6s" repeatCount="indefinite" '
              'keyTimes="0;.31;.33;.35;.37;.72;.74;.76;1" '
              'values="{a};{b};{c};{b};{a};{c};{b};{c};{a}"/>')
    o.append(f'<g opacity=".85"><text x="{cx}" y="{by}" {base} fill="{RED}">{NAME}</text>'
             + glitch.format(a="-1.5 0", b="-5 0", c="3 -1") + '</g>')
    o.append(f'<g opacity=".85"><text x="{cx}" y="{by}" {base} fill="{TEAL}">{NAME}</text>'
             + glitch.format(a="1.5 0", b="5 0", c="-3 1") + '</g>')
    for sw, op in ((9, ".05"), (6, ".08"), (3, ".13")):
        o.append(f'<text x="{cx}" y="{by}" {base} fill="none" stroke="{TEAL}" '
                 f'stroke-width="{sw}" opacity="{op}">{NAME}</text>')
    o.append(f'<text x="{cx}" y="{by}" {base} fill="{WHITE}">{NAME}{flicker()}</text>')

    # ---- subtitulo + cursor ----------------------------------------------
    sub = "SOFTWARE ENGINEER &#183; S&#195;O PAULO &#183; BR"
    o.append(f'<text x="{cx}" y="150" font-family="{MONO}" font-size="14" '
             f'letter-spacing="5" text-anchor="middle" fill="{DIM}">{sub}</text>')
    o.append(f'<rect x="{cx + 244}" y="139" width="9" height="15" fill="{TEAL}">'
             f'<animate attributeName="opacity" values="1;1;0;0" dur="1.06s" '
             f'calcMode="discrete" repeatCount="indefinite"/></rect>')

    # ---- linha viva + ponto correndo --------------------------------------
    o.append(f'<rect x="90" y="172" width="{W - 180}" height="1.5" fill="url(#rule)"/>')
    o.append(f'<circle cy="172.7" r="3" fill="{TEAL}">'
             f'<animate attributeName="cx" values="90;{W - 90};90" dur="9s" '
             f'repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" '
             f'keySplines=".45 0 .55 1;.45 0 .55 1"/></circle>')

    # ---- aceno a Lain, piscando no canto ----------------------------------
    o.append(f'<text x="34" y="46" font-family="{MONO}" font-size="10.5" '
             f'letter-spacing="3" fill="{AMBER}" opacity=".8">'
             f'PRESENT DAY &#160;&#160;PRESENT TIME{flicker("5s", ".2")}</text>')
    o.append(f'<text x="{W - 34}" y="46" font-family="{MONO}" font-size="10.5" '
             f'letter-spacing="3" text-anchor="end" fill="{ICE}" opacity=".55">'
             f'[ CONNECTED ]</text>')

    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    import os, sys
    dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "assets", "header.svg")
    open(dst, "w").write(build())
    print("header ->", os.path.abspath(dst))
