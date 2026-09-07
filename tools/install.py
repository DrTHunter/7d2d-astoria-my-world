#!/usr/bin/env python3
"""
Patch a stock Astoria 8K world into DrTHunter's version.

Run it with no arguments and it finds your 7 Days to Die folder itself:

    python tools/install.py

It will not touch anything until every check passes, and it copies the stock
files to <name>.stock-backup first, so you can always go back.
"""
import os, sys, json, shutil, zlib, struct, hashlib, argparse

HERE   = os.path.dirname(os.path.abspath(__file__))
PATCH  = os.path.join(os.path.dirname(HERE), "world-patch")
MODSRC = os.path.join(os.path.dirname(HERE), "mods", "Astoria-StarterBases")


def md5(path, chunk=1 << 20):
    m = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            m.update(block)
    return m.hexdigest()


def find_game_dir():
    for env in ("APPDATA",):
        base = os.environ.get(env)
        if base:
            p = os.path.join(base, "7DaysToDie")
            if os.path.isdir(p):
                return p
    for p in (os.path.expanduser("~/.local/share/7DaysToDie"),
              os.path.expanduser("~/Library/Application Support/7DaysToDie")):
        if os.path.isdir(p):
            return p
    return None


def apply_dtm(stock_path, out_path, patch_path):
    blob = zlib.decompress(open(patch_path, "rb").read())
    if blob[:4] != b"D2DT":
        sys.exit("dtm.patch is corrupt (bad magic)")
    ver, count = struct.unpack_from("<II", blob, 4)
    if ver != 1:
        sys.exit(f"dtm.patch version {ver} is newer than this installer")
    off = 12
    offsets = memoryview(blob)[off:off + 4 * count].cast("I")
    values  = memoryview(blob)[off + 4 * count:off + 6 * count].cast("H")
    data = bytearray(open(stock_path, "rb").read())
    for i in range(count):
        struct.pack_into("<H", data, offsets[i] * 2, values[i])
    open(out_path, "wb").write(data)
    return count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game-dir", help=r"e.g. %APPDATA%\7DaysToDie")
    ap.add_argument("--world", default="Astoria 8K")
    ap.add_argument("--force", action="store_true",
                    help="patch even if the stock files do not match the expected checksums")
    a = ap.parse_args()

    man = json.load(open(os.path.join(PATCH, "manifest.json")))
    game = a.game_dir or find_game_dir()
    if not game:
        sys.exit("Could not find your 7DaysToDie folder. Pass --game-dir.")
    world = os.path.join(game, "GeneratedWorlds", a.world)
    print(f"game folder : {game}")
    print(f"world folder: {world}")
    if not os.path.isdir(world):
        sys.exit(f"\n'{a.world}' is not installed.\nInstall the base map first: {man['base_map']}\n"
                 f"It must end up at {world}")

    # ---- 1. check the stock world is the version this patch was built against ----
    print("\nchecking the stock world ...")
    ok = True
    for name, want in man["stock"].items():
        p = os.path.join(world, name)
        if not os.path.exists(p):
            print(f"  MISSING  {name}"); ok = False; continue
        got = md5(p)
        if got == want:
            print(f"  ok       {name}")
        elif got == man["result"][name]:
            print(f"  ALREADY PATCHED  {name}")
        else:
            print(f"  MISMATCH {name}\n           expected {want}\n           found    {got}"); ok = False
    if not ok and not a.force:
        sys.exit("\nYour Astoria files are not the version this patch was built against.\n"
                 f"Expected: {man['base_map']}\n"
                 "Reinstall that exact version, or re-run with --force if you know what you are doing.")

    # ---- 2. back up, then patch ----
    print("\npatching ...")
    for name in man["stock"]:
        src = os.path.join(world, name)
        bak = src + ".stock-backup"
        if os.path.exists(src) and not os.path.exists(bak):
            shutil.copy2(src, bak); print(f"  backed up {name} -> {os.path.basename(bak)}")
    n = apply_dtm(os.path.join(world, "dtm.raw.stock-backup"),
                  os.path.join(world, "dtm.raw"),
                  os.path.join(PATCH, "dtm.patch"))
    print(f"  dtm.raw        {n} cells changed (the levelled pads and the roads)")
    for name in ("prefabs.xml", "spawnpoints.xml"):
        shutil.copy2(os.path.join(PATCH, name), os.path.join(world, name))
        print(f"  {name:<14} replaced")
    for junk in ("dtm_processed.raw", "splat3_processed.png", "splat4_processed.png",
                 "splat3_half.png", "splat4_half.png"):
        p = os.path.join(world, junk)
        if os.path.exists(p):
            os.remove(p); print(f"  removed cache  {junk}")

    # ---- 3. verify the result ----
    print("\nverifying ...")
    bad = [n2 for n2, want in man["result"].items() if md5(os.path.join(world, n2)) != want]
    if bad:
        sys.exit(f"FAILED: {bad} do not match the expected result. Restore the .stock-backup files.")
    print("  all three files match the expected checksums")

    # ---- 4. the starter-base mod ----
    dst = os.path.join(game, "Mods", "Astoria-StarterBases")
    print(f"\ninstalling the starter-base mod -> {dst}")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(MODSRC, dst)
    print(f"  {len(os.listdir(os.path.join(dst,'Prefabs','POIs')))} files")

    print(f"\nDone. {man['decorations']} POIs, {man['dtm_cells_changed']} terrain cells.")
    print("Start a NEW save on 'Astoria 8K' - an existing save keeps its old chunks.")


if __name__ == "__main__":
    main()
