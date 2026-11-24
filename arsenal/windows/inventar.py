"""Inventar de procese si jurnal de evenimente Windows, modelate ca obiecte.

Lucrarea A: clasele Proces si Eveniment, cu metoda e_suspect, incarcate din JSON.
Lucrarea B: clasa-container Inventar si raportul de alarme, din terminal.
"""

import argparse
import json
import os
from dataclasses import asdict, dataclass

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        """True daca procesul ruleaza din Temp sau Roaming."""
        return any(cale in self.cale for cale in CAI_SUSPECTE)


@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        """True daca ID-ul e cunoscut ca periculos sau nivelul e critical."""
        return self.id in SUSPECTE_ID or self.nivel == "critical"


def procese_din_json(cale):
    """Intoarce lista de obiecte Proces citite din fisierul JSON."""
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]


def evenimente_din_json(cale):
    """Intoarce lista de obiecte Eveniment citite din fisierul JSON."""
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]


@dataclass
class Inventar:
    procese: list

    @classmethod
    def din_json(cls, cale):
        """Constructor alternativ: umple inventarul din fisierul JSON."""
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])

    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        """Procesele care se declara singure suspecte."""
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self):
        """Procesele grupate pe utilizator: dict user -> lista de nume."""
        grup = {}
        for p in self.procese:
            grup.setdefault(p.user, []).append(p.nume)
        return grup


def main():
    p = argparse.ArgumentParser(description="Inventar de procese si evenimente Windows")
    p.add_argument("capturi", help="folderul cu procese.json si evenimente.json")
    p.add_argument("--json", action="store_true", help="raport JSON in loc de rezumat")
    a = p.parse_args()

    inv = Inventar.din_json(os.path.join(a.capturi, "procese.json"))
    ev = evenimente_din_json(os.path.join(a.capturi, "evenimente.json"))
    alarma = [e for e in ev if e.e_suspect()]

    if a.json:
        raport = {
            "procese": len(inv),
            "suspecte": [asdict(p) for p in inv.suspecte()],
            "evenimente": len(ev),
            "alarma": [asdict(e) for e in alarma],
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    print(f"Procese: {len(inv)} | suspecte: {len(inv.suspecte())}")
    for proc in inv.suspecte():
        print(f"  [{proc.pid}] {proc.nume}  ({proc.user})  {proc.cale}")

    print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")
    for e in alarma:
        print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")


if __name__ == "__main__":
    main()
