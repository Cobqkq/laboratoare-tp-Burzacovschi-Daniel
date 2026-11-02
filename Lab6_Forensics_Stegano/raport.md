# Laborator 6 — Informații invizibile: forensics și steganografie

Toate comenzile au fost rulate din rădăcina proiectului, cu mediul virtual activat.
Rezultatele de mai jos sunt output real, nu capturi de ecran.

## Lucrarea A — Decoder universal (`arsenal/forensics/decode.py`)

### 1. Mesajul cu straturi de codare

Fișier: `probe/mesaj.txt`

Straturile descoperite, în ordine:

```text
base64 → base64 → hex → text
```

Rezultat final:

```text
FLAG{straturi_de_encoding}
```

Comenzi:

```bash
python arsenal/forensics/decode.py probe/mesaj.txt --fisier
cat arsenal/forensics/fisa.json
```

Conținutul fișei:

```json
{
  "strat": "hex",
  "rezultat": "FLAG{straturi_de_encoding}"
}
```

### 2. XOR cu cheie de un octet

Fișier: `probe/xor.bin`

Cheia găsită: **128**

Textul decodat:

```text
Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}
```

Comandă:

```bash
python -c "from arsenal.forensics.decode import a5_xor; a5_xor()"
```

### 3. Hash spart prin dicționar

Fișier: `probe/hashuri.txt`, wordlist: `probe/wordlist.txt`

Algoritm identificat după lungime: **MD5** (32 de caractere hex)

Parola găsită: **password**

Comandă:

```bash
python -c "from arsenal.forensics.decode import a6_hash; a6_hash()"
```

### 4. Test

```bash
python -m pytest -q
```

```text
1 passed
```

## Lucrarea B — Forensics pe fișiere și steganografie

### 1. Tipul real al fișierelor (B1)

```text
probe/foto.jpg   → jpeg
probe/ascuns.png → png
```

Tipul a fost stabilit după primii octeți (`\xff\xd8` pentru JPEG, `\x89PNG` pentru PNG),
nu după extensie.

### 2. Text citibil din binar (B2)

Comandă:

```bash
python -c "from forensics import b2_strings; b2_strings()"
```

Indiciul apare la coada fișierului, după `IEND`:

```text
secret.txtFLAG{ascuns_prin_carving}
secret.txtPK
```

Adică în `ascuns.png` este lipită o arhivă care conține `secret.txt`.

### 3. Metadate EXIF și GPS (B3)

```text
Model = iPhone 13
DateTime = 2026:09:14 10:30:00
Make = Apple
GPSInfo = {1: 'N', 2: (47.0, 1.0, 0.0), 3: 'E', 4: (28.0, 51.0, 27.0)}
```

Coordonate convertite din grade-minute-secunde în grade zecimale:

```text
latitudine  = 47.016666666666666
longitudine = 28.8575
```

### 4. Arhiva ascunsă (B4)

Comandă:

```bash
python -c "from forensics import b4_carving; b4_carving()"
```

Semnătura `PK\x03\x04` a fost găsită la octetul **781**. Arhiva a fost scrisă în
`gasit.zip` și dezarhivată.

Conținut:

```text
secret.txt
```

Textul din `secret.txt`:

```text
FLAG{ascuns_prin_carving}
```

### 5. Mesajul ascuns prin LSB (B5–B6)

Mesajul a fost scris în ultimii biți ai canalelor R, G, B din `probe/foto.jpg`
și salvat ca `stego.png` (PNG, ca să nu se piardă biții prin compresie).

Comandă:

```bash
python -c "from stego import b5_ascunde, b6_dezvaluie; b5_ascunde(); b6_dezvaluie()"
```

Mesaj dezvăluit:

```text
FLAG{ascuns_in_pixeli}
```

## Concluzii

- Mesajul din `probe/mesaj.txt` era codat în trei straturi succesive și ascundea
  `FLAG{straturi_de_encoding}`.
- XOR pe un singur octet a fost spart prin forță brută; cheia este `128`.
- Hash-ul era MD5, iar parola găsită în wordlist este `password`.
- `ascuns.png` era un PNG valid cu o arhivă ZIP lipită la coadă, găsită prin file
  carving la octetul 781.
- Metadatele EXIF conțineau coordonate GPS reale, convertite în grade zecimale.
- Steganografia LSB a permis ascunderea și recuperarea exactă a mesajului,
  cu condiția salvării în PNG.
