"""Regenerate docs/ADDED_POIS_map.html, the interactive Astoria 8K POI map.

The map is a stack of world-aligned layers: one base map at a time, any number
of overlays on top, then the POI pins. Every layer covers the full
8192x8192 world north-up, so nothing needs registering.

    python tools/mapgen.py                         # rebuild from the repo
    python tools/mapgen.py --maps "C:\\path\\to\\maps"   # add your own map renders
    python tools/mapgen.py --inline                # one self-contained .html

Maps passed with --maps are added as base layers, and the first one (natural
filename order) becomes the default base. They must be square, north-up and
cover the whole world, which is what every 7 Days to Die map export already is.
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import shutil
import sys

from PIL import Image

import maplayers

Image.MAX_IMAGE_PIXELS = None

# Windows has no .webp in its registry, so guess_type() returns None there and
# --inline would label the payload image/png. Register it rather than rely on it.
mimetypes.add_type("image/webp", ".webp")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WORLD = os.path.join(ROOT, "GeneratedWorlds", "Astoria 8K")
OUTDIR = os.path.join(ROOT, "docs", "maps")
OUTHTML = os.path.join(ROOT, "docs", "ADDED_POIS_map.html")
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif")


def natural(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def label_from(filename):
    stem = os.path.splitext(os.path.basename(filename))[0]
    stem = re.sub(r"[_\-]+", " ", stem).strip()
    stem = re.sub(r"\s+", " ", stem)
    return stem[:1].upper() + stem[1:] if stem else "Map"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "map"


def import_user_maps(maps_dir, out, size, quality):
    """Copy the user's own renders in as base layers, as WebP no larger than
    `size` - a render already smaller than that is kept at its own resolution."""
    files = sorted(
        (f for f in os.listdir(maps_dir) if f.lower().endswith(IMG_EXT)),
        key=natural,
    )
    if not files:
        print("  no images found in %s" % maps_dir, file=sys.stderr)
        return []

    layers = []
    for i, f in enumerate(files):
        src = os.path.join(maps_dir, f)
        im = Image.open(src)
        if im.width != im.height:
            print(
                "  ! %s is %dx%d, not square - it will be stretched to the world "
                "square and will not line up with the pins" % (f, im.width, im.height),
                file=sys.stderr,
            )
        # never scale up: enlarging a 2000 px export to 2048 invents no detail,
        # it just costs bytes and softens what is there
        n = min(size, max(im.size))
        im = im.convert("RGB")
        if im.size != (n, n):
            im = im.resize((n, n), Image.LANCZOS)
        name = "user-%02d-%s.webp" % (i + 1, slug(os.path.splitext(f)[0])[:40])
        im.save(os.path.join(out, name), quality=quality, method=6)
        layers.append(
            {
                "id": "u%d" % (i + 1),
                "label": label_from(f),
                "kind": "base",
                "file": "maps/" + name,
                "note": "your render \u00b7 " + f,
            }
        )
        print("  + %-28s %s" % (label_from(f), name))
    return layers


def build(args):
    os.makedirs(OUTDIR, exist_ok=True)
    print("building layers at %dx%d" % (args.size, args.size))

    user = import_user_maps(args.maps, OUTDIR, args.size, args.quality) if args.maps else []

    # your own maps replace the old foundation render rather than sitting
    # alongside it - it only stays as a fallback when there is nothing else
    base_render = os.path.join(OUTDIR, "base_render.jpg")
    keep_render = os.path.exists(base_render) and (not user or args.keep_render)
    if user and not args.keep_render:
        print("  - dropped the old foundation render, your maps replace it")
    elif not os.path.exists(base_render):
        print("  ! docs/maps/base_render.jpg missing, no foundation render layer", file=sys.stderr)

    maplayers.roads(WORLD, OUTDIR, args.size)
    maplayers.biomes(WORLD, OUTDIR, args.size)
    maplayers.regions(WORLD, OUTDIR, args.size)
    print("  + roads, biomes, regions from the world PNGs")

    layers = list(user)
    if keep_render:
        layers.append(
            {
                "id": "render",
                "label": "Game render",
                "kind": "base",
                "file": "maps/base_render.jpg",
                "note": "the original foundation map",
            }
        )
    layers += [
        {
            "id": "biomes-b",
            "label": "Biomes",
            "kind": "base",
            "file": "maps/biomes.png",
            "note": "biomes.png, flat colour",
        },
        {
            "id": "regions-b",
            "label": "Terrain zones",
            "kind": "base",
            "file": "maps/regions.png",
            "note": "regions.png, the world's terrain banding",
        },
        {
            "id": "roads",
            "label": "Roads",
            "kind": "overlay",
            "file": "maps/roads.png",
            "op": 100,
            "on": True,
            "note": "splat3.png \u00b7 grey asphalt, tan gravel",
        },
        {
            "id": "biomes-o",
            "label": "Biomes",
            "kind": "overlay",
            "file": "maps/biomes.png",
            "op": 35,
            "on": False,
            "note": "tint the base with the biome colours",
        },
        {
            "id": "regions-o",
            "label": "Terrain zones",
            "kind": "overlay",
            "file": "maps/regions.png",
            "op": 40,
            "on": False,
            "note": "tint the base with the terrain banding",
        },
    ]

    # the first base layer in the list is what the map opens on
    for l in layers:
        if l["kind"] == "base":
            l["def"] = True
            break

    for l in layers:
        p = os.path.join(ROOT, "docs", l["file"])
        l["kb"] = round(os.path.getsize(p) / 1024)

    return layers


def inline(layers):
    for l in layers:
        p = os.path.join(ROOT, "docs", l["file"])
        mime = mimetypes.guess_type(p)[0] or "image/png"
        with open(p, "rb") as fh:
            l["file"] = "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode("ascii"))
    return layers


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--maps", metavar="DIR", help="folder of your own full-world map renders")
    ap.add_argument("--size", type=int, default=2048, help="layer resolution, px (default 2048)")
    ap.add_argument("--quality", type=int, default=82, help="WebP quality for --maps imports (default 82)")
    ap.add_argument(
        "--keep-render",
        action="store_true",
        help="keep the old foundation render as a base layer even when --maps supplies your own",
    )
    ap.add_argument("--inline", action="store_true", help="embed every layer, one portable .html")
    ap.add_argument("--out", default=OUTHTML)
    args = ap.parse_args()

    if args.maps and not os.path.isdir(args.maps):
        ap.error("--maps: no such folder: %s" % args.maps)

    with open(os.path.join(HERE, "mapdata.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    layers = build(args)
    legend = maplayers.biome_legend(WORLD)
    if args.inline:
        layers = inline(layers)

    with open(os.path.join(HERE, "map_template.html"), encoding="utf-8") as fh:
        html = fh.read()

    for token, value in [
        ("__POIS__", data["pois"]),
        ("__PACKS__", data["packs"]),
        ("__SPAWNS__", data["spawns"]),
        ("__LAYERS__", layers),
        ("__BIOMELEGEND__", legend),
    ]:
        html = html.replace(token, json.dumps(value, separators=(",", ":")))

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(html)

    nbase = sum(1 for l in layers if l["kind"] == "base")
    print(
        "wrote %s  (%.1f KB, %d base layers, %d overlays)"
        % (
            os.path.relpath(args.out, ROOT),
            os.path.getsize(args.out) / 1024,
            nbase,
            len(layers) - nbase,
        )
    )


if __name__ == "__main__":
    main()
