"""Renderizador 3D proprio para o avatar (sem API externa, sem engine).

Raycasting ortografico contra caixas orientadas (as partes do boneco),
amostrando a skin 64x64 com o mesmo mapeamento de UV do Minecraft.
Saida: um PNG estatico e um GIF girando 360 graus, ambos com fundo
transparente para funcionarem no tema claro e no tema escuro do GitHub.
"""
import math
import numpy as np
from PIL import Image

import skin as skinmod

SS = 2                      # supersampling (anti-aliasing)
LIGHT = np.array([-0.35, 0.80, 0.45])
LIGHT /= np.linalg.norm(LIGHT)
SHADE_LEVELS = 6            # degraus de luz (mantem a paleta do GIF pequena)


# ------------------------------------------------------------------ util ----
def roty(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rotx(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


class Box:
    """Uma parte do boneco: caixa com textura e transformacao propria."""

    def __init__(self, part, size, corner, inflate=0.0, rot=None, pivot=None):
        self.part = part
        self.size = np.array(size, float) + 2 * inflate
        corner = np.array(corner, float) - inflate
        rot = np.eye(3) if rot is None else rot
        pivot = np.array(pivot, float) if pivot is not None else np.zeros(3)
        self.R = rot
        self.T = corner + pivot - rot @ pivot

    def apply(self, M, offset=np.zeros(3)):
        b = Box.__new__(Box)
        b.part, b.size = self.part, self.size
        b.R, b.T = M @ self.R, M @ self.T + offset
        return b


# --------------------------------------------------------------- modelo ----
def model(t):
    """t em [0,1): fase do idle. Devolve as caixas ja posicionadas."""
    swing = math.radians(11) * math.sin(2 * math.pi * t)
    bob = 0.22 * math.sin(4 * math.pi * t)
    tilt = math.radians(3.5) * math.sin(2 * math.pi * t + 0.7)

    head_rot = rotx(-tilt) @ roty(math.radians(7) * math.sin(2 * math.pi * t))
    parts = [
        # cabeca + camada do cabelo/fone, girando no pescoco
        Box(skinmod.HEAD, (8, 8, 8), (-4, 24, -4), rot=head_rot, pivot=(4, 0, 4)),
        Box(skinmod.HAT, (8, 8, 8), (-4, 24, -4), inflate=0.55,
            rot=head_rot, pivot=(4.55, 0.55, 4.55)),
        # torso + capuz
        Box(skinmod.BODY, (8, 12, 4), (-4, 12, -2)),
        Box(skinmod.JACKET, (8, 12, 4), (-4, 12, -2), inflate=0.26),
        # bracos balancando no ombro
        Box(skinmod.ARM_R, (4, 12, 4), (-8, 12, -2),
            rot=rotx(swing), pivot=(2, 12, 2)),
        Box(skinmod.ARM_L, (4, 12, 4), (4, 12, -2),
            rot=rotx(-swing), pivot=(2, 12, 2)),
        # pernas em contratempo com os bracos
        Box(skinmod.LEG_R, (4, 12, 4), (-4, 0, -2),
            rot=rotx(-swing * 0.55), pivot=(2, 12, 2)),
        Box(skinmod.LEG_L, (4, 12, 4), (0, 0, -2),
            rot=rotx(swing * 0.55), pivot=(2, 12, 2)),
    ]
    return parts, bob


# ------------------------------------------------------------------ UV ------
def sample(part, axis, positive, a, tex):
    """a: coords normalizadas (N,3) dentro da caixa -> cor RGBA (N,4)."""
    U, V = part["U"], part["V"]
    W, H, D = part["W"], part["H"], part["D"]
    ax, ay, az = a[:, 0], a[:, 1], a[:, 2]
    if axis == 0:
        tx = np.where(positive, U + D + W + (1 - az) * D, U + az * D)
        ty = V + D + (1 - ay) * H
    elif axis == 1:
        tx = np.where(positive, U + D + ax * W, U + D + W + ax * W)
        ty = np.where(positive, V + (1 - az) * D, V + az * D)
    else:
        tx = np.where(positive, U + D + ax * W, U + 2 * D + W + (1 - ax) * W)
        ty = V + D + (1 - ay) * H
    xi = np.clip(tx.astype(int), 0, 63)
    yi = np.clip(ty.astype(int), 0, 63)
    return tex[yi, xi]


# -------------------------------------------------------------- raycast ----
def screen_window(box, target, right, up, half_v, w, h):
    """Retangulo de pixels que a caixa pode cobrir (culling em espaco de tela)."""
    sx, sy, sz = box.size
    corners = np.array([[x, y, z] for x in (0, sx) for y in (0, sy) for z in (0, sz)])
    world = corners @ box.R.T + box.T
    rel = world - target
    px = (rel @ right) / (2 * half_v) + 0.5
    py = 0.5 - (rel @ up) / (2 * half_v)
    x0 = max(int(np.floor(px.min() * w)) - 1, 0)
    x1 = min(int(np.ceil(px.max() * w)) + 1, w)
    y0 = max(int(np.floor(py.min() * h)) - 1, 0)
    y1 = min(int(np.ceil(py.max() * h)) + 1, h)
    return x0, x1, y0, y1


def trace(boxes, ro, rd, tex, w, h, target, right, up, half_v):
    """Um raio ortografico por pixel; z-buffer incremental, so no recorte
    de tela de cada parte do boneco."""
    n = w * h
    big = np.float32(1e9)
    np.seterr(all="ignore")   # raios paralelos a uma face geram inf/nan inofensivos
    best_t = np.full(n, big, np.float32)
    best_col = np.zeros((n, 3), np.float32)
    best_nrm = np.zeros((n, 3), np.float32)
    rows = np.arange(h)[:, None] * w

    for box in boxes:
        x0, x1, y0, y1 = screen_window(box, target, right, up, half_v, w, h)
        if x1 <= x0 or y1 <= y0:
            continue
        idx = (rows[y0:y1] + np.arange(x0, x1)).ravel()

        size = box.size.astype(np.float32)
        ld = (box.R.T @ rd).astype(np.float32)
        lo = ((ro[idx] - box.T) @ box.R).astype(np.float32)
        with np.errstate(divide="ignore", invalid="ignore"):
            inv = (1.0 / np.where(np.abs(ld) < 1e-12, 1e-12, ld)).astype(np.float32)
        tn = np.minimum((0.0 - lo) * inv, (size - lo) * inv)
        tf = np.maximum((0.0 - lo) * inv, (size - lo) * inv)
        tmin = tn.max(axis=1)
        cand = (tf.min(axis=1) >= np.maximum(tmin, 0)) & (tf.min(axis=1) > 0)
        cand &= tmin < best_t[idx]
        if not cand.any():
            continue

        axis = tn.argmax(axis=1)
        a = np.clip((lo + tmin[:, None] * ld) / size, 0, 1)
        for ax in range(3):
            m = cand & (axis == ax)
            if not m.any():
                continue
            pos = bool(ld[ax] < 0)          # entramos pela face "alta"
            rgba = sample(box.part, ax, pos, a[m], tex)
            solid = rgba[:, 3] > 0
            if not solid.any():
                continue
            local = np.flatnonzero(m)[solid]
            g = idx[local]
            best_t[g] = tmin[local]
            best_col[g] = rgba[solid, :3]
            ln = np.zeros(3)
            ln[ax] = 1.0 if pos else -1.0
            best_nrm[g] = box.R @ ln

    vis = best_t < big
    lam = np.clip(best_nrm @ LIGHT.astype(np.float32), 0, 1)
    shade = np.round((0.52 + 0.48 * lam) * SHADE_LEVELS) / SHADE_LEVELS
    return np.clip(best_col * shade[:, None], 0, 255), vis.astype(np.float32)


# ---------------------------------------------------------------- camera ----
def frame(size, yaw, phase, tex, pitch=17.0, zoom=37.0):
    w = h = size * SS
    p = math.radians(pitch)
    d = np.array([0.0, -math.sin(p), -math.cos(p)])
    right = np.array([1.0, 0.0, 0.0])
    up = np.cross(right, d)

    half_v = zoom / 2
    sx = ((np.arange(w) + 0.5) / w - 0.5) * 2 * half_v
    sy = (0.5 - (np.arange(h) + 0.5) / h) * 2 * half_v
    gx, gy = np.meshgrid(sx, sy)
    target = np.array([0.0, 16.4, 0.0])
    ro = (target - d * 200.0
          + gx.reshape(-1, 1) * right + gy.reshape(-1, 1) * up).astype(np.float32)

    boxes, bob = model(phase)
    M = roty(yaw)
    boxes = [b.apply(M, np.array([0.0, bob, 0.0])) for b in boxes]

    rgb, a = trace(boxes, ro, d, tex, w, h, target, right, up, half_v)
    rgb = rgb.reshape(h, w, 3)
    a = a.reshape(h, w)

    # downsample com media ponderada por alpha (evita halo na borda)
    rgb = rgb.reshape(size, SS, size, SS, 3).transpose(0, 2, 1, 3, 4)
    aa = a.reshape(size, SS, size, SS).transpose(0, 2, 1, 3)
    wsum = aa.sum(axis=(2, 3))
    num = (rgb * aa[..., None]).sum(axis=(2, 3))
    out = np.where(wsum[..., None] > 0, num / np.maximum(wsum, 1e-9)[..., None], 0)
    return out.astype(np.uint8), wsum / (SS * SS)


# ------------------------------------------------------------------ saida ---
def to_rgba(rgb, cov):
    a = (np.clip(cov, 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(np.dstack([rgb, a]))


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "assets")
    tex_img = skinmod.build()
    tex_img.save(os.path.join(out, "mkmuniz-skin.png"))
    tex = np.array(tex_img)

    # 1) retrato estatico em 3/4
    rgb, cov = frame(560, math.radians(-32), 0.13, tex, pitch=15, zoom=36)
    to_rgba(rgb, cov).save(os.path.join(out, "mkmuniz-hero.png"))

    # 2) GIF girando 360 graus
    n, size = 36, 400
    frames, masks = [], []
    for i in range(n):
        rgb, cov = frame(size, 2 * math.pi * i / n, i / n, tex, zoom=34)
        frames.append(rgb)
        masks.append(cov < 0.45)
        print(f"  frame {i + 1}/{n}", end="\r")
    print()

    # paleta global unica: sem flicker entre frames e arquivo menor
    montage = Image.fromarray(np.concatenate(frames, axis=1), "RGB")
    pal = montage.quantize(colors=255, method=Image.MEDIANCUT)

    gif = []
    for rgb, mask in zip(frames, masks):
        q = Image.fromarray(rgb, "RGB").quantize(palette=pal, dither=Image.NONE)
        arr = np.array(q)
        arr[mask] = 255                     # indice 255 = transparente
        f = Image.fromarray(arr, "P")
        f.putpalette(pal.getpalette())
        gif.append(f)

    gif[0].save(os.path.join(out, "mkmuniz-3d.gif"), save_all=True,
                append_images=gif[1:], duration=80, loop=0,
                transparency=255, disposal=2, optimize=False)
    print("ok ->", os.path.abspath(out))


if __name__ == "__main__":
    main()
