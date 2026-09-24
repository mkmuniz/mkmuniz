"""Gera a skin 64x64 (formato Minecraft) do avatar do mkmuniz.

Nada de editor de imagem: cada face do boneco e' desenhada como pixel art
em texto, com um mapa de caractere -> cor. Mexer no boneco = mexer aqui.
"""
from PIL import Image

# ---------------------------------------------------------------- paleta ----
PALETTE = {
    ".": (0, 0, 0, 0),          # transparente
    "S": (217, 160, 102, 255),  # pele
    "s": (184, 122, 75, 255),   # pele (sombra)
    "H": (43, 33, 24, 255),     # cabelo
    "h": (61, 48, 37, 255),     # cabelo (brilho)
    "E": (242, 245, 248, 255),  # esclera
    "P": (59, 42, 30, 255),     # pupila
    "M": (138, 75, 60, 255),    # boca
    "D": (31, 59, 99, 255),     # moletom (escuro / capuz)
    "B": (45, 95, 168, 255),    # moletom (azul TypeScript)
    "C": (97, 218, 251, 255),   # ciano React
    "c": (171, 235, 252, 255),  # ciano (facetas claras)
    "W": (232, 238, 245, 255),  # cordao do capuz
    "J": (55, 65, 92, 255),     # jeans
    "K": (26, 28, 34, 255),     # tenis
    "G": (40, 43, 50, 255),     # fone de ouvido (casco)
    "g": (74, 79, 90, 255),     # fone de ouvido (espuma)
}

T = "........"   # atalho: linha 8px transparente
T4 = "...."

# ------------------------------------------------------------ desenho 3D ----
# Cada peca tem origem (U,V) no atlas e as 6 faces em pixel art.
# Ordem das faces segue o layout padrao de skin do Minecraft.

HEAD = dict(U=0, V=0, W=8, H=8, D=8, faces={
    "front": ["HHHHHHHH", "HHHHHHHH", "HSSSSSSH", "SSSSSSSS",
              "SEPSSPES", "SSSSSSSS", "SSSMMSSS", "SSSSSSSS"],
    "back":  ["HHHHHHHH", "HHHHHHHH", "HHHHHHHH", "HHHHHHHH",
              "HHhHHhHH", "HHHHHHHH", "SHHHHHHS", "SSHHHHSS"],
    "right": ["HHHHHHHH", "HHHHHHHH", "HHHHHSSS", "HHHSSSSS",
              "HHSSSSSS", "HHSSSSSS", "HHsSSSSS", "HHsSSSSS"],
    "left":  ["HHHHHHHH", "HHHHHHHH", "SSSHHHHH", "SSSSSHHH",
              "SSSSSSHH", "SSSSSSHH", "SSSSSsHH", "SSSSSsHH"],
    "top":   ["HHHHHHHH", "HhhhhhhH", "HhHHHHhH", "HHHHHHHH",
              "HHHHHHHH", "HhHHHHhH", "HhhhhhhH", "HHHHHHHH"],
    "bottom": ["ssssssss"] * 8,
})

# camada "chapeu": cabelo com volume + fone de ouvido
HAT = dict(U=32, V=0, W=8, H=8, D=8, faces={
    "front": ["HHHHHHHH", "HHHHHHHH", T, T, T, T, T, T],
    "back":  ["HHHHHHHH", "HHHHHHHH", "HHHHHHHH", T, T, T, T, T],
    "right": ["HHHHHHHH", "HHHGGHHH", "..GGGG..", ".GCCCCG.",
              ".GCggCG.", ".GCCCCG.", "..GGGG..", T],
    "left":  ["HHHHHHHH", "HHHGGHHH", "..GGGG..", ".GCCCCG.",
              ".GCggCG.", ".GCCCCG.", "..GGGG..", T],
    "top":   ["HHHHHHHH", "HHHHHHHH", "HHHHHHHH", "GGGGGGGG",
              "GGGGGGGG", "HHHHHHHH", "HHHHHHHH", "HHHHHHHH"],
    "bottom": [T] * 8,
})

BODY = dict(U=16, V=16, W=8, H=12, D=4, faces={
    "front": ["DDDDDDDD", "BDDDDDDB", "BBDWWDBB", "BBBWWBBB",
              "BBBCCBBB", "BBCcCCBB", "BCcCCCCB", "BBCCCCBB",
              "BBBCCBBB", "BDDDDDDB", "BDDDDDDB", "BBBBBBBB"],
    "back":  ["DDDDDDDD", "DDDDDDDD", "DDDDDDDD", "BDDDDDDB",
              "BBBBBBBB", "BBBBBBBB", "BBBBBBBB", "BBBBBBBB",
              "BBBBBBBB", "BBBBBBBB", "BBBBBBBB", "DDDDDDDD"],
    "right": ["DDDD", "DDDD", "BBBB", "BBBB", "BBBB", "BBBB",
              "BBBB", "BBBB", "BBBB", "BBBB", "BBBB", "DDDD"],
    "left":  ["DDDD", "DDDD", "BBBB", "BBBB", "BBBB", "BBBB",
              "BBBB", "BBBB", "BBBB", "BBBB", "BBBB", "DDDD"],
    "top":   ["DDDDDDDD"] * 4,
    "bottom": ["BBBBBBBB"] * 4,
})

# capuz caido nas costas (camada extra do torso)
JACKET = dict(U=16, V=32, W=8, H=12, D=4, faces={
    "front": [T] * 12,
    "back":  ["DDDDDDDD", "DDDDDDDD", "DDDDDDDD", "DDDDDDDD"] + [T] * 8,
    "right": ["DDDD", "DDDD", "DDDD", "DDDD"] + [T4] * 8,
    "left":  ["DDDD", "DDDD", "DDDD", "DDDD"] + [T4] * 8,
    "top":   ["DDDDDDDD"] * 4,
    "bottom": [T] * 4,
})

_ARM = ["BBBB"] * 9 + ["DDDD", "SSSS", "SSSS"]
ARM_R = dict(U=40, V=16, W=4, H=12, D=4, faces={
    "front": _ARM, "back": _ARM, "right": _ARM, "left": _ARM,
    "top": ["BBBB"] * 4, "bottom": ["SSSS"] * 4,
})
ARM_L = dict(ARM_R, U=32, V=48)

_LEG = ["JJJJ"] * 10 + ["KKKK", "KKKK"]
LEG_R = dict(U=0, V=16, W=4, H=12, D=4, faces={
    "front": _LEG, "back": _LEG, "right": _LEG, "left": _LEG,
    "top": ["JJJJ"] * 4, "bottom": ["KKKK"] * 4,
})
LEG_L = dict(LEG_R, U=16, V=48)

PARTS = [HEAD, HAT, BODY, JACKET, ARM_R, ARM_L, LEG_R, LEG_L]


def _rect(part, face):
    """Retangulo (x, y, w, h) da face no atlas, layout padrao do Minecraft."""
    U, V, W, H, D = part["U"], part["V"], part["W"], part["H"], part["D"]
    return {
        "top":    (U + D,         V,     W, D),
        "bottom": (U + D + W,     V,     W, D),
        "right":  (U,             V + D, D, H),
        "front":  (U + D,         V + D, W, H),
        "left":   (U + D + W,     V + D, D, H),
        "back":   (U + 2 * D + W, V + D, W, H),
    }[face]


def build():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    px = img.load()
    for part in PARTS:
        for face, rows in part["faces"].items():
            x0, y0, w, h = _rect(part, face)
            assert len(rows) == h, f"{face}: {len(rows)} linhas, esperado {h}"
            for dy, row in enumerate(rows):
                assert len(row) == w, f"{face} linha {dy}: {len(row)} != {w}"
                for dx, ch in enumerate(row):
                    px[x0 + dx, y0 + dy] = PALETTE[ch]
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "skin.png"
    build().save(out)
    print("skin ->", out)
