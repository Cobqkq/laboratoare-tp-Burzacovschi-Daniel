# A1. Text si octeti: incalzirea

s = "Salut"
b = s.encode()      # bytes
print(b, b[0])      # b"Salut" 83
print(b.hex())
print(bytes.fromhex(b.hex()))

# A2. Recunosti stratul dupa forma

def ghici_strat(s):
    import re
    if re.search(r"%[0-9a-fA-f]{2}",s):
        return "url"
    elif re.fullmatch(r"[0-9a-fA-F]+",s) and len(s) % 2 == 0:
        return "hex"
    elif re.fullmatch(r"[A-Za-z0-9+/]+={0,2}",s):
        return "base64"
    else:
        return "necunoscut"

# A3. Desfaci stratul recunoscut

def desfa(s):
    import base64
    from urllib.parse import unquote
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    elif strat == "hex":
        return strat, bytes.fromhex(s)
    elif strat == "url":
        return strat, unquote(s).encode()
    return strat, s.encode()

# A4. Straturi multiple, intr-o bucla

def citibil(b):
    return all(32 <= c < 127 for c in b)


def a4_straturi():
    val = "NTM1OTU3NTk="
    for _ in range(8):
        strat, b = desfa(val)
        if citibil(b):
            print(strat,"->", b)
            break
        else:
            val = b.decode()
            continue

# A5. Spargi un XOR cu cheie de un octet

def a5_xor():
    date = open("probe/xor.bin", "rb").read()
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            print("cheie:", k, clar.decode())

# A6. Spargi un hash prin dictionar

def a6_hash():
    import hashlib
    tinta = open("probe/hashuri.txt").readline().strip()
    print(len(tinta))   # 32 md5 / 40 sha1 / 64 sha256
    for cuv in open("probe/wordlist.txt", encoding="latin1"):
        cuv = cuv.strip()
        if hashlib.md5(cuv.encode()).hexdigest() == tinta:
            print("gasit:", cuv)
            break

# A7. argparse, fisa JSON si un test

def main():
    import argparse
    import json
    p = argparse.ArgumentParser()
    p.add_argument("intrare")          # sir sau cale
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()
    if a.fisier:
        val = open(a.intrare, "rb").read().decode("utf-8").strip()
    else:
        val = a.intrare
    strat, b = "necunoscut", val.encode()
    for _ in range(8):
        strat_nou, b_nou = desfa(val)
        if strat_nou == "necunoscut":
            break
        strat, b = strat_nou, b_nou
        val = b.decode()
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
        json.dump({"strat": strat, "rezultat": b.decode()}, f, indent=2)

if __name__ == "__main__":
    main()
