"""Build the map layer images used by the interactive POI map.

Every layer is a north-up square covering the whole 8192x8192 world, so they all
register against each other and against the POI pins without any offset maths.

Sources, all straight out of the world folder:

  biomes.png    the five biome colours, already the palette the game uses
  splat3.png    R = asphalt, G = gravel -> the road network
  regions.png   terrain zoning bands

splat4.png is deliberately not used: its green channel covers 39% of the map
with ground-cover texturing, which carries no information at map scale.

Run via mapgen.py; this module only writes the images.
"""

import os

import numpy as np
from PIL import Image, ImageFilter

Image.MAX_IMAGE_PIXELS = None

# 7 Days to Die's biome palette, straight from biomes.png.
BIOMES = [
    ((0, 64, 0), "pine forest"),
    ((255, 228, 119), "desert"),
    ((255, 255, 255), "snow"),
    ((255, 168, 0), "burnt forest"),
    ((186, 0, 255), "wasteland"),
]

ASPHALT = (196, 201, 210)
GRAVEL = (214, 180, 126)


def _save_indexed(im, path, colors):
    """PNG, palette-reduced. These layers are flat colour, so this is lossless
    in practice and roughly a tenth the size of RGB."""
    mode = Image.FASTOCTREE if im.mode == "RGBA" else Image.MEDIANCUT
    im.quantize(colors=colors, method=mode).save(path, optimize=True)
    return path


def biomes(world, out, size):
    """Biome map. NEAREST on the way down so biome borders stay hard edges
    instead of blending into colours that are not biomes."""
    src = Image.open(os.path.join(world, "biomes.png")).convert("RGB")
    im = src.resize((size, size), Image.NEAREST)
    return _save_indexed(im, os.path.join(out, "biomes.png"), 16)


def regions(world, out, size):
    src = Image.open(os.path.join(world, "regions.png")).convert("RGB")
    im = src.resize((size, size), Image.NEAREST)
    return _save_indexed(im, os.path.join(out, "regions.png"), 16)


def roads(world, out, size):
    """Road network as a transparent overlay, asphalt and gravel coloured apart.

    Roads are one to a few pixels wide at 8192, so a straight 4x downscale
    drops most of them below visibility. Dilating by one pixel first keeps the
    network continuous once it is resized.
    """
    a = np.asarray(Image.open(os.path.join(world, "splat3.png")).convert("RGBA"))

    # Grow each road class on its own, before a colour is chosen. Dilating the
    # composed RGBA instead takes the maximum of every channel independently,
    # so an asphalt edge meeting a gravel edge came out (214, 201, 210) - a
    # lilac that is neither road colour.
    grow = ImageFilter.MaxFilter(3)
    asphalt = np.asarray(Image.fromarray(a[:, :, 0]).filter(grow))
    gravel = np.asarray(Image.fromarray(a[:, :, 1]).filter(grow))

    rgba = np.zeros(asphalt.shape + (4,), np.uint8)
    rgba[:, :, 3] = np.maximum(asphalt, gravel)
    is_asphalt = asphalt >= gravel
    for c in range(3):
        rgba[:, :, c] = np.where(is_asphalt, ASPHALT[c], GRAVEL[c])

    im = Image.fromarray(rgba, "RGBA").resize((size, size), Image.LANCZOS)
    return _save_indexed(im, os.path.join(out, "roads.png"), 32)


def biome_legend(world):
    """Which biomes actually occur, with their share of the map, so the legend
    never lists a biome this world does not have."""
    a = np.asarray(
        Image.open(os.path.join(world, "biomes.png")).convert("RGB").resize((1024, 1024), Image.NEAREST)
    ).reshape(-1, 3)
    total = len(a)
    out = []
    for rgb, name in BIOMES:
        share = np.all(a == np.array(rgb, np.uint8), axis=1).mean() * 100
        if share >= 0.05:
            out.append({"c": "#%02x%02x%02x" % rgb, "n": name, "pct": round(float(share), 1)})
    out.sort(key=lambda b: -b["pct"])
    return out
