"""Genere icon-192.png et icon-512.png sans dependance externe (pas de Pillow).

Motif : feuille creme sur fond vert sauge, reprise de la charte du site
les-ailes-de-flo.com (vert #4F6450, creme #F8F6F1).
"""
import math
import os
import struct
import zlib

VERT = (0x4F, 0x64, 0x50)
CREME = (0xF8, 0xF6, 0xF1)

DOSSIER = os.path.join(
    os.path.expanduser("~"), "Documents", "Projets perso", "cahier-clientele"
)

ECART = 0.55      # ecart des centres des deux cercles -> forme de feuille
RAYON = 1.0
ECHELLE = 0.62    # la feuille tient dans la zone sure des icones maskable
ANGLE = math.radians(45)
VEINE = 0.030     # demi-epaisseur de la nervure centrale


def dans_feuille(x, y):
    """x, y dans [-1, 1] : True si le point est dans la feuille."""
    xe, ye = x / ECHELLE, y / ECHELLE
    c, s = math.cos(-ANGLE), math.sin(-ANGLE)
    u, v = xe * c - ye * s, xe * s + ye * c
    if math.hypot(u + ECART, v) > RAYON:
        return False
    if math.hypot(u - ECART, v) > RAYON:
        return False
    # Nervure centrale evidee, sauf tout en haut (pointe pleine).
    if abs(u) < VEINE / ECHELLE and v < 0.72:
        return False
    return True


def rendu(taille):
    """Renvoie les octets RGB de l'icone, avec anticrenelage 3x3."""
    lignes = []
    demi = taille / 2.0
    for py in range(taille):
        ligne = bytearray()
        for px in range(taille):
            couvert = 0
            for sy in range(3):
                for sx in range(3):
                    x = (px + (sx + 0.5) / 3 - demi) / demi
                    y = (py + (sy + 0.5) / 3 - demi) / demi
                    if dans_feuille(x, y):
                        couvert += 1
            t = couvert / 9.0
            for i in range(3):
                ligne.append(int(round(VERT[i] * (1 - t) + CREME[i] * t)))
        lignes.append(bytes(ligne))
    return lignes


def morceau(nom, donnees):
    return (
        struct.pack(">I", len(donnees))
        + nom
        + donnees
        + struct.pack(">I", zlib.crc32(nom + donnees) & 0xFFFFFFFF)
    )


def ecrire_png(chemin, taille):
    lignes = rendu(taille)
    brut = b"".join(b"\x00" + l for l in lignes)  # filtre 0 sur chaque ligne
    png = b"\x89PNG\r\n\x1a\n"
    png += morceau(b"IHDR", struct.pack(">IIBBBBB", taille, taille, 8, 2, 0, 0, 0))
    png += morceau(b"IDAT", zlib.compress(brut, 9))
    png += morceau(b"IEND", b"")
    with open(chemin, "wb") as f:
        f.write(png)
    print(chemin, os.path.getsize(chemin), "octets")


ecrire_png(os.path.join(DOSSIER, "icon-192.png"), 192)
ecrire_png(os.path.join(DOSSIER, "icon-512.png"), 512)
