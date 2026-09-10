"""Regenere icon-192.png et icon-512.png a partir de l'arbre du site
(arbre-separateur.png, relevé sur les-ailes-de-flo.com) : arbre crème sur le
fond vert de la charte. Decodage + encodage PNG maison, sans Pillow.

Lancer depuis ce dossier :  python icones.py
"""
import os, struct, zlib

DOSSIER = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(DOSSIER, "arbre-separateur.png")
VERT = (0x4F, 0x64, 0x50)     # #4F6450 vert charte
CREME = (0xF8, 0xF6, 0xF1)    # #F8F6F1 creme
HAUTEUR_REL = 0.74            # hauteur de l'arbre = 74% de l'icone
N = 4                         # sous-echantillons par axe (anticrenelage)


def decoder_png_rgba(chemin):
    d = open(chemin, "rb").read()
    assert d[:8] == b"\x89PNG\r\n\x1a\n"
    w, h, bit, ctype = struct.unpack(">IIBB", d[16:26])
    assert bit == 8 and ctype == 6, ("attendu RGBA 8 bits", bit, ctype)
    idat = bytearray()
    i = 8
    while i < len(d):
        ln = struct.unpack(">I", d[i:i+4])[0]
        typ = d[i+4:i+8]
        if typ == b"IDAT":
            idat += d[i+8:i+8+ln]
        i += 12 + ln
        if typ == b"IEND":
            break
    brut = zlib.decompress(bytes(idat))
    bpp, stride = 4, w * 4
    prev = bytearray(stride)
    alpha = []
    pos = 0
    for y in range(h):
        f = brut[pos]; pos += 1
        ligne = bytearray(brut[pos:pos+stride]); pos += stride
        if f == 1:
            for x in range(bpp, stride):
                ligne[x] = (ligne[x] + ligne[x-bpp]) & 255
        elif f == 2:
            for x in range(stride):
                ligne[x] = (ligne[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = ligne[x-bpp] if x >= bpp else 0
                ligne[x] = (ligne[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = ligne[x-bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x-bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                ligne[x] = (ligne[x] + pr) & 255
        alpha.append([ligne[x*4+3] for x in range(w)])
        prev = ligne
    return w, h, alpha


def morceau(nom, data):
    return struct.pack(">I", len(data)) + nom + data + struct.pack(">I", zlib.crc32(nom+data) & 0xFFFFFFFF)


def ecrire_png_rgb(chemin, taille, lignes):
    brut = b"".join(b"\x00" + bytes(l) for l in lignes)
    png = b"\x89PNG\r\n\x1a\n"
    png += morceau(b"IHDR", struct.pack(">IIBBBBB", taille, taille, 8, 2, 0, 0, 0))
    png += morceau(b"IDAT", zlib.compress(brut, 9))
    png += morceau(b"IEND", b"")
    open(chemin, "wb").write(png)
    print(chemin, os.path.getsize(chemin), "octets")


def fabriquer(taille, sw, sh, alpha):
    th = taille * HAUTEUR_REL
    scale = th / sh
    ox = (taille - sw * scale) / 2.0
    oy = (taille - th) / 2.0
    lignes = []
    for dy in range(taille):
        ligne = bytearray(taille * 3)
        for dx in range(taille):
            acc = 0
            for sy in range(N):
                fy = (dy + (sy + 0.5) / N - oy) / scale
                if fy < 0 or fy >= sh:
                    continue
                row = alpha[int(fy)]
                for sx in range(N):
                    fx = (dx + (sx + 0.5) / N - ox) / scale
                    if 0 <= fx < sw:
                        acc += row[int(fx)]
            cov = acc / (N * N * 255.0)
            cov = 0.0 if cov < 0 else (1.0 if cov > 1 else cov)
            o = dx * 3
            ligne[o]   = int(round(VERT[0] * (1-cov) + CREME[0] * cov))
            ligne[o+1] = int(round(VERT[1] * (1-cov) + CREME[1] * cov))
            ligne[o+2] = int(round(VERT[2] * (1-cov) + CREME[2] * cov))
        lignes.append(ligne)
    return lignes


if __name__ == "__main__":
    w, h, alpha = decoder_png_rgba(SRC)
    print("source", w, "x", h)
    ecrire_png_rgb(os.path.join(DOSSIER, "icon-192.png"), 192, fabriquer(192, w, h, alpha))
    ecrire_png_rgb(os.path.join(DOSSIER, "icon-512.png"), 512, fabriquer(512, w, h, alpha))
