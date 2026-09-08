"""Read and write 7 Days To Die V2.0 prefab files (.tts version 19, .blocks.nim).

Layout of a .tts, all little-endian, n = sx*sy*sz and index = x + sx*(y + sy*z):

    "tts\\0"            magic
    uint32             version (19)
    uint16 x, y, z     size
    uint32[n]          block values - type = v & 0xFFFF,
                                      rotation = (v >> 16) & 0x3F,
                                      meta = v >> 22
    int8[n]            density
    uint16[n]          damage
    uint32 c; byte[c]  bit per block: "this block carries paint"
    byte[8] * popcount six face texture ids + two pad bytes, in block order
    uint32 c; byte[c]  bit per block, second flag plane
    ...                tile entities; a bare uint32 0 when there are none

Doors do not need a tile entity record - the game builds one when the prefab is
placed (stock POIs ship working doors with an empty trailer), so the trailer is
carried through untouched.
"""
import struct


class Nim:
    """The block-name table that travels beside a prefab."""

    def __init__(self, path=None):
        self.id2name = {}
        if path:
            self.load(path)

    def load(self, path):
        d = open(path, 'rb').read()
        ver, cnt = struct.unpack_from('<II', d, 0)
        o = 8
        for _ in range(cnt):
            bid, = struct.unpack_from('<I', d, o)
            o += 4
            ln = d[o]
            o += 1
            self.id2name[bid] = d[o:o + ln].decode('utf-8')
            o += ln
        assert o == len(d), (o, len(d))

    @property
    def name2id(self):
        return {v: k for k, v in self.id2name.items()}

    def save(self, path, ids):
        ids = sorted(set(ids))
        out = struct.pack('<II', 1, len(ids))
        for b in ids:
            nm = self.id2name[b].encode('utf-8')
            out += struct.pack('<I', b) + bytes([len(nm)]) + nm
        open(path, 'wb').write(out)


class Prefab:
    def __init__(self, path=None):
        if path:
            self.load(path)

    def load(self, path):
        d = open(path, 'rb').read()
        assert d[:4] == b'tts\0', d[:4]
        self.ver, = struct.unpack_from('<I', d, 4)
        self.sx, self.sy, self.sz = struct.unpack_from('<HHH', d, 8)
        n = self.n = self.sx * self.sy * self.sz
        o = 14
        self.blocks = list(struct.unpack_from('<%dI' % n, d, o))
        o += 4 * n
        self.density = bytearray(d[o:o + n])
        o += n
        self.damage = list(struct.unpack_from('<%dH' % n, d, o))
        o += 2 * n
        cA, = struct.unpack_from('<I', d, o)
        o += 4
        bitA = d[o:o + cA]
        o += cA
        pc = sum(bin(b).count('1') for b in bitA)
        blob = d[o:o + 8 * pc]
        o += 8 * pc
        cB, = struct.unpack_from('<I', d, o)
        o += 4
        self.bitB = bytearray(d[o:o + cB])
        o += cB
        self.trailer = d[o:]
        self.tex = {}
        k = 0
        for i in range(n):
            if bitA[i >> 3] >> (i & 7) & 1:
                self.tex[i] = blob[8 * k:8 * k + 8]
                k += 1
        assert k == pc

    def idx(self, x, y, z):
        return x + self.sx * (y + self.sy * z)

    def at(self, x, y, z):
        return self.blocks[self.idx(x, y, z)]

    def dump(self):
        n = self.n
        bitA = bytearray((n + 7) // 8)
        blob = bytearray()
        for i in sorted(self.tex):
            bitA[i >> 3] |= 1 << (i & 7)
            blob += self.tex[i]
        out = bytearray(b'tts\0')
        out += struct.pack('<I', self.ver)
        out += struct.pack('<HHH', self.sx, self.sy, self.sz)
        out += struct.pack('<%dI' % n, *self.blocks)
        out += bytes(self.density)
        out += struct.pack('<%dH' % n, *self.damage)
        out += struct.pack('<I', len(bitA)) + bytes(bitA)
        out += bytes(blob)
        out += struct.pack('<I', len(self.bitB)) + bytes(self.bitB)
        out += self.trailer
        return bytes(out)

    def save(self, path):
        open(path, 'wb').write(self.dump())


def btype(v):
    return v & 0xFFFF


def brot(v):
    return (v >> 16) & 0x3F


def bmeta(v):
    return v >> 22


def bval(t, rot=0, meta=0):
    return (t & 0xFFFF) | ((rot & 0x3F) << 16) | (meta << 22)
