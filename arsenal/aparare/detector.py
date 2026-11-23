"""Lucrarea B - detector de brute force cu prag reglabil si raport JSON."""

import argparse
import json
from collections import Counter

from arsenal.aparare.parse_auth import citeste_esecuri, pe_ip


def suspecti(counts, prag=10):
    """Intoarce lista de (ip, n) cu n >= prag, sortata descrescator.

    counts este un Counter, iar most_common() intoarce perechile
    (ip, numar) deja sortate de la cel mai mare numar la cel mai mic.
    """
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    rezultat = []
    for ip, n in counts.most_common():
        if n >= prag:
            rezultat.append((ip, n))
    return rezultat


def main():
    p = argparse.ArgumentParser(description="Detector de brute force in auth.log")
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    esecuri = citeste_esecuri(a.log)
    counts = pe_ip(esecuri)
    sus = suspecti(counts, a.prag)

    if a.json:
        lista = []
        for ip, n in sus:
            lista.append({"ip": ip, "incercari": n})
        raport = {
            "esecuri": len(esecuri),
            "pe_ip": dict(counts),
            "suspecti": lista,
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    print(f"Esecuri de autentificare: {len(esecuri)}")
    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")
    print(f"Suspecti (prag {a.prag}):")
    if len(sus) == 0:
        print("  niciunul")
    for ip, n in sus:
        print(f"  {ip}  ({n} incercari)  BRUTE FORCE")


if __name__ == "__main__":
    main()
