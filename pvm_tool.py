
import sys, struct, os, re, argparse
MAGIC_PVMH = b'PVMH'
MAGIC_PVRT = b'PVRT'

def find_pvrt_offsets(buf):
    return [m.start() for m in re.finditer(MAGIC_PVRT, buf)]

def extract(pvm_path, out_dir):
    data = open(pvm_path,'rb').read()
    # Header region is everything before the first PVRT
    pvrt_offs = find_pvrt_offsets(data)
    if not pvrt_offs:
        raise SystemExit("No PVRT blocks found.")
    header = data[:pvrt_offs[0]]
    # Pull count from header if present (optional)
    count = struct.unpack_from("<H", data, 10)[0] if data[:4]==MAGIC_PVMH else len(pvrt_offs)
    # Names from header
    names=[]
    for m in re.finditer(rb'[A-Za-z0-9_\-]{3,}\x00', header):
        s = m.group()[:-1].decode('ascii', errors='ignore')
        names.append(s)
    if len(names) >= len(pvrt_offs):
        names = names[-len(pvrt_offs):]
    else:
        while len(names) < len(pvrt_offs):
            names.append(f'asset_{len(names)}')
    os.makedirs(out_dir, exist_ok=True)
    for i, off in enumerate(pvrt_offs):
        end = pvrt_offs[i+1] if i+1 < len(pvrt_offs) else len(data)
        chunk = data[off:end]
        name = names[i] if i < len(names) else f'asset_{i}'
        out_path = os.path.join(out_dir, f"{i:02d}_{name}.pvr")
        open(out_path,'wb').write(chunk)
        print(f"wrote {out_path}  (0x{len(chunk):X} bytes) at 0x{off:X}")

def repack(pvm_path, in_dir, out_path):
    orig = open(pvm_path,'rb').read()
    pvrt_offs = find_pvrt_offsets(orig)
    if not pvrt_offs:
        raise SystemExit("Original has no PVRT blocks.")
    header = orig[:pvrt_offs[0]]  # preserves full header/padding
    files = [fn for fn in os.listdir(in_dir) if fn.lower().endswith('.pvr')]
    if not files:
        raise SystemExit("No .pvr files found to repack.")
    def sort_key(fn):
        m = re.match(r'(\d+)_', fn)
        return (int(m.group(1)) if m else 1e9, fn.lower())
    files.sort(key=sort_key)
    with open(out_path,'wb') as out:
        out.write(header)
        for fn in files:
            out.write(open(os.path.join(in_dir, fn),'rb').read())
            print(f"added {fn}")
    print(f"Repacked to {out_path}")

def main():
    ap = argparse.ArgumentParser(description="Simple PVM extractor/repacker for Dreamcast PVRT textures")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ap_e = sub.add_parser("extract")
    ap_e.add_argument("pvm")
    ap_e.add_argument("out_dir")
    ap_r = sub.add_parser("repack")
    ap_r.add_argument("pvm")
    ap_r.add_argument("in_dir")
    ap_r.add_argument("out_pvm")
    args = ap.parse_args()
    if args.cmd=="extract":
        extract(args.pvm, args.out_dir)
    else:
        repack(args.pvm, args.in_dir, args.out_pvm)

if __name__=="__main__":
    main()
